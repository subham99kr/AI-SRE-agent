from pydantic import BaseModel


class IncidentReport(BaseModel):

    title: str

    executive_summary: str

    technical_summary: str

    overall_status: str

    recommendations: list[str]