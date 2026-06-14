from pydantic import BaseModel
from datetime import datetime


class IncidentRequest(BaseModel):

    description: str


class ClusterIncidentRequest(BaseModel):

    namespace: str

    deployment: str


class RemediationStep(BaseModel):

    description: str

    kubectl_command: str | None = None


class IncidentResponse(BaseModel):

    root_cause: str

    confidence: float

    risk: str

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

    namespace: str

    deployment: str

    incident_type: str

    risk: str

    verification_success: bool


class IncidentDetailsResponse(BaseModel):

    id: str

    created_at: datetime

    namespace: str

    deployment: str

    incident_type: str

    root_cause: str

    confidence: float

    risk: str

    requires_approval: bool

    rollback_available: bool

    verification_success: bool

    verification_message: str