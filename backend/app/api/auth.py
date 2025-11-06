"""Authentication API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import Token, UserResponse, GoogleAuthCallback
from app.services.auth import create_access_token, get_or_create_user, update_user_tokens
from app.services.google_oauth import (
    get_authorization_url,
    exchange_code_for_tokens,
    get_user_info
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.get("/google")
async def google_auth():
    """Initiate Google OAuth flow"""
    try:
        authorization_url, state = get_authorization_url()

        return {
            "authorization_url": authorization_url,
            "state": state
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OAuth initialization failed: {str(e)}"
        )


@router.get("/google/callback")
async def google_auth_callback(
    code: str,
    state: str | None = None,
    db: Session = Depends(get_db)
):
    """Handle Google OAuth callback"""
    try:
        # Exchange code for tokens
        tokens = exchange_code_for_tokens(code, state)

        # Get user info
        user_info = get_user_info(tokens["access_token"])
        email = user_info["email"]

        # Create or get user
        user = get_or_create_user(db, email)

        # Store Gmail tokens
        update_user_tokens(
            db,
            user.id,
            tokens["access_token"],
            tokens.get("refresh_token"),
            tokens.get("token_expiry")
        )

        # Create JWT token
        access_token = create_access_token(data={"sub": email})

        # Redirect to extension with token
        # In production, you'd redirect to your extension or web app
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OAuth callback failed: {str(e)}"
        )


@router.post("/token", response_model=Token)
async def create_token(
    callback_data: GoogleAuthCallback,
    db: Session = Depends(get_db)
):
    """Exchange authorization code for JWT token (for extension use)"""
    try:
        # Exchange code for tokens
        tokens = exchange_code_for_tokens(callback_data.code, callback_data.state)

        # Get user info
        user_info = get_user_info(tokens["access_token"])
        email = user_info["email"]

        # Create or get user
        user = get_or_create_user(db, email)

        # Store Gmail tokens
        update_user_tokens(
            db,
            user.id,
            tokens["access_token"],
            tokens.get("refresh_token"),
            tokens.get("token_expiry")
        )

        # Create JWT token
        access_token = create_access_token(data={"sub": email})

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token creation failed: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    token: str,
    db: Session = Depends(get_db)
):
    """Get current user info"""
    from app.services.auth import verify_token
    from app.models.user import User

    token_data = verify_token(token)
    user = db.query(User).filter(User.email == token_data["email"]).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
