import dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .sub_agents.scc import scc_agent
from .sub_agents.web_risk import web_risk_agent

dotenv.load_dotenv()

MODEL = "gemini-2.5-flash"

security_manager = LlmAgent(
    name="security_manager",
    model=MODEL,
    instruction=prompt.SECURITY_MANAGER_PROMPT,
    output_key="security_manager_output",
    tools=[
      AgentTool(agent=scc_agent),
      AgentTool(agent=web_risk_agent)
    ],
)

root_agent = security_manager
