from sqlalchemy import select

from app.database.execution import Execution

from app.storage.base_repository import (
    BaseRepository
)


class ExecutionRepository(BaseRepository):

    def create(
        self,
        execution: Execution
    ) -> Execution:

        self.add(
            execution
        )

        return execution

    def get_by_incident(
        self,
        incident_id: str
    ) -> list[Execution]:

        statement = select(
            Execution
        ).where(
            Execution.incident_id == incident_id
        )

        return list(
            self.db.scalars(
                statement
            )
        )