import uuid

from datetime import datetime

from sqlalchemy import (
    String,
    Float,
    Boolean,
    DateTime,
    func,
)

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
        String(500)
    )

    confidence: Mapped[float] = mapped_column(
        Float
    )

    risk: Mapped[str] = mapped_column(
        String(20)
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