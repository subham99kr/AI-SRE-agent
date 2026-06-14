from sqlalchemy import (
    String,
    Boolean,
    ForeignKey,
)

from sqlalchemy.dialects.postgresql import (
    JSONB,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import Base


class Verification(Base):

    __tablename__ = "incident_verification"

    incident_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("incidents.id"),
        primary_key=True
    )

    success: Mapped[bool] = mapped_column(
        Boolean
    )

    message: Mapped[str] = mapped_column(
        String(500)
    )

    checks: Mapped[list] = mapped_column(
        JSONB
    )