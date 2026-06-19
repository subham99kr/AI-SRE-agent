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
    
    def get_attempts(
        self,
        root_incident_id: str
    ) -> list[Incident]:

        statement = (

            select(
                Incident
            )

            .where(
                Incident.root_incident_id
                == root_incident_id
            )

            .order_by(
                Incident.attempt_number
            )

        )

        return list(
            self.db.scalars(statement)
        )
    
    def get_attempts_by_root(
        self,
        root_incident_id: str,
        limit: int = 5
    ) -> list[Incident]:

        statement = (

            select(
                Incident
            )

            .where(
                Incident.root_incident_id
                == root_incident_id
            )

            .order_by(
                Incident.attempt_number.asc()
            )

        )

        incidents = list(
            self.db.scalars(statement)
        )
        incidents.reverse()
        return incidents
    
    def get_next_attempt_number(
        self,
        root_incident_id: str
    ) -> int:

        attempts = self.get_attempts(
            root_incident_id
        )

        if not attempts:

            return 1

        return (
            attempts[-1].attempt_number
            + 1
        )
    
    def reject(
        self,
        incident: Incident
    ) -> Incident:

        self.db.merge(
            incident
        )

        return incident