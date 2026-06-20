import shlex
import subprocess

from app.models.execution import (
    CommandResult
)


class KubectlTool:

    def run(
        self,
        command: str
    ) -> CommandResult:

        try:

            args = shlex.split(command)

            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=120
            )

            return CommandResult(
                command=command,
                success=result.returncode == 0,
                stdout=result.stdout.strip(),
                stderr=result.stderr.strip()
            )

        except Exception as e:

            return CommandResult(
                command=command,
                success=False,
                stdout="",
                stderr=str(e)
            )

    def rollout_status(
        self,
        deployment: str,
        namespace: str
    ) -> CommandResult:

        command = (
            f"kubectl rollout status "
            f"deployment/{deployment} "
            f"-n {namespace}"
        )

        return self.run(command)

    def rollout_restart(
        self,
        deployment: str,
        namespace: str
    ) -> CommandResult:

        command = (
            f"kubectl rollout restart "
            f"deployment/{deployment} "
            f"-n {namespace}"
        )

        return self.run(command)

    def rollout_undo(
        self,
        deployment: str,
        namespace: str
    ) -> CommandResult:

        command = (
            f"kubectl rollout undo "
            f"deployment/{deployment} "
            f"-n {namespace}"
        )

        return self.run(command)

    def apply(
        self,
        file_path: str
    ) -> CommandResult:

        command = (
            f"kubectl apply -f {file_path}"
        )

        return self.run(command)

    def delete(
        self,
        file_path: str
    ) -> CommandResult:

        command = (
            f"kubectl delete -f {file_path}"
        )

        return self.run(command)

    def patch(
        self,
        resource: str,
        name: str,
        patch: str,
        namespace: str
    ) -> CommandResult:

        command = (
            f"kubectl patch {resource} {name} "
            f"-n {namespace} "
            f"-p '{patch}'"
        )

        return self.run(command)

    def scale(
        self,
        deployment: str,
        replicas: int,
        namespace: str
    ) -> CommandResult:

        command = (
            f"kubectl scale deployment "
            f"{deployment} "
            f"--replicas={replicas} "
            f"-n {namespace}"
        )

        return self.run(command)

    def get_pods(
        self,
        namespace: str
    ) -> CommandResult:

        command = (
            f"kubectl get pods "
            f"-n {namespace}"
        )

        return self.run(command)

    def get_deployment(
        self,
        deployment: str,
        namespace: str
    ) -> CommandResult:

        command = (
            f"kubectl get deployment "
            f"{deployment} "
            f"-n {namespace}"
        )

        return self.run(command)

    def describe_deployment(
        self,
        deployment: str,
        namespace: str
    ) -> CommandResult:

        command = (
            f"kubectl describe deployment "
            f"{deployment} "
            f"-n {namespace}"
        )

        return self.run(command)