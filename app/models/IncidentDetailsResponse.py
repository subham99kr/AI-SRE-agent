from pydantic import BaseModel


class IncidentDetailsResponse(BaseModel):

    incident: dict

    evidence: dict

    remediation: dict | None

    execution: dict | None

    verification: dict | None

    report: dict | None