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
                action_required=state["action_required"],
                action_reason=state["action_reason"],
                confidence=state["confidence"],
                risk=state["risk"],
                requires_approval=state["requires_approval"],
                rollback_available=state["rollback_available"],
                status=state["status"],
                approval_status=state["approval_status"],
                approval_reason=state["approval_reason"],
                approved_by=None,
                verification_success=False,
                verification_message="Waiting for execution.",
                # remediation_reasoning=state["remediation_reasoning"],
            )

            incident_repo.create(incident)

            db.flush()

            #
            # First incident becomes its own root
            #

            #
            # Root incident or retry
            #

            if state.get(
                "root_incident_id"
            ):

                incident.root_incident_id = (
                    state["root_incident_id"]
                )

                incident.attempt_number = (
                    state["attempt_number"]
                )

            else:

                incident.root_incident_id = (
                    incident.id
                )

                incident.attempt_number = 1

            #
            # Save Evidence
            #

            evidence_repo.create(
                Evidence(
                    incident_id=incident.id,

                    deployment_spec=state["evidence"].get(
                        "deployment",
                        {}
                    ),

                    pods=state["evidence"].get(
                        "pods",
                        []
                    ),

                    events=state["evidence"].get(
                        "events",
                        []
                    ),

                    logs=state["evidence"].get(
                        "logs",
                        []
                    ),

                    raw_evidence=state["evidence"]

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
                    reasoning=state["remediation_reasoning"],
                    steps=state["remediation_steps"],
                )
            )


            db.commit()

            return incident.id

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()