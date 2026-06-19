from pydantic import BaseModel


class RejectRequest(BaseModel):

    # incident_id: str
    
    feedback: str

    user: str