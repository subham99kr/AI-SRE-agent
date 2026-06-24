from sqlalchemy import func

from app.database.incident import Incident


class IncidentGroupRepository:

    def __init__(self, db):

        self.db = db

    def get_groups(self):

        rows = (

            self.db.query(

                Incident.root_incident_id,

                Incident.namespace,

                Incident.deployment,

                func.count(
                    Incident.id
                ).label(
                    "attempt_count"
                ),

                func.max(
                    Incident.created_at
                ).label(
                    "latest_created_at"
                )

            )

            .filter(
                Incident.root_incident_id.isnot(None)
            )

            .group_by(

                Incident.root_incident_id,

                Incident.namespace,

                Incident.deployment

            )

            .order_by(

                func.max(
                    Incident.created_at
                ).desc()

            )

            .all()

        )

        return rows