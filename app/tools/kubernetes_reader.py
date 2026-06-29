from kubernetes import client

from kubernetes import client

from app.config.kubernetes_config import (
    ClusterManager
)


class KubernetesTool:

    def __init__(self,cluster_id: str):
        self.cluster_id = cluster_id

        api_client = (ClusterManager().get_client(cluster_id))

        self.core_api = (client.CoreV1Api(api_client))

        self.apps_api = (client.AppsV1Api(api_client))

    def get_deployment(
        self,
        deployment_name: str,
        namespace: str = "default"
    ):

        return self.apps_api.read_namespaced_deployment(
            name=deployment_name,
            namespace=namespace
        )

    def get_deployment_pods(
        self,
        deployment_name: str,
        namespace: str = "default"
    ) -> list[dict]:

        deployment = self.get_deployment(
            deployment_name,
            namespace
        )

        selector = deployment.spec.selector.match_labels

        label_selector = ",".join(
            [
                f"{key}={value}"
                for key, value in selector.items()
            ]
        )

        pods = self.core_api.list_namespaced_pod(
            namespace=namespace,
            label_selector=label_selector
        )

        result = []

        for pod in pods.items:

            container_statuses = (
                pod.status.container_statuses or []
            )

            restart_count = sum(
                c.restart_count
                for c in container_statuses
            )

            waiting_reason = None
            ready = True
            last_exit_code = None
            termination_reason = None

            if container_statuses:

                status = container_statuses[0]

                ready = status.ready

                if (
                    status.state and
                    status.state.waiting
                ):
                    waiting_reason = (
                        status.state.waiting.reason
                    )

                if (
                    status.last_state and
                    status.last_state.terminated
                ):
                    last_exit_code = (
                        status.last_state.terminated.exit_code
                    )

                    termination_reason = (
                        status.last_state.terminated.reason
                    )

            result.append(
                {
                    "name": pod.metadata.name,
                    "phase": pod.status.phase,
                    "ready": ready,
                    "waiting_reason": waiting_reason,
                    "last_exit_code": last_exit_code,
                    "termination_reason": termination_reason,
                    "node": pod.spec.node_name,
                    "pod_ip": pod.status.pod_ip,
                    "restarts": restart_count
                }
            )

        return result

    def get_pod_logs(
        self,
        pod_name: str,
        namespace: str = "default",
        tail_lines: int = 100,
        previous: bool = False
    ):

        return self.core_api.read_namespaced_pod_log(
            name=pod_name,
            namespace=namespace,
            tail_lines=tail_lines,
            previous=previous
        )

    def get_previous_logs(
        self,
        pod_name: str,
        namespace: str = "default"
    ):

        try:

            return self.get_pod_logs(
                pod_name=pod_name,
                namespace=namespace,
                previous=True
            )

        except Exception:

            return "Previous container logs unavailable."

    def get_pod_events(
        self,
        pod_name: str,
        namespace: str = "default"
    ) -> list[dict]:

        events = self.core_api.list_namespaced_event(
            namespace=namespace
        )

        result = []

        for event in events.items:

            if (
                event.involved_object and
                event.involved_object.name == pod_name
            ):

                result.append(
                    {
                        "reason": event.reason,
                        "message": event.message,
                        "type": event.type
                    }
                )

        return result

    def get_events(
        self,
        namespace: str = "default"
    ) -> list[dict]:

        events = self.core_api.list_namespaced_event(
            namespace=namespace
        )

        result = []

        for event in events.items:

            result.append(
                {
                    "reason": event.reason,
                    "message": event.message,
                    "type": event.type,
                    "object": (
                        event.involved_object.name
                        if event.involved_object
                        else None
                    )
                }
            )

        return result
    
    def get_deployment_spec(
        self,
        deployment_name: str,
        namespace: str = "default"
    ) -> list[dict]:

        deployment = self.get_deployment(
            deployment_name,
            namespace
        )

        containers = (
            deployment
            .spec
            .template
            .spec
            .containers
        )

        result = []

        for container in containers:

            env_vars = []

            if container.env:

                env_vars = [
                    env.name
                    for env in container.env
                ]

            result.append(
                {
                    "name": container.name,
                    "image": container.image,
                    "command": container.command,
                    "args": container.args,
                    "env": env_vars
                }
            )

        return result
        
    def get_pod(
        self,
        pod_name: str,
        namespace: str = "default"
    ):

        return self.core_api.read_namespaced_pod(
            name=pod_name,
            namespace=namespace
        )
    

    def get_pod(
        self,
        pod_name: str,
        namespace: str = "default"
    ):

        return self.core_api.read_namespaced_pod(
            name=pod_name,
            namespace=namespace
        )

    def get_node(
        self,
        node_name: str
    ):

        return self.core_api.read_node(
            name=node_name
        )

    def get_service(
        self,
        service_name: str,
        namespace: str = "default"
    ):

        return self.core_api.read_namespaced_service(
            name=service_name,
            namespace=namespace
        )

    def get_endpoints(
        self,
        service_name: str,
        namespace: str = "default"
    ):

        return self.core_api.read_namespaced_endpoints(
            name=service_name,
            namespace=namespace
        )

    def get_pvc(
        self,
        pvc_name: str,
        namespace: str = "default"
    ):

        return self.core_api.read_namespaced_persistent_volume_claim(
            name=pvc_name,
            namespace=namespace
        )

    def get_pv(
        self,
        pv_name: str
    ):

        return self.core_api.read_persistent_volume(
            name=pv_name
        )

    def get_configmap(
        self,
        configmap_name: str,
        namespace: str = "default"
    ):

        return self.core_api.read_namespaced_config_map(
            name=configmap_name,
            namespace=namespace
        )

    def get_secret(
        self,
        secret_name: str,
        namespace: str = "default"
    ):

        return self.core_api.read_namespaced_secret(
            name=secret_name,
            namespace=namespace
        )

    def get_ingress(
        self,
        ingress_name: str,
        namespace: str = "default"
    ):

        networking = client.NetworkingV1Api()

        return networking.read_namespaced_ingress(
            name=ingress_name,
            namespace=namespace
        )

    def get_network_policy(
        self,
        policy_name: str,
        namespace: str = "default"
    ):

        networking = client.NetworkingV1Api()

        return networking.read_namespaced_network_policy(
            name=policy_name,
            namespace=namespace
        )

    def get_statefulset(
        self,
        name: str,
        namespace: str = "default"
    ):

        return self.apps_api.read_namespaced_stateful_set(
            name=name,
            namespace=namespace
        )

    def get_replicaset(
        self,
        name: str,
        namespace: str = "default"
    ):

        return self.apps_api.read_namespaced_replica_set(
            name=name,
            namespace=namespace
        )
    
    def list_namespaces(self):

        return [

            namespace.metadata.name

            for namespace

            in

            self.core_api.list_namespace().items

        ]
        
    def list_deployments(

        self,

        namespace: str

    ):

        return self.apps_api.list_namespaced_deployment(

            namespace=namespace

        ).items

    def list_replicasets(

        self,

        namespace: str

    ):

        return self.apps_api.list_namespaced_replica_set(

            namespace=namespace

        ).items

    def list_pods(

        self,

        namespace: str

    ):

        pods = self.core_api.list_namespaced_pod(

            namespace=namespace

        )

        result = []

        for pod in pods.items:

            restart_count = 0

            ready = False

            statuses = (

                pod.status.container_statuses

                or

                []

            )

            if statuses:

                restart_count = sum(

                    c.restart_count

                    for c in statuses

                )

                ready = all(

                    c.ready

                    for c in statuses

                )

            deployment = None

            replicaset = None

            owners = (

                pod.metadata.owner_references

                or

                []

            )

            if owners:

                owner = owners[0]

                if owner.kind == "ReplicaSet":

                    replicaset = owner.name

                    deployment = "-".join(

                        owner.name.split("-")[:-1]

                    )

            result.append(

                {

                    "name":
                    pod.metadata.name,

                    "deployment":
                    deployment,

                    "replicaset":
                    replicaset,

                    "status":
                    pod.status.phase,

                    "ready":
                    ready,

                    "restarts":
                    restart_count

                }

            )

        return result
        