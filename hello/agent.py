import os
import random
import dotenv
from typing import List, Any, Optional
from google.adk.agents import Agent
from google.adk.models import LlmResponse
from google.cloud import modelarmor_v1
from google.genai.types import Content, Part

dotenv.load_dotenv()

def greet(name: str) -> str:
    """Greets a user by name.
    Args:
        name: A string denoting the user's name.
    Returns:
        A string greeting the user.
    """
    return f"Hello, {name}!"

def roll_dice(n_dice: int) -> List[int]:
    """Rolls n_dice 6-sided dice and returns the results.
    Args:
        n_dice: An integer denoting the number of dice to be rolled.
    Returns:
        A list of integers denoting the results of the rolled dice.
    """
    return [random.randint(1, 6) for _ in range(n_dice)]

def sanitize_prompt(callback_context: Any, **kwargs: Any) -> Optional[LlmResponse]:
    """
    Sanitizes the input prompt using Google Cloud Model Armor.
    Returns:
        None: If prompt is safe (Agent proceeds to call Gemini).
        LlmResponse: If prompt is unsafe (Agent skips Gemini and shows this message).
    """
    prompt = getattr(callback_context, "user_content", None)
    
    if hasattr(prompt, "content"):
        prompt = prompt.content
    elif hasattr(prompt, "parts"):
        prompt = prompt.parts[0].text

    if not prompt or not isinstance(prompt, str):
        return None

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    template_id = os.getenv("MODEL_ARMOR_TEMPLATE_ID", "ma-all-med")
    endpoint = f"modelarmor.{location}.rep.googleapis.com"

    client = modelarmor_v1.ModelArmorClient(
        client_options={"api_endpoint": endpoint}
    )

    request = modelarmor_v1.SanitizeUserPromptRequest(
        name=f"projects/{project_id}/locations/{location}/templates/{template_id}",
        user_prompt_data=modelarmor_v1.DataItem(text=prompt)
    )
    
    response = client.sanitize_user_prompt(request=request)

    if response.sanitization_result.filter_match_state == modelarmor_v1.FilterMatchState.NO_MATCH_FOUND:
        return None
    else:
        # Extract violation details from filter_results
        violations = []

        # Map confidence levels to readable strings
        confidence_map = {
            0: "unspecified",
            1: "low",
            2: "medium",
            3: "high",
        }
        
        if hasattr(response.sanitization_result, 'filter_results'):
            filter_results = response.sanitization_result.filter_results
            
            # Check RAI filter
            if 'rai' in filter_results:
                rai_result = filter_results['rai'].rai_filter_result
                if rai_result.match_state == modelarmor_v1.FilterMatchState.MATCH_FOUND:
                    for category, result in rai_result.rai_filter_type_results.items():
                        if result.match_state == modelarmor_v1.FilterMatchState.MATCH_FOUND:
                            confidence = getattr(result, 'confidence_level', None)
                            if confidence is not None:
                                confidence_str = confidence_map.get(int(confidence), str(confidence))
                                violations.append(f"{category} (confidence: {confidence_str})")
                            else:
                                violations.append(category)
            
            # Check PI and Jailbreak filter
            if 'pi_and_jailbreak' in filter_results:
                pi_result = filter_results['pi_and_jailbreak'].pi_and_jailbreak_filter_result
                if pi_result.match_state == modelarmor_v1.FilterMatchState.MATCH_FOUND:
                    confidence = getattr(pi_result, 'confidence_level', None)
                    if confidence is not None:
                        confidence_str = confidence_map.get(int(confidence), str(confidence))
                        violations.append(f"prompt_injection_or_jailbreak (confidence: {confidence_str})")
                    else:
                        violations.append("prompt_injection_or_jailbreak")
            
            # Check Sensitive Data Protection filter
            if 'sdp' in filter_results:
                sdp_result = filter_results['sdp'].sdp_filter_result
                sdp_match_state = None
                info_types = set()
                
                # Check inspect_result
                if hasattr(sdp_result, 'inspect_result'):
                    inspect_result = sdp_result.inspect_result
                    sdp_match_state = getattr(inspect_result, 'match_state', None)
                    
                    # Extract findings if available
                    if hasattr(inspect_result, 'findings') and inspect_result.findings:
                        for finding in inspect_result.findings:
                            if hasattr(finding, 'info_type') and hasattr(finding.info_type, 'name'):
                                info_types.add(finding.info_type.name)
                
                # Add violation if match found
                if sdp_match_state == modelarmor_v1.FilterMatchState.MATCH_FOUND:
                    if info_types:
                        violations.append(f"sensitive_data ({', '.join(sorted(info_types))})")
                    else:
                        violations.append("sensitive_data")
            
            # Check Malicious URIs
            if 'malicious_uris' in filter_results:
                uri_result = filter_results['malicious_uris'].malicious_uri_filter_result
                if uri_result.match_state == modelarmor_v1.FilterMatchState.MATCH_FOUND:
                    violations.append("malicious_uri")
            
            # Check CSAM
            if 'csam' in filter_results:
                csam_result = filter_results['csam'].csam_filter_filter_result
                if csam_result.match_state == modelarmor_v1.FilterMatchState.MATCH_FOUND:
                    violations.append("csam")
        
        violations_str = ", ".join(violations) if violations else "Content policy violation detected."
        
        block_msg = (
            f"🚫 **Message blocked by Model Armor**\n\n"
            f"Reason: {violations_str}"
        )
        return LlmResponse(
            content = Content(
                role="model",
                parts=[Part(text=block_msg)]
            )
        )

root_agent = Agent(
    name="hello",
    model="gemini-2.5-flash",
    instruction="You are an AI assistant designed to provide helpful information.",
    before_model_callback=sanitize_prompt,
    tools=[greet, roll_dice],
)
