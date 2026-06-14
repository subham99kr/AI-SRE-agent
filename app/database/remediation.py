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


class Remediation(Base):

    __tablename__ = "incident_remediation"

    incident_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("incidents.id"),
        primary_key=True
    )

    risk: Mapped[str] = mapped_column(
        String(20)
    )

    rollback_available: Mapped[bool] = mapped_column(
        Boolean
    )

    steps: Mapped[list] = mapped_column(
        JSONB
    )