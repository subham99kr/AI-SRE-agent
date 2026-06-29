from pathlib import Path

from kubectl import Kubectl


ROOT = Path(__file__).parent


class MonitoringInstaller:

    def __init__(
        self,
        context: str
    ):

        self.kubectl = Kubectl(
            context
        )

    def install(self):

        print()

        print("=" * 60)
        print("Installing Monitoring Stack")
        print("=" * 60)

        self.namespace()

        self.rbac()

        self.configmap()

        self.pvc()

        self.deployment()

        self.service()

        self.wait()

        print()

        print("=" * 60)
        print("Monitoring Ready")
        print("=" * 60)

    def namespace(self):

        print()

        print("Namespace")

        if self.kubectl.namespace_exists(
            "monitoring"
        ):

            print("✓ Exists")

            return

        self.kubectl.apply(

            ROOT /

            "namespace.yaml"

        )

    def rbac(self):

        print()

        print("RBAC")

        self.kubectl.apply(

            ROOT /

            "prometheus-rbac.yaml"

        )

    def configmap(self):

        print()

        print("ConfigMap")

        self.kubectl.apply(

            ROOT /

            "prometheus-configmap.yaml"

        )

    def pvc(self):

        print()

        print("PVC")

        if self.kubectl.pvc_exists(

            "prometheus-data",

            "monitoring"

        ):

            print("✓ Exists")

            return

        self.kubectl.apply(

            ROOT /

            "prometheus-pvc.yaml"

        )

    def deployment(self):

        print()

        print("Deployment")

        self.kubectl.apply(

            ROOT /

            "prometheus-deployment.yaml"

        )

    def service(self):

        print()

        print("Service")

        self.kubectl.apply(

            ROOT /

            "prometheus-service.yaml"

        )

    def wait(self):

        print()

        print("Waiting for Prometheus...")

        try:

            self.kubectl.rollout(

                "prometheus",

                "monitoring"

            )

        except Exception:

            print()

            print("Deployment rollout failed.")

            print()

            print(

                self.kubectl.get_pods(

                    "monitoring"

                ).stdout

            )

            raise

        try:

            self.kubectl.wait_for_pod(

                "monitoring",

                "app=prometheus"

            )

        except Exception:

            print()

            print("Prometheus pod never became Ready.")

            print()

            print(

                self.kubectl.get_pods(

                    "monitoring"

                ).stdout

            )

            raise

        print()

        print("✓ Monitoring Ready")