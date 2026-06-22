from pydantic import BaseModel


class RemediationStep(BaseModel):

    description: str

    kubectl_command: str | None = None


class RemediationPlan(BaseModel):
    action_required: bool

    action_reason: str

    risk: str

    requires_approval: bool = True

    rollback_available: bool

    steps: list[RemediationStep]