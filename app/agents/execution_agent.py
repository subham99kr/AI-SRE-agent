from app.models.execution import (
    ExecutionResult
)

from app.tools.kubectl_tool import (
    KubectlTool
)


class ExecutionAgent:

    async def run(

        self,
        cluster_id: str,

        remediation_steps: list,

        approved: bool

    ) -> list[dict]:
        
        self.tool = KubectlTool(cluster_id)

        if not approved:

            print("=" * 80)
            print("Execution skipped because approval is required.")
            print("=" * 80)

            return []

        results = []

        for step in remediation_steps:

            command = step.get(
                "kubectl_command"
            )

            if not command:

                continue

            print("=" * 80)
            print(
                f"EXECUTING: {command}"
            )
            print("=" * 80)

            result = self.tool.run(
                command
            )

            execution = ExecutionResult(

                step=step[
                    "description"
                ],

                command=command,

                success=result.success,

                stdout=result.stdout,

                stderr=result.stderr

            )

            results.append(
                execution.model_dump()
            )

            if not result.success:

                print("=" * 80)
                print(
                    "Stopping execution because one command failed."
                )
                print("=" * 80)

                break

        return results