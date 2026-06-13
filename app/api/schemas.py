from pydantic import BaseModel


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