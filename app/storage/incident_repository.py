from sqlalchemy import select, delete

from app.database.incident import Incident

from app.storage.base_repository import (
    BaseRepository
)


class IncidentRepository(BaseRepository):

    def create(
        self,
        incident: Incident
    ) -> Incident:

        self.add(
            incident
        )

        return incident

    def get(
        self,
        incident_id: str
    ) -> Incident | None:

        statement = select(
            Incident
        ).where(
            Incident.id == incident_id
        )

        return self.db.scalar(
            statement
        )

    def list_incidents(self) -> list[Incident]:

        statement = (
            select(Incident)
            .order_by(
                Incident.created_at.desc()
            )
        )

        return list(
            self.db.scalars(statement)
        )

    def delete(
        self,
        incident_id: str
    ):

        statement = delete(
            Incident
        ).where(
            Incident.id == incident_id
        )

        self.db.execute(statement)

    def latest(
        self,
        limit: int = 10
    ) -> list[Incident]:

        statement = (
            select(
                Incident
            )
            .order_by(
                Incident.created_at.desc()
            )
            .limit(limit)
        )

        return list(
            self.db.scalars(statement)
        )

    def filter_by_type(
        self,
        incident_type: str
    ) -> list[Incident]:

        statement = (
            select(
                Incident
            )
            .where(
                Incident.incident_type
                == incident_type
            )
            .order_by(
                Incident.created_at.desc()
            )
        )

        return list(
            self.db.scalars(statement)
        )
    
    def update(
        self,
        incident: Incident
    ) -> Incident:

        self.db.merge(
            incident
        )

        return incident