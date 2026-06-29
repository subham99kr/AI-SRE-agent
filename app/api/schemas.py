from pydantic import BaseModel
from datetime import datetime
from typing import Any


class IncidentRequest(BaseModel):

    description: str


class ClusterIncidentRequest(BaseModel):

    namespace: str
    cluster_id: str
    deployment: str


class RemediationStep(BaseModel):

    description: str

    kubectl_command: str | None = None


class IncidentResponse(BaseModel):

    root_cause: str

    confidence: float

    risk: str

    status: str

    approval_status: str

    approval_reason: str | None = None
    
    requires_approval: bool = True

    rollback_available: bool

    remediation_steps: list[RemediationStep]

    verification_success: bool

    verification_message: str

    verification_checks: list[str]

    incident_id: str | None = None


class IncidentListItem(BaseModel):

    id: str

    created_at: datetime
    cluster_id : str
    namespace: str

    deployment: str

    incident_type: str

    risk: str

    verification_success: bool



class IncidentDetailsResponse(BaseModel):

    incident: dict | None = None

    evidence: dict | None = None

    remediation: dict | None = None

    execution: dict | None = None

    verification: dict | None = None

    report: dict | None = None

class AttemptResponse(BaseModel):

    id: str

    attempt_number: int

    status: str

    approval_status: str

    verification_success: bool

    created_at: datetime