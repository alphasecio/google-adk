# Hello Agent

A Google ADK agent demonstrating real-time prompt inspection using Google Cloud Model Armor.

## Overview

This agent integrates Model Armor's content safety filters via `before_model_callback` to inspect user prompts before they reach the LLM. Unsafe content is blocked with detailed violation feedback while maintaining session continuity.

## Features

- **Responsible AI Filters**: Detects sexually explicit, hate speech, harassment, and dangerous content with confidence levels
- **Prompt Injection Protection**: Blocks jailbreak attempts and system prompt manipulation
- **Sensitive Data Detection**: Identifies sensitive data (Govt IDs, Passports, credit cards, emails, phone nos, IPs)
- **Malicious URI Detection**: Flags known malicious domains using Google Safe Browsing
- **CSAM Detection**: Screens for child safety concerns
- **Seamless UX**: Blocked messages don't terminate sessions—users can rephrase and continue

## Setup

1. **Clone and navigate**:
   ```bash
   git clone https://github.com/alphasecio/google-adk.git
   cd google-adk/hello
   ```

2. **Install dependencies**:
   ```bash
   pip install google-adk google-cloud-model-armor python-dotenv
   ```

3. **Configure environment**:
   Create `.env` file:
   ```bash
   GOOGLE_CLOUD_PROJECT=your-project-id
   GOOGLE_CLOUD_LOCATION=your-location
   MODEL_ARMOR_TEMPLATE_ID=your-template-id
   ```

4. **Enable Data Loss Prevention and Model Armor APIs**:
   ```bash
   gcloud services enable dlp.googleapis.com modelarmor.googleapis.com --project=YOUR_PROJECT_ID
   ```

5. **Grant IAM permissions**:
   ```bash
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
   --member="serviceAccount:service-PROJECT_NUMBER@gcp-sa-aiplatform-re.iam.gserviceaccount.com" \
   --role="roles/modelarmor.user"
   ```

6. **Create Sensitive Data Protection template**
   * Inspection for built-in infoTypes:  Govt IDs, Passports, credit cards, emails, phone numbers, IP addresses

7. **Create Model Armor template**: `ma-all-med`
   * Malicious URL detection: Enabled
   * Prompt injection and jailbreak detection: Enabled
     * Confidence level: Medium and above 
   * Sensitive data protection template: Enabled
     * Detection type: Advanced
     * Inspection template: SDP template ID
   * Responsible AI: Enabled
     * Hate speech: Medium and above
     * Dangerous: Medium and above
     * Sexually explicit: Medium and above
     * Harassment: Medium and above 

## Usage

### Local Testing
```bash
adk web
```

Navigate to `http://127.0.0.1:8000` and interact with the agent.

### Deployment

Deploy to Vertex AI Agent Engine:
```bash
adk deploy --project=YOUR_PROJECT_ID --location=us-central1
```

Access via:
- **Agent Engine Playground**: Cloud Console → Vertex AI → Agent Engine → Your Agent → Playground
- **Gemini Enterprise App**: Publish to Gemini Enterprise and access via vertexaisearch.cloud.google.com/u/xxx → Your Agent
