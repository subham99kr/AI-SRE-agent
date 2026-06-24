from sqlalchemy import (
    String,
    Text,
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


class Report(Base):

    __tablename__ = "incident_report"

    incident_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("incidents.id"),
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        Text
    )

    executive_summary: Mapped[str] = mapped_column(
        Text
    )

    technical_summary: Mapped[str] = mapped_column(
        Text
    )

    overall_status: Mapped[str] = mapped_column(
        Text
    )

    recommendations: Mapped[list] = mapped_column(
        JSONB
    )