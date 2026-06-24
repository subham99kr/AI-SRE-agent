from app.database.session import SessionLocal

from app.storage.incident_history_repository import (
    IncidentHistoryRepository
)

from app.storage.evidence_repository import (
    EvidenceRepository
)

from app.storage.remediation_repository import (
    RemediationRepository
)

from app.storage.report_repository import (
    ReportRepository
)

from app.utils.sqlalchemy_utils import (
    model_to_dict
)


class IncidentHistoryService:

    def get_attempts(
        self,
        root_incident_id: str
    ):

        db = SessionLocal()

        try:

            history_repo = (
                IncidentHistoryRepository(db)
            )

            evidence_repo = (
                EvidenceRepository(db)
            )

            remediation_repo = (
                RemediationRepository(db)
            )

            report_repo = (
                ReportRepository(db)
            )

            attempts = (
                history_repo.get_attempts(
                    root_incident_id
                )
            )

            result = []

            for incident in attempts:

                result.append({

                    "incident":
                    model_to_dict(
                        incident
                    ),

                    "evidence":
                    model_to_dict(

                        evidence_repo
                        .get(
                            incident.id
                        )

                    ),

                    "remediation":
                    model_to_dict(

                        remediation_repo
                        .get(
                            incident.id
                        )

                    ),

                    "report":
                    model_to_dict(

                        report_repo
                        .get(
                            incident.id
                        )

                    )

                })

            return result

        finally:

            db.close()