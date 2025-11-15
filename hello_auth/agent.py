import os
import dotenv
import requests
from google.adk.agents import Agent

dotenv.load_dotenv()

# OAuth Proxy URL (local or deployed on Railway)
OAUTH_PROXY_URL = os.getenv("OAUTH_PROXY_URL", "http://localhost:5000")

# API key for programmatic access (optional, for CLI/server usage)
OAUTH_PROXY_API_KEY = os.getenv("OAUTH_PROXY_API_KEY")

def get_access_token() -> dict:
    """Get access token from OAuth Proxy.
    
    Returns:
        dict with 'access_token' and 'provider', or None if not authenticated
    """
    if not OAUTH_PROXY_API_KEY:
        print("Error: OAUTH_PROXY_API_KEY not set")
        return None
    
    headers = {'X-API-Key': OAUTH_PROXY_API_KEY}
    
    try:
        response = requests.get(
            f"{OAUTH_PROXY_URL}/api/token",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            print("OAuth Proxy: Not authenticated or invalid API key")
            return None
        else:
            print(f"OAuth Proxy error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Failed to connect to OAuth Proxy: {e}")
    
    return None

def get_github_access_token() -> str:
    """Get GitHub access token from OAuth Proxy.
    
    Returns:
        Access token string or None if not authenticated
    """
    token_data = get_access_token()
    
    if token_data and token_data.get('access_token'):
        return token_data['access_token']
    
    return None

def greet_github_user() -> str:
    """Greets the authenticated GitHub user by name and email.
    
    Returns:
        A personalized greeting including username and email (if available).
    """
    access_token = get_github_access_token()
    
    if not access_token:
        return f"❌ Not authenticated. Visit {OAUTH_PROXY_URL} to login and get access token."
    
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        user_response = requests.get("https://api.github.com/user", headers=headers)
        if user_response.status_code != 200:
            return f"❌ Failed to retrieve GitHub user info: {user_response.text}"
        
        user = user_response.json()
        username = user.get("login", "unknown user")
        email = user.get("email")
        
        if not email:
            email_response = requests.get("https://api.github.com/user/emails", headers=headers)
            if email_response.status_code == 200:
                emails = email_response.json()
                primary = next((e for e in emails if e.get("primary")), None)
                email = primary.get("email") if primary else None
        
        if email:
            return f"Hello, {username} ({email})! 👋"
        return f"Hello, {username}! 👋"
    
    except Exception as e:
        return f"❌ Error connecting to GitHub: {str(e)}"

root_agent = Agent(
    name="hello_auth",
    model="gemini-2.5-flash",
    instruction="You are an AI assistant designed to greet users.",
    tools=[greet_github_user],
)
