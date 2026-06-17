from sqlalchemy.orm import Session

from app.database.session import SessionLocal

from app.database.execution import Execution
from app.database.verification import Verification
from app.database.report import Report

from app.storage.incident_repository import IncidentRepository
from app.storage.execution_repository import ExecutionRepository
from app.storage.verification_repository import VerificationRepository
from app.storage.report_repository import ReportRepository


class ExecutionPersistenceService:

    def save(
        self,
        state: dict
    ):

        db: Session = SessionLocal()

        try:

            incident_repo = IncidentRepository(db)

            execution_repo = ExecutionRepository(db)

            verification_repo = VerificationRepository(db)

            report_repo = ReportRepository(db)

            #
            # Load Incident
            #

            incident = incident_repo.get(
                state["incident"].id
            )

            if incident is None:

                raise ValueError(
                    "Incident not found."
                )

            #
            # Update Incident
            #

            incident.status = (

                "RESOLVED"

                if state["verification_success"]

                else

                "FAILED"

            )

            incident.verification_success = (
                state["verification_success"]
            )

            incident.verification_message = (
                state["verification_message"]
            )

            incident_repo.update(
                incident
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

                        stderr=item["stderr"]

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

                    checks=state["verification_checks"]

                )

            )

            #
            # Save Report
            #

            report = state[
                "incident_report"
            ].model_dump()

            report_repo.create(

                Report(

                    incident_id=incident.id,

                    title=report["title"],

                    executive_summary=report[
                        "executive_summary"
                    ],

                    technical_summary=report[
                        "technical_summary"
                    ],

                    overall_status=report[
                        "overall_status"
                    ],

                    recommendations=report[
                        "recommendations"
                    ]

                )

            )

            db.commit()

        except Exception:

            db.rollback()

            raise

        finally:

            db.close()