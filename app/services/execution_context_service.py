from sqlalchemy.orm import Session

from app.database.session import SessionLocal

from app.storage.incident_repository import IncidentRepository
from app.storage.evidence_repository import EvidenceRepository
from app.storage.remediation_repository import RemediationRepository


class ExecutionContextService:

    def load(
        self,
        incident_id: str
    ):

        db: Session = SessionLocal()

        try:

            incident_repo = IncidentRepository(db)
            evidence_repo = EvidenceRepository(db)
            remediation_repo = RemediationRepository(db)

            incident = incident_repo.get(
                incident_id
            )

            if incident is None:

                return None

            evidence = evidence_repo.get(
                incident_id
            )

            remediation = remediation_repo.get(
                incident_id
            )

            return {

                "incident": incident,

                "evidence": evidence,

                "remediation": remediation

            }

        finally:

            db.close()