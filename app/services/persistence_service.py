from sqlalchemy.orm import Session

from app.database.session import SessionLocal

from app.database.incident import Incident
from app.database.evidence import Evidence
from app.database.execution import Execution
from app.database.remediation import Remediation
from app.database.verification import Verification
from app.database.report import Report

from app.storage.incident_repository import IncidentRepository
from app.storage.evidence_repository import EvidenceRepository
from app.storage.execution_repository import ExecutionRepository
from app.storage.remediation_repository import RemediationRepository
from app.storage.verification_repository import VerificationRepository
from app.storage.report_repository import ReportRepository


class PersistenceService:

    def save(
        self,
        state: dict
    ):

        db: Session = SessionLocal()

        try:

            incident_repo = IncidentRepository(db)
            evidence_repo = EvidenceRepository(db)
            execution_repo = ExecutionRepository(db)
            remediation_repo = RemediationRepository(db)
            verification_repo = VerificationRepository(db)
            report_repo = ReportRepository(db)

            #
            # Save Incident
            #

            incident = Incident(
                namespace=state["namespace"],
                deployment=state["deployment"],
                incident_type=state["incident_type"],
                root_cause=state["root_cause"],
                confidence=state["confidence"],
                risk=state["risk"],
                requires_approval=state["requires_approval"],
                rollback_available=state["rollback_available"],
                verification_success=state["verification_success"],
                verification_message=state["verification_message"],
            )

            incident_repo.create(incident)

            db.flush()      # <-- Generates UUID before commit

            #
            # Save Evidence
            #

            evidence_repo.create(
                Evidence(
                    incident_id=incident.id,
                    deployment_spec=state["evidence"]["deployment"],
                    pods=state["evidence"]["pods"],
                    events=state["evidence"]["events"],
                    logs=state["evidence"]["logs"],
                )
            )

            #
            # Save Remediation
            #

            remediation_repo.create(
                Remediation(
                    incident_id=incident.id,
                    risk=state["risk"],
                    rollback_available=state["rollback_available"],
                    steps=state["remediation_steps"],
                )
            )

            #
            # Save Verification
            #

            verification_repo.create(
                Verification(
                    incident_id=incident.id,
                    success=state["verification_success"],
                    message=state["verification_message"],
                    checks=state["verification_checks"],
                )
            )

            #
            # Save Execution Results
            #

            for item in state["execution_results"]:

                execution_repo.create(
                    Execution(
                        incident_id=incident.id,
                        step=item["step"],
                        command=item["command"],
                        success=item["success"],
                        stdout=item["stdout"],
                        stderr=item["stderr"],
                    )
                )

            #
            # Save Report
            #

            report = state["incident_report"].model_dump()

            report_repo.create(
                Report(
                    incident_id=incident.id,
                    title=report["title"],
                    executive_summary=report["executive_summary"],
                    technical_summary=report["technical_summary"],
                    overall_status=report["overall_status"],
                    recommendations=report["recommendations"],
                )
            )

            db.commit()

            return incident.id

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()