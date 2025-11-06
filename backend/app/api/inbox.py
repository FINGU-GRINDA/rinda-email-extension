"""Inbox analysis API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import InboxAnalysisResponse, EmailActionResponse, EmailActionCreate
from app.services.auth import verify_token
from app.services.gmail_api import get_recent_emails, analyze_email_interactions
from app.services.llm import generate_email_draft
from app.models.user import User
from app.models.email_action import EmailAction
from datetime import datetime

router = APIRouter(prefix="/api/inbox", tags=["Inbox"])


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


@router.get("/analyze", response_model=InboxAnalysisResponse)
async def analyze_inbox(
    user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Analyze user's inbox and return top 3 recommended actions"""

    if not user.gmail_token:
        raise HTTPException(
            status_code=400,
            detail="Gmail not connected. Please authenticate with Google."
        )

    try:
        # Fetch recent emails from Gmail
        recent_emails = get_recent_emails(user.gmail_token, max_results=50)

        if not recent_emails:
            # Return empty results if no emails
            return {
                "actions": [],
                "total_count": 0
            }

        # Analyze for follow-up opportunities
        opportunities = analyze_email_interactions(recent_emails)

        # Store top 3 opportunities in database and generate drafts
        actions = []
        for opp in opportunities[:3]:
            # Generate draft
            draft = generate_email_draft(
                recipient_name=opp["recipient_name"],
                action_type=opp["action_type"],
                context=f"Previous email about: {opp.get('subject', 'our conversation')}",
                last_interaction=f"{opp.get('last_interaction', 'recently')}",
                signal=opp["reason"]
            )

            # Create action in database
            action = EmailAction(
                user_id=user.id,
                recipient_email=opp["recipient_email"],
                recipient_name=opp["recipient_name"],
                action_type=opp["action_type"],
                reason=opp["reason"],
                emoji=opp["emoji"],
                draft_subject=draft["subject"],
                draft_content=draft["body"],
                priority_score=opp["priority_score"],
                source_thread_id=opp.get("thread_id"),
                source_message_id=opp.get("message_id"),
                last_interaction_date=opp.get("last_interaction")
            )

            db.add(action)
            db.flush()  # Get ID without committing
            actions.append(action)

        db.commit()

        # Refresh to get full objects
        for action in actions:
            db.refresh(action)

        return {
            "actions": actions,
            "total_count": len(actions)
        }

    except Exception as e:
        db.rollback()
        print(f"Error analyzing inbox: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze inbox: {str(e)}"
        )


@router.get("/actions", response_model=List[EmailActionResponse])
async def get_saved_actions(
    user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get user's saved email actions"""

    actions = db.query(EmailAction).filter(
        EmailAction.user_id == user.id,
        EmailAction.is_sent == False
    ).order_by(
        EmailAction.priority_score.desc()
    ).limit(limit).all()

    return actions


@router.post("/actions/{action_id}/mark-sent")
async def mark_action_sent(
    action_id: int,
    user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Mark an action as sent"""

    action = db.query(EmailAction).filter(
        EmailAction.id == action_id,
        EmailAction.user_id == user.id
    ).first()

    if not action:
        raise HTTPException(status_code=404, detail="Action not found")

    action.is_sent = True
    action.sent_at = datetime.utcnow()
    db.commit()

    return {"success": True, "message": "Action marked as sent"}
