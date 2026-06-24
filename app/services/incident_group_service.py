from app.database.session import SessionLocal

from app.storage.incident_group_repository import (
    IncidentGroupRepository
)

from app.database.incident import Incident


class IncidentGroupService:

    def get_groups(self):

        db = SessionLocal()

        try:

            repo = IncidentGroupRepository(
                db
            )

            groups = repo.get_groups()

            result = []

            for group in groups:

                latest = (

                    db.query(
                        Incident
                    )

                    .filter(
                        Incident.root_incident_id
                        ==
                        group.root_incident_id
                    )

                    .order_by(
                        Incident.created_at.desc()
                    )

                    .first()

                )

                result.append({

                    "root_incident_id":
                    group.root_incident_id,

                    "namespace":
                    group.namespace,

                    "deployment":
                    group.deployment,

                    "attempt_count":
                    group.attempt_count,

                    "latest_status":
                    latest.status,

                    "latest_created_at":
                    latest.created_at

                })

            return result

        finally:

            db.close()