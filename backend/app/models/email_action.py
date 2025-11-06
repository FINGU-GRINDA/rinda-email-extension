"""Email action database model"""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class EmailAction(Base):
    """Email action model for storing recommended follow-up actions"""

    __tablename__ = "email_actions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Recipient information
    recipient_email = Column(String(255), nullable=False)
    recipient_name = Column(String(255), nullable=True)

    # Action details
    action_type = Column(String(50), nullable=False)  # follow_up, thank_you, new_opportunity
    reason = Column(Text, nullable=False)
    emoji = Column(String(10), nullable=True)

    # Draft content
    draft_subject = Column(String(500), nullable=True)
    draft_content = Column(Text, nullable=False)

    # Metadata
    priority_score = Column(Integer, default=0)  # For ranking actions
    is_sent = Column(Boolean, default=False)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Source email context
    source_thread_id = Column(String(255), nullable=True)
    source_message_id = Column(String(255), nullable=True)
    last_interaction_date = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="email_actions")

    def __repr__(self):
        return f"<EmailAction(id={self.id}, recipient={self.recipient_email}, type={self.action_type})>"
