## 🤖 Agent Identity Demo
This project deploys a minimal Gemini-powered agent to Vertex AI Agent Engine using the secure **Agent Identity** principal (`IdentityType.AGENT_IDENTITY`), rather than a traditional Service Account.

### 🛠️ Setup
1. Install dependencies
```
pip install google-cloud-aiplatform google-adk python-dotenv absl-py
```

2. Create `.env` file (or copy from the repo root) in the `agent_id` directory with the following variables.
```
GOOGLE_GENAI_USE_VERTEXAI=True
GOOGLE_CLOUD_PROJECT="your-project-id"
GOOGLE_CLOUD_LOCATION="your-region"
GOOGLE_CLOUD_STORAGE_BUCKET="your-storage-bucket"
GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY=True
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=True
```

### 🚀 Deployment
From the same directory as `agent_id`, run the deployment script:
```
python -m agent_id.deploy
```

The script will output the deployed Agent Name. Copy this value for the next step.

`✅ Deployed agent: projects/.../locations/.../reasoningEngines/AGENT_ENGINE_ID`


### 🔐 Post-Deployment: Grant Permissions
Unlike Service Accounts, Agent Identity starts with zero permissions (least privilege). You must grant the agent permission to run inference and use project quotas. Required roles:
* `roles/aiplatform.expressUser` (Access memory/sessions/inference)
* `roles/serviceusage.serviceUsageConsumer` (Use project quota)
  
Replace `AGENT_ENGINE_ID`, `PROJECT_NUMBER`, `PROJECT_ID`, `LOCATION`, and `ORG_ID` as applicable in the commands below.
```
export PRINCIPAL="principal://agents.global.org-ORG_ID.system.id.goog/resources/aiplatform/projects/PROJECT_NUMBER/locations/LOCATION/reasoningEngines/AGENT_ENGINE_ID"

gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="$PRINCIPAL" \
    --role="roles/aiplatform.expressUser"

gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="$PRINCIPAL" \
    --role="roles/serviceusage.serviceUsageConsumer"
```

### 🧪 Testing
Once permissions are granted (allow ~1 minute for propagation), you can interact with the agent using the Vertex AI SDK or Cloud Console.
