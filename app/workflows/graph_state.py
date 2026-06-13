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

    fix_plan: list[str]

    confidence: float