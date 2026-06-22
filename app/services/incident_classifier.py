from app.models.evidence import (
    Evidence
)


class IncidentClassifier:

    @staticmethod
    def classify(
        evidence: Evidence
    ) -> str:

        #
        # Pod-based detection
        #

        for pod in evidence.pods:

            phase = pod.get(
                "phase"
            )

            waiting_reason = pod.get(
                "waiting_reason"
            )

            restart_count = pod.get(
                "restarts",
                0
            )

            last_exit_code = pod.get(
                "last_exit_code"
            )

            termination_reason = pod.get(
                "termination_reason"
            )

            #
            # Image Pull
            #

            if waiting_reason in (
                "ImagePullBackOff",
                "ErrImagePull"
            ):

                return "IMAGE_PULL"

            #
            # Pending
            #

            if phase == "Pending":

                return "PENDING"

            #
            # OOMKilled
            #

            if termination_reason == "OOMKilled":

                return "OOM_KILLED"

            #
            # CrashLoop
            #

            if waiting_reason == "CrashLoopBackOff":
                return "CRASH_LOOP"

            if (
                restart_count >= 3
                and phase != "Running"

            ):

                return "CRASH_LOOP"

            if (

                termination_reason == "Error"

                and restart_count >= 3

            ):

                return "CRASH_LOOP"

        #
        # Event-based detection
        #

        for event in evidence.events:

            reason = event.get(
                "reason",
                ""
            )

            message = (
                event.get(
                    "message",
                    ""
                )
                .lower()
            )

            #
            # Image Pull
            #

            if (

                reason in (
                    "ErrImagePull",
                    "Failed"
                )

                and (

                    "pull image" in message

                    or "imagepullbackoff" in message

                    or "errimagepull" in message

                )

            ):

                return "IMAGE_PULL"

            #
            # CrashLoop
            #

            if reason == "BackOff":

                return "CRASH_LOOP"

            #
            # Scheduling
            #

            if reason == "FailedScheduling":

                return "UNSCHEDULABLE"

            #
            # Evicted
            #

            if reason == "Evicted":

                return "EVICTED"

        #
        # Unknown
        #

        return "UNKNOWN"