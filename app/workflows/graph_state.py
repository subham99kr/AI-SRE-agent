from typing import TypedDict

from app.models.evidence import Evidence


class InvestigationState(
    TypedDict,
    total=False
):
    namespace: str

    deployment: str

    evidence: Evidence

    incident_type: str

    root_cause: str

    confidence: float

    fix_plan: list[str]