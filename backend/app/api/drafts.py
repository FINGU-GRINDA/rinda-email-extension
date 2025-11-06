"""Email draft generation API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import DraftGenerateRequest, DraftGenerateResponse
from app.services.auth import verify_token
from app.services.llm import generate_email_draft
from app.services.rate_limiter import rate_limiter
from app.models.user import User

router = APIRouter(prefix="/api/drafts", tags=["Drafts"])


async def get_current_user_from_token(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
) -> User:
    """Dependency to get current user from JWT token"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization.replace("Bearer ", "")
    token_data = verify_token(token)

    user = db.query(User).filter(User.email == token_data["email"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/generate", response_model=DraftGenerateResponse)
async def generate_draft(
    request: DraftGenerateRequest,
    user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Generate email draft using AI"""

    # Check rate limit
    rate_limit = rate_limiter.check_rate_limit(user.id)

    if not rate_limit["allowed"]:
        raise HTTPException(
            status_code=429,
            detail={
                "message": f"Daily limit of {rate_limit['max_count']} emails reached",
                "current_count": rate_limit["current_count"],
                "max_count": rate_limit["max_count"],
                "reset_time": rate_limiter.get_reset_time(user.id).isoformat()
            }
        )

    try:
        # Generate draft
        draft = generate_email_draft(
            recipient_name=request.recipient_name or request.recipient_email.split('@')[0],
            action_type=request.action_type,
            context=request.context or "",
            last_interaction=request.last_interaction or "",
            signal=request.signal or ""
        )

        # Increment rate limit counter
        rate_limiter.increment_count(user.id)

        return {
            "subject": draft["subject"],
            "body": draft["body"],
            "action_type": request.action_type
        }

    except Exception as e:
        print(f"Error generating draft: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate draft: {str(e)}"
        )


@router.get("/rate-limit")
async def check_rate_limit(
    user: User = Depends(get_current_user_from_token)
):
    """Check current rate limit status"""

    rate_limit = rate_limiter.check_rate_limit(user.id)

    return {
        "allowed": rate_limit["allowed"],
        "current_count": rate_limit["current_count"],
        "max_count": rate_limit["max_count"],
        "remaining": rate_limit["remaining"],
        "reset_time": rate_limiter.get_reset_time(user.id).isoformat()
    }
