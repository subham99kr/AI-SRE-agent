from pydantic import BaseModel


class IncidentRequest(BaseModel):
    description: str


class IncidentResponse(BaseModel):
    root_cause: str
    confidence: float
    fix_plan: list[str]

class ClusterIncidentRequest(BaseModel):
    namespace: str
    deployment: str