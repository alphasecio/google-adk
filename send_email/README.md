# Send Email Agent
 
A Google ADK agent that sends emails using the [Resend](https://resend.com) API.
 
## Overview
 
This agent provides email sending capabilities through a simple natural language interface. Users can compose and send emails by describing what they want to send.
 
## Features
 
- **Email Composition**: Natural language email composition
- **Resend Integration**: Uses Resend API for reliable email delivery
- **HTML & Plain Text**: Sends both HTML and plain text versions
 
## Setup
 
1. **Clone and navigate**:
   ```
   git clone https://github.com/alphasecio/google-adk.git
   cd google-adk/send_email
   ```
 
2. **Install dependencies**:
   ```
   pip install google-adk resend python-dotenv
   ```
 
3. **Get Resend API key**:
   - Sign up at [resend.com](https://resend.com)
   - Verify your sending domain
   - Generate an API key
 
4. **Configure environment**:

   Copy `.env.example` to `.env` from the `agent_id` root folder to the `agent_id` agent folder directory, and update as necessary.
   ```
   GOOGLE_GENAI_USE_VERTEXAI=True
   GOOGLE_CLOUD_PROJECT="your-project-id"
   GOOGLE_CLOUD_LOCATION="your-region"
  
   GOOGLE_CLOUD_STORAGE_BUCKET="your-storage-bucket"
   GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY=True
   OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=True

   RESEND_API_KEY=your-resend-api-key
   RESEND_FROM_EMAIL=noreply@yourdomain.com
   ```
 
## Usage
 
### Local Testing
```
adk web
```
 
Navigate to `http://127.0.0.1:8000` and try:
- "Send an email to user@example.com with subject 'Hello' and body 'This is a test'"
 
### Deployment
 
Deploy to Vertex AI Agent Engine:
```
python deploy.py
```
 
Access via:
- **Agent Engine Playground**: Cloud Console → Vertex AI → Agent Engine → Your Agent → Playground
- **Gemini Enterprise App**: Publish to Gemini Enterprise and access via vertexaisearch.cloud.google.com/u/xxx → Your Agent
