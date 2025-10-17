import os
import random
import dotenv
import google.auth
from typing import Dict, Any
from google.adk.agents import Agent
from google.cloud import webrisk_v1

dotenv.load_dotenv()

_client = None

def _get_client():
    global _client
    if _client is None:
        try:
            _client = webrisk_v1.WebRiskServiceClient()
        except Exception:
            raise
    return _client

def lookup_url(url: str) -> Dict[str, Any]:
    """Checks URLs for threats using Google Cloud Web Risk API."""
    if not url or not url.strip():
        return {
            "error": "URL cannot be empty.",
            "safe": None
        }

    try:
        client = _get_client()
        
        # Define threat types to check
        threat_types = [
            webrisk_v1.ThreatType.MALWARE,
            webrisk_v1.ThreatType.SOCIAL_ENGINEERING,
            webrisk_v1.ThreatType.SOCIAL_ENGINEERING_EXTENDED_COVERAGE,
            webrisk_v1.ThreatType.UNWANTED_SOFTWARE
        ]

        # Call the Web Risk API to search for URL threats
        response = client.search_uris(
            uri=url.strip(),
            threat_types=threat_types
        )
        
        # Process the response
        if response.threat:
            threat_types_found = [t.name for t in response.threat.threat_types]
            return {
                "safe": False,
                "url": url,
                "threat_types": threat_types_found,
                "expire_time": response.threat.expire_time.isoformat() if response.threat.expire_time else None,
                "message": f"Threats found: {', '.join(threat_types_found)}"
            }
        else:
            return {
                "safe": True,
                "url": url,
                "message": f"No threats detected."
            }
            
    except Exception as e:
        return {
            "error": str(e),
            "safe": None,
            "url": url
        }

root_agent = Agent(
    name="web_risk",
    model="gemini-2.5-flash",
    instruction="You are an AI assistant designed to provide helpful information.",
    tools=[lookup_url],
)
