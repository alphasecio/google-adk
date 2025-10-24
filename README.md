# Google ADK
Sample Google Agent Development Kit ([ADK](https://google.github.io/adk-docs/)) agents with callable tools. Each agent can be deployed to [Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview), and published to [Gemini Enterprise](https://cloud.google.com/gemini-enterprise?hl=en) (previously Agentspace).


### 🤖 Agent Summary
| Agent    | Description                                                                 |
|----------|-----------------------------------------------------------------------------|
| hello    | Greets users and rolls dice using Python functions.                         |
| web_risk | Detects malware, phishing, and unwanted software URLs using Web Risk API.   |
| scc      | Lists top SCC findings in a project, and remediation guidance for a finding.|


### 🧠 Tools Summary
| Agent	   | Tool	                      | Description                                                  |
|----------|----------------------------|--------------------------------------------------------------|
| hello	   | greet(name)	              | Returns a friendly greeting.                                 |
| hello	   | roll_dice(n_dice)          | Rolls N six-sided dice and returns the results.              |
| web_risk | lookup_url(url)	          | Checks a URL against Google’s Web Risk database for threats. |
| scc      | top_vulnerability_findings | Lists top SCC vulnerability findings in a project.           |
| scc      | get_finding_remediation    | Returns remediation guidance for a finding.                  |


### 📁 Directory Structure
```
├── hello/
|   ├── __init__.py
│   ├── agent.py         # Defines the "hello" agent and its tools
│   └── deploy.py        # Deployment script for Agent Engine
├── scc/
|   ├── __init__.py
│   ├── agent.py         # Defines the "scc" agent and its tools
│   └── deploy.py        # Deployment script for Agent Engine
├── web_risk/
|   ├── __init__.py
│   ├── agent.py         # Defines the "web_risk" agent and its tools
│   └── deploy.py        # Deployment script for Agent Engine
├── .env.example         # Environment variable template
├── pyproject.toml       # Poetry project definition
└── README.md
```

### ⚙️ Environment Configuration
Copy `.env.example` to `.env` in the respective folders, and fill in your configuration:
```
# Option 1: Gemini API Key (for local development)
GOOGLE_GENAI_USE_VERTEXAI=False
GOOGLE_API_KEY="your-google-api-key"

# Option 2: Vertex AI (for Google Cloud deployment)
GOOGLE_GENAI_USE_VERTEXAI=True
GOOGLE_CLOUD_PROJECT="your-project-id"
GOOGLE_CLOUD_LOCATION="your-location"
GOOGLE_CLOUD_STORAGE_BUCKET="your-storage-bucket"
```
Note: For Vertex AI deployments, make sure your active Google Cloud credentials have `Vertex AI Admin` and `Storage Admin` roles.


### 🚀 Deploy to Vertex AI Agent Engine
Use `poetry` to install necessary pre-requisites.
```
pip install poetry
poetry lock
poetry install --with deployment
```

You can deploy each agent directly to Vertex AI Agent Engine.
```
python -m hello.deploy
python -m scc.deploy
python -m web_risk.deploy
```

A successful deployment will result in:
```
✅ Deployed agent: projects/<PROJECT_NUMBER>/locations/<LOCATION>/reasoningEngines/<AGENT_ID>
```


### 🌐 Publish to Gemini Enterprise
After deployment, you can publish your registered ADK agents to Gemini Enterprise using the [Agent Registration Tool](https://github.com/VeerMuchandi/agent_registration_tool).

1️⃣ Clone the registration tool
```
git clone https://github.com/VeerMuchandi/agent_registration_tool
cd agent_registration_tool
```

2️⃣ List deployed agents
```
python as_registry_client.py list_deployed_agents \
  --project_id "gcp-project-id-from-config" \
  --location "location-from-config"
```

3️⃣ Create registration configs for each agent. Either use default `config.json` or `--config` to specify a different path. Example below
```
nano config_hello.json
```
```
{
    "project_id": "gcp-project-id-from-config",
    "location": "location-from-config", 
    "app_id": "agentspace-app-id",
    "ars_display_name": "agent-display-name-for-registry",
    "description": "agent-description-for-registry",
    "tool_description": "tool-description-for-registry",
    "adk_deployment_id": "reasoning-engine-id-from-agent-engine",
    "auth_id": "oauth-auth-id-if-any",
    "api_location": "agentspace-app-location",
    "re_location": "reasoning-engine-location"
}
```
Note: If reasoning engine is `projects/PROJECT_ID/locations/LOCATION/reasoningEngines/RE_ID`, then `adk_deployment_id` is `RE_ID`.

4️⃣ Register the agents. If successful, your agents will be visible and callable within Gemini Enterprise.
```
python as_registry_client.py register_agent --config=config_hello.json
python as_registry_client.py register_agent --config=config_scc.json
python as_registry_client.py register_agent --config=config_webrisk.json
```
