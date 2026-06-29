from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent

CLUSTERS_FILE = ROOT / "clusters.yaml"


class ClusterRegistry:

    def __init__(self):

        if CLUSTERS_FILE.exists():

            with open(

                CLUSTERS_FILE,

                "r"

            ) as file:

                self.data = yaml.safe_load(file)

                if self.data is None:

                    self.data = {

                        "clusters": []

                    }

        else:

            self.data = {

                "clusters": []

            }

    def save(self):

        with open(

            CLUSTERS_FILE,

            "w"

        ) as file:

            yaml.safe_dump(

                self.data,

                file,

                sort_keys=False

            )

    def register(

        self,

        cluster_id: str,

        kubeconfig_path: Path,

        prometheus_url: str,

        host_port: int | None = None

    ):

        existing = None

        for cluster in self.data["clusters"]:

            if cluster["id"] == cluster_id:

                existing = cluster

                break

        if existing:

            answer = input(

                f"'{cluster_id}' already exists. Overwrite? (Y/N): "

            )

            if answer.lower() != "y":

                print()

                print("Registration cancelled.")

                return

            self.data["clusters"].remove(

                existing

            )

        cluster = {

            "id":

            cluster_id,

            "name":

            cluster_id,

            "kubeconfig":

            f"./clusters/{kubeconfig_path.name}",

            "prometheus":

            prometheus_url

        }

        if host_port is not None:

            cluster["host_port"] = host_port

        self.data["clusters"].append(

            cluster

        )

        self.save()

        print()

        print("=" * 60)

        print("Cluster Registered Successfully")

        print("=" * 60)

        print()

        print(

            f"Cluster     : {cluster_id}"

        )

        print(

            f"Kubeconfig  : ./clusters/{kubeconfig_path.name}"

        )

        print(

            f"Prometheus  : {prometheus_url}"

        )

        if host_port is not None:

            print(

                f"Host Port   : {host_port}"

            )

        print()

    def unregister(

        self,

        cluster_id: str

    ):

        self.data["clusters"] = [

            cluster

            for cluster in self.data["clusters"]

            if cluster["id"] != cluster_id

        ]

        self.save()