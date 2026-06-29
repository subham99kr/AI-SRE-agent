import requests

from kubectl import Kubectl


class HealthChecker:

    def __init__(

        self,

        context: str,

        prometheus_url: str

    ):

        self.context = context

        self.prometheus = prometheus_url

        self.kubectl = Kubectl(
            context
        )

    def verify(self):

        print()

        print("=" * 60)

        print("Health Check")

        print("=" * 60)

        self.check_pod()

        self.check_service()

        self.check_api()

        self.check_targets()

        print()

        print("✓ Monitoring Stack Healthy")

    def check_pod(self):

        print()

        print("Checking Pod...")

        self.kubectl.wait_for_pod(

            "monitoring",

            "app=prometheus"

        )

        print("✓ Pod Ready")

    def check_service(self):

        print()

        print("Checking Service...")

        if not self.kubectl.service_exists(

            "prometheus",

            "monitoring"

        ):

            raise RuntimeError(

                "Prometheus service missing."

            )

        print("✓ Service Ready")

    def check_api(self):

        print()

        print("Checking API...")

        response = requests.get(

            f"{self.prometheus}/-/healthy",

            timeout=10

        )

        if response.status_code != 200:

            raise RuntimeError(

                "Prometheus API unavailable."

            )

        print("✓ API Healthy")

    def check_targets(self):

        print()

        print("Checking Targets...")

        response = requests.get(

            f"{self.prometheus}/api/v1/targets",

            timeout=10

        )

        response.raise_for_status()

        data = response.json()

        active = data["data"]["activeTargets"]

        print(

            f"✓ Active Targets : {len(active)}"

        )

        for target in active:

            print(

                f"   "

                f"{target['labels'].get('job')} "

                f"({target['health']})"

            )