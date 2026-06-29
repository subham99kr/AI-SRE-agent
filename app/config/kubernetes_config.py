import yaml
from kubernetes import config


class ClusterManager:

    def __init__(self):

        with open(
            "clusters.yaml",
            "r"
        ) as file:

            self.config = yaml.safe_load(file)

    def _get_cluster(
        self,
        cluster_id: str
    ):

        return next(

            c

            for c in self.config["clusters"]

            if c["id"] == cluster_id

        )

    def get_cluster_names(self):

        return [

            cluster["id"]

            for cluster in self.config["clusters"]

        ]

    def get_client(
        self,
        cluster_id: str
    ):

        cluster = self._get_cluster(
            cluster_id
        )

        return config.new_client_from_config(

            config_file=cluster["kubeconfig"]

        )

    def get_kubeconfig_path(
        self,
        cluster_id: str
    ):

        cluster = self._get_cluster(
            cluster_id
        )

        return cluster["kubeconfig"]

    def get_prometheus_url(
        self,
        cluster_id: str
    ):

        cluster = self._get_cluster(
            cluster_id
        )

        return cluster["prometheus"]
    
    def get_clusters(self):

        return self.config["clusters"]