import requests

from app.config.kubernetes_config import (
    ClusterManager
)


class PrometheusConnectionService:

    def __init__(self):

        self.cluster_manager = ClusterManager()

    def verify(
        self,
        cluster_id: str
    ) -> bool:

        url = (

            self.cluster_manager

            .get_prometheus_url(
                cluster_id
            )

        )

        try:

            response = requests.get(

                f"{url}/-/healthy",

                timeout=5

            )

            return response.status_code == 200

        except Exception:

            return False

    def verify_all(self):

        result = {}

        for cluster in (

            self.cluster_manager

            .get_cluster_names()

        ):

            result[cluster] = (

                self.verify(cluster)

            )

        return result