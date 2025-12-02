import os
from google.adk.agents.llm_agent import Agent

def get_secret() -> str:
    """Retrieves the secret directly from Secret Manager via the environment variable."""
    secret = os.environ.get("SECRET")
    if secret:
        return secret
    else:
        return "Error: SECRET environment variable not found."

root_agent = Agent(
    name='secret_agent',
    model='gemini-2.5-flash',
    instruction='Answer user questions to the best of your knowledge',
    tools=[get_secret],
)
