from typing import TypedDict

from app.models.report import (
    IncidentReport
)


class InvestigationState(
    TypedDict,
    total=False
):

    #
    # Incoming Request
    #
    cluster_id: str
    namespace: str
    deployment: str

    #
    # Retry Information
    #

    retry: bool

    incident_id: str

    root_incident_id: str

    attempt_number: int

    #
    # Previous Attempt
    #


    previous_attempt_summary: str
    #
    # Current Investigation
    #

    evidence: dict

    incident_type: str

    root_cause: str

    confidence: float

    risk: str

    #
    # Approval
    #

    action_required: bool

    action_reason: str

    status: str

    requires_approval: bool

    approval_status: str

    approval_reason: str | None

    operator_feedback: str | None

    rollback_available: bool

    remediation_reasoning: str

    remediation_steps: list

    #
    # Execution
    #

    execution_results: list

    #
    # Verification
    #

    verification_success: bool

    verification_message: str

    verification_checks: list[str]

    #
    # Report
    #

    incident_report: IncidentReport