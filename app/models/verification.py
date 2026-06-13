from pydantic import BaseModel


class VerificationResult(BaseModel):

    success: bool

    message: str

    checks: list[str]