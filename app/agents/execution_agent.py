from app.tools.kubectl_tool import (
    KubectlTool
)


class ExecutionAgent:

    def __init__(self):

        self.kubectl = KubectlTool()

    async def run(
        self,
        remediation_steps: list
    ) -> dict:

        execution_results = []

        for step in remediation_steps:

            command = step.get(
                "kubectl_command"
            )

            if not command:

                continue

            result = self.kubectl.run(
                command
            )

            execution_results.append(
                result.model_dump()
            )

        return {
            "execution_results":
            execution_results
        }