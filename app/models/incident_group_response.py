from pydantic import BaseModel
from datetime import datetime

class IncidentGroupResponse(BaseModel):

    root_incident_id: str

    namespace: str
    cluster_id: str
    deployment: str

    attempt_count: int

    latest_status: str

    latest_created_at: datetime