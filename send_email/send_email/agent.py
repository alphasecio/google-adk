import os
import dotenv
import resend
from google.adk.agents import Agent

dotenv.load_dotenv()

def send_email(recipient: str, subject: str, body: str) -> str:
    """Sends an email using the Resend service.

    Args:
        recipient: The email address of the recipient.
        subject: The subject line of the email.
        body: The HTML or plain text body of the email.

    Returns:
        A string indicating the success or failure of the email attempt.
    """
        
    try:
        resend.api_key = os.getenv("RESEND_API_KEY")
        sender_email = os.getenv("RESEND_FROM_EMAIL") 
        
        email = resend.Emails.send({
            "from": sender_email,
            "to": [recipient],
            "subject": subject,
            "html": f"<strong>{body}</strong>",
            "text": f"{body}"
        })
        return f"Email sent successfully to {email['id']}."
    except Exception as e:
        return f"Error sending email: {e}"

root_agent = Agent(
    name="hello",
    model="gemini-2.5-flash",
    instruction="You are an AI assistant designed to send emails.",
    tools=[send_email],
)
