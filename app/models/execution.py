from pydantic import BaseModel


class CommandResult(BaseModel):

    command: str

    success: bool

    stdout: str

    stderr: str

class ExecutionResult(BaseModel):

    step: str

    command: str

    success: bool

    stdout: str

    stderr: str