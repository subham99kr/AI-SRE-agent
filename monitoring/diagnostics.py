from kubectl import Kubectl


class Diagnostics:

    def __init__(
        self,
        context: str
    ):

        self.kubectl = Kubectl(
            context
        )

    def collect(self):

        print()

        print("=" * 60)

        print(
            "Collecting Diagnostics"
        )

        print("=" * 60)

        print()

        print("Pods")

        print("-" * 60)

        print(

            self.kubectl.get_pods(

                "monitoring"

            ).stdout

        )

        print()

        print("Events")

        print("-" * 60)

        print(

            self.kubectl.get_events(

                "monitoring"

            ).stdout

        )

        print()

        pods = self.kubectl.get_pod_names(

            "monitoring",

            "app=prometheus"

        )

        for pod in pods:

            print()

            print("=" * 60)

            print(pod)

            print("=" * 60)

            print()

            print("Describe")

            print("-" * 60)

            print(

                self.kubectl.describe_pod(

                    pod,

                    "monitoring"

                ).stdout

            )

            print()

            print("Logs")

            print("-" * 60)

            print(

                self.kubectl.pod_logs(

                    pod,

                    "monitoring"

                ).stdout

            )

        print()

        print("Deployment")

        print("-" * 60)

        print(

            self.kubectl.deployment_yaml(

                "prometheus",

                "monitoring"

            ).stdout

        )