"""Services package"""

from app.services.auth import create_access_token, verify_token, get_or_create_user
from app.services.google_oauth import get_authorization_url, exchange_code_for_tokens
from app.services.gmail_api import get_recent_emails, analyze_email_interactions
from app.services.llm import generate_email_draft
from app.services.rate_limiter import rate_limiter

__all__ = [
    "create_access_token",
    "verify_token",
    "get_or_create_user",
    "get_authorization_url",
    "exchange_code_for_tokens",
    "get_recent_emails",
    "analyze_email_interactions",
    "generate_email_draft",
    "rate_limiter"
]
