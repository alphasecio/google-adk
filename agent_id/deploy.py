import os
import vertexai
from vertexai import agent_engines, types
from agent_id.agent import root_agent
from dotenv import load_dotenv

def main(argv: list[str]) -> None:
    del argv
    load_dotenv()
    
    # Get config from environment
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    bucket = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
    
    # Validate config
    if not all([project_id, location, bucket]):
        print("❌ Missing required environment variables:")
        if not project_id: print("  - GOOGLE_CLOUD_PROJECT")
        if not location: print("  - GOOGLE_CLOUD_LOCATION")
        if not bucket: print("  - GOOGLE_CLOUD_STORAGE_BUCKET")
        return
    
    client = vertexai.Client(
        project=project_id,
        location=location,
        http_options=dict(api_version="v1beta1")
    )

    remote_agent = client.agent_engines.create(
        agent=root_agent,
        config={
            "display_name": root_agent.name,
            "identity_type": types.IdentityType.AGENT_IDENTITY,
            "requirements": [
                "google-adk (>=1.19.0)",
                "google-cloud-aiplatform[agent_engines] (>=1.128.0,<2.0.0)",
                "google-genai (>=1.52.0,<2.0.0)",
                "pydantic (>=2.10.6,<3.0.0)",
                "absl-py (>=2.2.1,<3.0.0)",
                "google-auth (>=2.0.0)",
                "python-dotenv (>=1.0.1)",
            ],
            "extra_packages": [f"./{root_agent.name}"],
            "staging_bucket": f"gs://{bucket}",
        },
    )

    print(f"✅ Deployed agent: {remote_agent.name}")

if __name__ == "__main__":
    app.run(main)
