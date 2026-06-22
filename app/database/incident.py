import uuid

from datetime import datetime

from sqlalchemy import (
    String,
    Float,
    Boolean,
    DateTime,
    Integer,
    func,
    Text
)
from typing import Optional

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import Base


class Incident(Base):

    __tablename__ = "incidents"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    namespace: Mapped[str] = mapped_column(
        String(100)
    )

    deployment: Mapped[str] = mapped_column(
        String(100)
    )

    incident_type: Mapped[str] = mapped_column(
        String(100)
    )

    root_cause: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    confidence: Mapped[float] = mapped_column(
        Float
    )

    risk: Mapped[str] = mapped_column(
        String(20)
    )

    action_required = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    action_reason = mapped_column(
        Text,
        nullable=False,
        default=""
    )

    requires_approval: Mapped[bool] = mapped_column(
        Boolean
    )

    rollback_available: Mapped[bool] = mapped_column(
        Boolean
    )

    verification_success: Mapped[bool] = mapped_column(
        Boolean
    )

    verification_message: Mapped[str] = mapped_column(
        String(500)
    )
    status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING_APPROVAL"
    )
    
    approval_status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING"
    )

    approval_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    approved_by: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

        #
    # Retry Tracking
    #

    root_incident_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        nullable=True,
        index=True
    )

    attempt_number: Mapped[int] = mapped_column(
        default=1
    )

    operator_feedback: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True
    )

    feedback_by: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    feedback_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    

    # approved_at i will implement later
