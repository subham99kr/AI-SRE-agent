#This table will store the raw Kubernetes evidence collected during the investigation.

from sqlalchemy import (
    String,
    ForeignKey,
)

from sqlalchemy.dialects.postgresql import (
    JSONB,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import (
    Base,
)


class Evidence(Base):

    __tablename__ = "incident_evidence"

    incident_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("incidents.id"),
        primary_key=True,
    )

    deployment_spec: Mapped[dict] = mapped_column(
        JSONB
    )

    pods: Mapped[list] = mapped_column(
        JSONB
    )

    events: Mapped[list] = mapped_column(
        JSONB
    )

    logs: Mapped[list] = mapped_column(
        JSONB
    )

    raw_evidence: Mapped[dict] = mapped_column(
        JSONB,
        nullable=True
    )