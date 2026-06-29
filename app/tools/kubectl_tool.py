import shlex
import subprocess
import json

from app.models.execution import (
    CommandResult
)
from app.config.kubernetes_config import ClusterManager


class KubectlTool:
    def __init__(
        self,
        cluster_id: str
    ):

        self.kubeconfig = (
            ClusterManager()
            .get_kubeconfig_path(cluster_id)
        )

        if self.kubeconfig is None:
            raise ValueError(
                f"Unknown cluster: {cluster_id}"
            )

    def run(
        self,
        command: str
    ) -> CommandResult:
        
        command = command.strip()

        if command.startswith("kubectl "):
            command = command[len("kubectl "):]

        command = (
            f'kubectl '
            f'--kubeconfig "{self.kubeconfig}" '
            f'{command}'
        )

        try:

            args = shlex.split(command)

            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=10
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
            f"rollout status "
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
            f"rollout restart "
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
            f"rollout undo "
            f"deployment/{deployment} "
            f"-n {namespace}"
        )

        return self.run(command)

    def apply(
        self,
        file_path: str
    ) -> CommandResult:

        command = (
            f"apply -f {file_path}"
        )

        return self.run(command)

    def delete(
        self,
        file_path: str
    ) -> CommandResult:

        command = (
            f"delete -f {file_path}"
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
            f"patch {resource} {name} "
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
            f"scale deployment "
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
            f"get pods "
            f"-n {namespace}"
        )

        return self.run(command)

    def get_deployment(
        self,
        deployment: str,
        namespace: str
    ) -> CommandResult:

        command = (
            f"get deployment "
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
            f"describe deployment "
            f"{deployment} "
            f"-n {namespace}"
        )

        return self.run(command)

    def get_deployment_json(
        self,
        deployment: str,
        namespace: str
    ):

        command = (
            f"get deployment "
            f"{deployment} "
            f"-n {namespace} "
            f"-o json"
        )

        result = self.run(command)

        if not result.success:
            return None

        try:
            return json.loads(result.stdout)

        except Exception:
            return None

    def get_pods_json(
        self,
        namespace: str
    ):

        command = (
            f"get pods "
            f"-n {namespace} "
            f"-o json"
        )

        result = self.run(command)

        if not result.success:
            return None

        try:
            return json.loads(result.stdout)

        except Exception:
            return None