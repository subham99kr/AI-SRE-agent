from typing import TypedDict

from app.database.incident import Incident
from app.database.evidence import Evidence
from app.database.remediation import Remediation
from app.models.report import IncidentReport


class ExecutionState(TypedDict, total=False):

    incident_id: str

    cluster_id: str

    incident: Incident

    evidence: Evidence

    remediation: Remediation

    execution_results: list

    verification_success: bool

    verification_message: str

    verification_checks: list[str]

    incident_report: IncidentReport
