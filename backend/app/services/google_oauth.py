"""Google OAuth 2.0 service"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from app.config import settings


# OAuth 2.0 scopes for Gmail API
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid'
]


def create_oauth_flow() -> Flow:
    """Create Google OAuth flow"""
    client_config = {
        "web": {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [settings.GOOGLE_REDIRECT_URI]
        }
    }

    flow = Flow.from_client_config(
        client_config=client_config,
        scopes=SCOPES,
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )

    return flow


def get_authorization_url() -> tuple[str, str]:
    """Get OAuth authorization URL and state"""
    flow = create_oauth_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )

    return authorization_url, state


def exchange_code_for_tokens(code: str, state: str) -> dict:
    """Exchange authorization code for tokens"""
    flow = create_oauth_flow()
    flow.fetch_token(code=code)

    credentials = flow.credentials

    return {
        "access_token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_expiry": credentials.expiry,
        "scopes": credentials.scopes
    }


def get_gmail_service(access_token: str):
    """Create Gmail API service client"""
    credentials = Credentials(token=access_token)
    service = build('gmail', 'v1', credentials=credentials)
    return service


def get_user_info(access_token: str) -> dict:
    """Get user info from Google"""
    credentials = Credentials(token=access_token)
    service = build('oauth2', 'v2', credentials=credentials)
    user_info = service.userinfo().get().execute()

    return {
        "email": user_info.get("email"),
        "name": user_info.get("name"),
        "picture": user_info.get("picture")
    }
