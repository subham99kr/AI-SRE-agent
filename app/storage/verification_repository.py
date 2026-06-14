from sqlalchemy import select

from app.database.verification import Verification

from app.storage.base_repository import (
    BaseRepository
)


class VerificationRepository(BaseRepository):

    def create(
        self,
        verification: Verification
    ) -> Verification:

        self.add(
            verification
        )

        return verification

    def get(
        self,
        incident_id: str
    ) -> Verification | None:

        statement = select(
            Verification
        ).where(
            Verification.incident_id == incident_id
        )

        return self.db.scalar(
            statement
        )