from app.models.evidence import (
    Evidence
)

from app.tools.kubernetes_reader import (
    KubernetesTool
)


class EvidenceBuilder:

    def __init__(self):

        self.k8s = KubernetesTool()

    def build_initial_context(

        self,

        namespace: str,

        deployment: str

    ) -> Evidence:

        """
        Collect only the minimum Kubernetes evidence
        required to classify the incident.

        Additional evidence is collected later by
        EvidenceCollector based on the selected playbook.
        """

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

                        seen_events.add(

                            key

                        )

                        events.append(

                            event

                        )

            except Exception as e:

                events.append(

                    {

                        "reason":
                        "EventCollectionFailed",

                        "message":
                        str(e),

                        "type":
                        "Error"

                    }

                )

        return Evidence(

            namespace=namespace,

            deployment=deployment,

            deployment_spec=deployment_spec,

            pods=pods,

            events=events

        )