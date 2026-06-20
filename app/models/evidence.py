from pydantic import BaseModel
from pydantic import Field


class PodLog(BaseModel):

    pod: str

    current_logs: str | None = None

    previous_logs: str | None = None


class Evidence(BaseModel):

    #
    # Initial Investigation
    #

    namespace: str

    deployment: str

    deployment_spec: list[dict] = Field(
        default_factory=list
    )

    pods: list[dict] = Field(
        default_factory=list
    )

    events: list[dict] = Field(
        default_factory=list
    )

    #
    # Adaptive Evidence
    #

    logs: list[PodLog] = Field(
        default_factory=list
    )

    reports: dict[str, list[str]] = Field(
        default_factory=dict
    )

    metrics: dict = Field(
        default_factory=dict
    )