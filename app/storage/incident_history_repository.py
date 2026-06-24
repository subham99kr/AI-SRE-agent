from app.database.incident import Incident


class IncidentHistoryRepository:

    def __init__(self, db):

        self.db = db

    def get_attempts(
        self,
        root_incident_id: str
    ):

        return (

            self.db.query(
                Incident
            )

            .filter(
                Incident.root_incident_id
                ==
                root_incident_id
            )

            .order_by(
                Incident.created_at.desc()
            )

            .all()

        )