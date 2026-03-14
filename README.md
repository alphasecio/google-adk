# Google ADK
Sample Google Agent Development Kit ([ADK](https://google.github.io/adk-docs/)) agents with callable tools. Each agent can be deployed to [Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview), and published to [Gemini Enterprise](https://cloud.google.com/gemini-enterprise?hl=en) (previously Agentspace).


### 🤖 Agent Summary
| Agent            | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| agent_id         | Deploys a simple agent with Agent Identity principal (preview)              |
| hello            | Greets users and rolls dice using Python functions.                         |
| scc              | Lists top SCC findings in a project, and remediation guidance for a finding.|
| web_risk         | Detects malware, phishing, and unwanted software URLs using Web Risk API.   |
| security_manager | Multi-agent security manager (includes SCC and Web Risk agents)             |
| secret_agent     | Retrieves secrets from Secret Manager bound as environment variables        |

### ⚙️ Environment Configuration
Copy `.env.example` to `.env` in the respective agent sub-folders, and fill in your configuration:
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

Navigate to each agent folder and deploy:
```
cd hello && python deploy.py
cd ../scc && python deploy.py
cd ../web_risk && python deploy.py
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
