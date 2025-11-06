"""Pydantic schemas for request/response validation"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


# Email action schemas
class EmailActionBase(BaseModel):
    recipient_email: EmailStr
    recipient_name: Optional[str] = None
    action_type: str
    reason: str
    emoji: Optional[str] = None
    draft_subject: Optional[str] = None
    draft_content: str


class EmailActionCreate(EmailActionBase):
    priority_score: Optional[int] = 0
    source_thread_id: Optional[str] = None
    source_message_id: Optional[str] = None
    last_interaction_date: Optional[datetime] = None


class EmailActionResponse(EmailActionBase):
    id: int
    user_id: int
    priority_score: int
    is_sent: bool
    sent_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Analysis response
class InboxAnalysisResponse(BaseModel):
    actions: List[EmailActionResponse]
    total_count: int


# Draft generation request
class DraftGenerateRequest(BaseModel):
    recipient_email: EmailStr
    recipient_name: Optional[str] = None
    action_type: str
    context: Optional[str] = None
    last_interaction: Optional[str] = None
    signal: Optional[str] = None


class DraftGenerateResponse(BaseModel):
    subject: str
    body: str
    action_type: str


# OAuth callback
class GoogleAuthCallback(BaseModel):
    code: str
    state: Optional[str] = None
