from app.models.evidence import Evidence
from app.tools.kubernetes_reader import KubernetesTool


class EvidenceBuilder:

    def __init__(self):

        self.k8s = KubernetesTool()

    def build_incident_context(
        self,
        namespace: str,
        deployment: str
    ) -> Evidence:

        pods = self.k8s.get_deployment_pods(
            deployment_name=deployment,
            namespace=namespace
        )

        deployment_spec = (
            self.k8s.get_deployment_spec(
                deployment_name=deployment,
                namespace=namespace
            )
        )

        events = []
        logs = []

        seen_events = set()

        for pod in pods:

            pod_name = pod["name"]

            try:

                pod_events = self.k8s.get_pod_events(
                    pod_name=pod_name,
                    namespace=namespace
                )

                for event in pod_events:

                    key = (
                        event.get("reason"),
                        event.get("message")
                    )

                    if key not in seen_events:

                        seen_events.add(key)
                        events.append(event)

            except Exception as e:

                events.append(
                    {
                        "reason": "EventCollectionFailed",
                        "message": str(e),
                        "type": "Error"
                    }
                )

            try:

                waiting_reason = (
                    pod.get("waiting_reason")
                )

                restart_count = (
                    pod.get("restarts", 0)
                )

                if waiting_reason in [
                    "ImagePullBackOff",
                    "ErrImagePull"
                ]:

                    logs.append(
                        {
                            "pod": pod_name,
                            "current_logs":
                            "Container never started; logs unavailable.",
                            "previous_logs": None
                        }
                    )

                elif restart_count > 0:

                    previous_logs = (
                        self.k8s.get_previous_logs(
                            pod_name=pod_name,
                            namespace=namespace
                        )
                    )

                    if isinstance(
                        previous_logs,
                        bytes
                    ):

                        previous_logs = (
                            previous_logs.decode(
                                "utf-8",
                                errors="ignore"
                            )
                        )

                    # Handles literal string "b''"
                    if (
                        str(previous_logs).strip()
                        == "b''"
                    ):

                        previous_logs = ""

                    

                    if (
                        "unable to retrieve container logs"
                        in str(previous_logs).lower()
                    ):
                        previous_logs = (
                            "Container terminated before logs could be collected."
                        )

                    if not str(previous_logs).strip():

                        previous_logs = (
                            "No logs emitted before container exit."
                        )

                    logs.append(
                        {
                            "pod": pod_name,
                            "current_logs": None,
                            "previous_logs":previous_logs
                        }
                    )

                else:

                    current_logs = (
                        self.k8s.get_pod_logs(
                            pod_name=pod_name,
                            namespace=namespace
                        )
                    )

                    if isinstance(
                        current_logs,
                        bytes
                    ):

                        current_logs = (
                            current_logs.decode(
                                "utf-8",
                                errors="ignore"
                            )
                        )

                    if (
                        str(current_logs).strip()
                        == "b''"
                    ):

                        current_logs = ""

                    if not str(
                        current_logs
                    ).strip():

                        current_logs = (
                            "No logs available."
                        )

                    logs.append(
                        {
                            "pod": pod_name,
                            "current_logs":
                            current_logs,
                            "previous_logs": None
                        }
                    )

            except Exception as e:

                logs.append(
                    {
                        "pod": pod_name,
                        "current_logs":
                        f"Failed to fetch logs: {e}",
                        "previous_logs": None
                    }
                )

        return Evidence(
            namespace=namespace,
            deployment=deployment,
            deployment_spec=deployment_spec,
            pods=pods,
            events=events,
            logs=logs
        )