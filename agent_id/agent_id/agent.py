from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    name='agent_id',
    model='gemini-2.5-flash-lite',
    instruction='Answer user questions to the best of your knowledge',
)
