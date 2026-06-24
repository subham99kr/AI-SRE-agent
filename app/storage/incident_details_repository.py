from sqlalchemy.orm import joinedload

from app.database.incident import Incident
from app.database.evidence import Evidence
from app.database.remediation import Remediation
from app.database.execution import Execution
from app.database.verification import Verification
from app.database.report import Report


class IncidentDetailsRepository:

    def __init__(self, db):

        self.db = db

    def get(
        self,
        incident_id: str
    ):

        return (

            self.db.query(

                Incident,
                Evidence,
                Remediation,
                Execution,
                Verification,
                Report

            )

            .outerjoin(

                Evidence,
                Evidence.incident_id == Incident.id

            )

            .outerjoin(

                Remediation,
                Remediation.incident_id == Incident.id

            )

            .outerjoin(

                Execution,
                Execution.incident_id == Incident.id

            )

            .outerjoin(

                Verification,
                Verification.incident_id == Incident.id

            )

            .outerjoin(

                Report,
                Report.incident_id == Incident.id

            )

            .filter(
                Incident.id == incident_id
            )

            .first()

        )