from sqlalchemy import select

from app.database.evidence import Evidence

from app.storage.base_repository import (
    BaseRepository
)


class EvidenceRepository(BaseRepository):

    def create(
        self,
        evidence: Evidence
    ) -> Evidence:

        self.add(
            evidence
        )

        return evidence

    def get(
        self,
        incident_id: str
    ) -> Evidence | None:

        statement = select(
            Evidence
        ).where(
            Evidence.incident_id == incident_id
        )

        return self.db.scalar(
            statement
        )