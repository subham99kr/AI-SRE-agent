import uuid

from sqlalchemy import (
    String,
    Boolean,
    Text,
    ForeignKey,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import Base


class Execution(Base):

    __tablename__ = "incident_execution"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    incident_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("incidents.id")
    )

    step: Mapped[str] = mapped_column(
        String(200)
    )

    command: Mapped[str] = mapped_column(
        Text
    )

    success: Mapped[bool] = mapped_column(
        Boolean
    )

    stdout: Mapped[str] = mapped_column(
        Text
    )

    stderr: Mapped[str] = mapped_column(
        Text
    )