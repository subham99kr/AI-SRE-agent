from pydantic import BaseModel


class CommandResult(BaseModel):

    command: str

    success: bool

    stdout: str

    stderr: str


class ExecutionResult(BaseModel):

    results: list[CommandResult]