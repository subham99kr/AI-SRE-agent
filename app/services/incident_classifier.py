from app.models.evidence import Evidence


class IncidentClassifier:

    @staticmethod
    def classify(
        evidence: Evidence
    ) -> str:

        for pod in evidence.pods:

            waiting_reason = (
                pod.get("waiting_reason")
            )

            restart_count = (
                pod.get("restarts", 0)
            )

            last_exit_code = (
                pod.get("last_exit_code")
            )

            termination_reason = (
                pod.get("termination_reason")
            )

            if waiting_reason in [
                "ImagePullBackOff",
                "ErrImagePull"
            ]:

                return "IMAGE_PULL"

            if (
                waiting_reason == "CrashLoopBackOff"
                or restart_count >= 3
                or (
                    last_exit_code is not None
                    and last_exit_code != 0
                )
                or termination_reason == "Error"
            ):

                return "CRASH_LOOP"

        for event in evidence.events:

            reason = event.get(
                "reason",
                ""
            )

            message = event.get(
                "message",
                ""
            )

            if reason == "BackOff":

                return "CRASH_LOOP"

            if (
                reason in [
                    "ErrImagePull",
                    "Failed"
                ]
                and "pull image"
                in message.lower()
            ):

                return "IMAGE_PULL"

        return "UNKNOWN"