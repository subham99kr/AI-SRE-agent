from pydantic import BaseModel


class PodLog(BaseModel):

    pod: str

    current_logs: str | None = None

    previous_logs: str | None = None


class Evidence(BaseModel):

    namespace: str

    deployment: str

    deployment_spec: list[dict]

    pods: list[dict]

    events: list[dict]

    logs: list[PodLog]