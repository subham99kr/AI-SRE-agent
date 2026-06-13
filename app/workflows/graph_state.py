from typing import TypedDict


class InvestigationState(
    TypedDict,
    total=False
):

    namespace: str

    deployment: str

    evidence: dict

    incident_type: str

    root_cause: str

    confidence: float

    risk: str

    requires_approval: bool

    rollback_available: bool

    remediation_steps: list

    execution_results: list

    verification_success: bool

    verification_message: str

    verification_checks: list[str]