import asyncio

from app.models.verification import (
    VerificationResult
)

from app.tools.kubectl_tool import (
    KubectlTool
)


class VerificationAgent:

    STABILIZATION_SECONDS = 10

    def __init__(self):

        self.tool = KubectlTool()

    async def run(

        self,

        namespace: str,

        deployment: str

    ) -> VerificationResult:

        checks = []

        #
        # Wait for rollout first
        #

        rollout = self.tool.rollout_status(

            deployment,

            namespace

        )

        if not rollout.success:

            return VerificationResult(

                success=False,

                message="Deployment rollout has not completed.",

                checks=[

                    "Rollout status check failed."

                ]

            )

        checks.append(
            "Rollout completed successfully."
        )

        #
        # First health check
        #

        ok, checks, restart_counts = self._check_cluster(

            namespace,

            deployment,

            checks

        )

        if not ok:

            return VerificationResult(

                success=False,

                message="Deployment is not healthy.",

                checks=checks

            )

        #
        # Stabilization period
        #

        await asyncio.sleep(

            self.STABILIZATION_SECONDS

        )

        #
        # Second health check
        #

        ok, checks, restart_counts_after = self._check_cluster(

            namespace,

            deployment,

            checks

        )

        if not ok:

            return VerificationResult(

                success=False,

                message="Deployment became unhealthy after rollout.",

                checks=checks

            )

        #
        # Restart count must not increase
        #

        for pod_name in restart_counts:

            if (

                restart_counts_after.get(

                    pod_name,

                    0

                )

                >

                restart_counts[pod_name]

            ):

                checks.append(

                    f"{pod_name}: restart count increased."

                )

                return VerificationResult(

                    success=False,

                    message="Pods are still restarting.",

                    checks=checks

                )

        checks.append(

            "Deployment remained healthy during stabilization."

        )

        return VerificationResult(

            success=True,

            message="Deployment successfully recovered.",

            checks=checks

        )

    def _check_cluster(

        self,

        namespace: str,

        deployment: str,

        checks: list[str]

    ):

        deployment_json = (

            self.tool.get_deployment_json(

                deployment,

                namespace

            )

        )

        if deployment_json is None:

            checks.append(

                "Deployment not found."

            )

            return False, checks, {}

        checks.append(

            "Deployment exists."

        )

        conditions = {

            c["type"]: c["status"]

            for c in deployment_json

            .get(

                "status",

                {}

            )

            .get(

                "conditions",

                []

            )

        }

        if (

            conditions.get(

                "Available"

            )

            != "True"

        ):

            checks.append(

                "Deployment Available=False"

            )

            return False, checks, {}

        checks.append(

            "Deployment Available=True"

        )

        pods = (

            self.tool.get_pods_json(

                namespace

            )

        )

        if pods is None:

            checks.append(

                "Unable to retrieve pods."

            )

            return False, checks, {}

        restart_counts = {}

        deployment_prefix = (

            deployment + "-"

        )

        matching = [

            p

            for p in pods["items"]

            if p["metadata"]["name"].startswith(

                deployment_prefix

            )

        ]

        if not matching:

            checks.append(

                "No pods found."

            )

            return False, checks, {}

        for pod in matching:

            name = pod["metadata"]["name"]

            status = pod["status"]

            phase = status.get(

                "phase"

            )

            if phase != "Running":

                checks.append(

                    f"{name}: phase={phase}"

                )

                return False, checks, {}

            container_statuses = status.get(

                "containerStatuses",

                []

            )

            if not container_statuses:

                checks.append(

                    f"{name}: no container status."

                )

                return False, checks, {}

            for container in container_statuses:

                restart_counts[name] = container.get(

                    "restartCount",

                    0

                )

                if not container.get(

                    "ready",

                    False

                ):

                    checks.append(

                        f"{name}: container not ready."

                    )

                    return False, checks, {}

                waiting = (

                    container

                    .get(

                        "state",

                        {}

                    )

                    .get(

                        "waiting"

                    )

                )

                if waiting:

                    reason = waiting.get(

                        "reason",

                        "Unknown"

                    )

                    checks.append(

                        f"{name}: waiting={reason}"

                    )

                    return False, checks, {}

                terminated = (

                    container

                    .get(

                        "state",

                        {}

                    )

                    .get(

                        "terminated"

                    )

                )

                if terminated:

                    reason = terminated.get(

                        "reason",

                        "Unknown"

                    )

                    checks.append(

                        f"{name}: terminated={reason}"

                    )

                    return False, checks, {}

        checks.append(

            "All deployment pods are Running and Ready."

        )

        return True, checks, restart_counts