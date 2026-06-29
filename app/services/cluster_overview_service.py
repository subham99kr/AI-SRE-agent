from app.config.kubernetes_config import (
    ClusterManager
)

from app.tools.kubernetes_reader import (
    KubernetesTool
)


class ClusterOverviewService:

    def get_clusters(self):

        manager = ClusterManager()

        overview = []

        for cluster_id in manager.get_cluster_names():

            try:

                k8s = KubernetesTool(cluster_id)

                cluster = {

                    "cluster_id": cluster_id,

                    "status": "ONLINE",

                    "namespaces": []

                }

                namespaces = k8s.list_namespaces()

                for namespace in namespaces:

                    deployments = (
                        k8s.list_deployments(
                            namespace
                        )
                    )

                    replicasets = (
                        k8s.list_replicasets(
                            namespace
                        )
                    )

                    pods = (
                        k8s.list_pods(
                            namespace
                        )
                    )

                    running = sum(

                        1

                        for pod in pods

                        if (
                            pod["status"] == "Running"
                            and
                            pod["ready"]
                        )

                    )

                    failed = len(pods) - running

                    cluster["namespaces"].append(

                        {

                            "name":
                            namespace,

                            "pod_count":
                            len(pods),

                            "running_pods":
                            running,

                            "failed_pods":
                            failed,

                            "deployment_count":
                            len(deployments),

                            "replicaset_count":
                            len(replicasets),

                            "pods":
                            pods

                        }

                    )

                overview.append(cluster)

            except Exception:

                overview.append(

                    {

                        "cluster_id":
                        cluster_id,

                        "status":
                        "OFFLINE",

                        "namespaces":
                        []

                    }

                )

        return overview