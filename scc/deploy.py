import os
from absl import app
from dotenv import load_dotenv
import vertexai
from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp

from scc.agent import root_agent

def deploy_agent(agent_obj) -> None:
    """Deploy an agent to Vertex AI Agent Engine."""
    adk_app = AdkApp(agent=agent_obj, enable_tracing=True)
    
    remote_agent = agent_engines.create(
        adk_app,
        display_name=agent_obj.name,
        requirements=[
            "google-adk (>=1.18.0)",
            "google-cloud-aiplatform[agent_engines] (>=1.126.0,<2.0.0)",
            "google-genai (>=1.49.0,<2.0.0)",
            "pydantic (>=2.10.6,<3.0.0)",
            "absl-py (>=2.2.1,<3.0.0)",
            "google-auth (>=2.0.0)",
            "python-dotenv (>=1.0.1)",
            "google-cloud-securitycenter (>=1.41.0)",
            "google-cloud-asset (>=4.1.0)",
            "typing-extensions (>=4.15.0)",
            "cloudpickle (>=3.1.0)"
        ],
        extra_packages=[f"./{agent_obj.name}"],
    )
    
    print(f"✅ Deployed agent: {remote_agent.resource_name}")

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
    
    # Initialize Vertex AI
    vertexai.init(
        project=project_id,
        location=location,
        staging_bucket=f"gs://{bucket}",
    )
    
    # Deploy the agent
    deploy_agent(root_agent)

if __name__ == "__main__":
    app.run(main)
