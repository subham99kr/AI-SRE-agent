from sqlalchemy.orm import Session

from app.database.session import SessionLocal

from app.storage.incident_repository import (
    IncidentRepository
)

from app.storage.remediation_repository import (
    RemediationRepository
)

from app.storage.report_repository import (
    ReportRepository
)


class RetryMemoryService:

    def load(
        self,
        root_incident_id: str,
        limit: int = 5
    ) -> str:

        db: Session = SessionLocal()

        try:

            incident_repo = IncidentRepository(db)

            remediation_repo = (
                RemediationRepository(db)
            )

            report_repo = (
                ReportRepository(db)
            )

            incidents = (
                incident_repo
                .get_attempts_by_root(
                    root_incident_id,
                    limit
                )
            )

            if not incidents:

                return ""

            sections = []

            for incident in incidents:

                remediation = (
                    remediation_repo.get(
                        incident.id
                    )
                )

                report = (
                    report_repo.get(
                        incident.id
                    )
                )

                section = []

                section.append(
                    f"Attempt #{incident.attempt_number}"
                )

                section.append(
                    f"Status: {incident.status}"
                )

                section.append(
                    f"Root Cause: {incident.root_cause}"
                )

                if remediation:

                    section.append(
                        "Remediation:"
                    )

                    for step in remediation.steps:

                        section.append(

                            f"- {step['description']}"

                        )

                if report:

                    section.append(

                        f"Outcome: "

                        f"{report.overall_status}"

                    )

                if incident.operator_feedback:

                    section.append(

                        "Operator Feedback: "

                        f"{incident.operator_feedback}"

                    )

                sections.append(

                    "\n".join(section)

                )

            return "\n\n".join(sections)

        finally:

            db.close()