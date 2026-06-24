from app.database.session import SessionLocal

from app.storage.incident_details_repository import (
    IncidentDetailsRepository
)

from app.utils.sqlalchemy_utils import (
    model_to_dict
)


class IncidentDetailsService:

    def get(
        self,
        incident_id: str
    ):

        db = SessionLocal()

        try:

            row = (

                IncidentDetailsRepository(db)

                .get(
                    incident_id
                )

            )

            if row is None:

                return None

            (
                incident,
                evidence,
                remediation,
                execution,
                verification,
                report
            ) = row

            return {

                "incident":
                model_to_dict(
                    incident
                ),

                "evidence":
                model_to_dict(
                    evidence
                ),

                "remediation":
                model_to_dict(
                    remediation
                ),

                "execution":
                model_to_dict(
                    execution
                ),

                "verification":
                model_to_dict(
                    verification
                ),

                "report":
                model_to_dict(
                    report
                )

            }

        finally:

            db.close()