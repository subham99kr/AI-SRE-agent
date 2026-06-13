from app.models.verification import (
    VerificationResult
)

from app.tools.kubectl_tool import (
    KubectlTool
)


class VerificationAgent:

    def __init__(self):

        self.tool = KubectlTool()

    async def run(

        self,

        namespace: str,

        deployment: str

    ) -> VerificationResult:

        checks = []

        deployment_result = (
            self.tool.describe_deployment(
                deployment,
                namespace
            )
        )

        if not deployment_result.success:

            return VerificationResult(

                success=False,

                message="Deployment not found.",

                checks=[]

            )

        checks.append(
            "Deployment exists."
        )

        pods_result = (
            self.tool.get_pods(
                namespace
            )
        )

        if not pods_result.success:

            return VerificationResult(

                success=False,

                message="Unable to retrieve Pods.",

                checks=checks

            )

        pod_lines = []

        lines = (
            pods_result.stdout
            .splitlines()
        )

        for line in lines[1:]:

            if line.startswith(
                deployment
            ):

                pod_lines.append(
                    line
                )

        if not pod_lines:

            checks.append(
                "No Pods found for deployment."
            )

            return VerificationResult(

                success=False,

                message="Deployment has no running Pods.",

                checks=checks

            )

        for pod in pod_lines:

            if (
                "CrashLoopBackOff"
                in pod
            ):

                checks.append(
                    "CrashLoopBackOff still detected."
                )

                return VerificationResult(

                    success=False,

                    message="Pods are still crashing.",

                    checks=checks

                )

            if (
                "ImagePullBackOff"
                in pod
            ):

                checks.append(
                    "ImagePullBackOff still detected."
                )

                return VerificationResult(

                    success=False,

                    message="Image pull failure still exists.",

                    checks=checks

                )

            if (
                "0/1"
                in pod
            ):

                checks.append(
                    "Some Pods are not Ready."
                )

                return VerificationResult(

                    success=False,

                    message="Deployment is not healthy.",

                    checks=checks

                )

        checks.append(
            "All deployment Pods are Ready."
        )

        rollout = (
            self.tool.rollout_status(
                deployment,
                namespace
            )
        )

        if rollout.success:

            checks.append(
                "Rollout completed successfully."
            )

        else:

            checks.append(
                "Rollout verification failed."
            )

            return VerificationResult(

                success=False,

                message="Deployment rollout has not completed.",

                checks=checks

            )

        return VerificationResult(

            success=True,

            message="Deployment successfully recovered.",

            checks=checks

        )