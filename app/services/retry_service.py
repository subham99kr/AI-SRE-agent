from sqlalchemy.orm import Session

from app.database.session import SessionLocal

from app.storage.incident_repository import (
    IncidentRepository
)


class RetryService:

    def create_retry(
        self,
        incident_id: str
    ) -> dict | None:

        db: Session = SessionLocal()

        try:

            repo = IncidentRepository(db)

            incident = repo.get(
                incident_id
            )

            if incident is None:

                return None

            root_id = (
                incident.root_incident_id
            )

            next_attempt = (
                repo.get_next_attempt_number(
                    root_id
                )
            )

            return {

                "namespace":
                incident.namespace,

                "deployment":
                incident.deployment,

                "root_incident_id":
                root_id,

                "attempt_number":
                next_attempt,
                
                "retry": True

            }

        finally:

            db.close()