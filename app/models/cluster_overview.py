from pydantic import BaseModel


class PodOverview(BaseModel):

    name: str

    deployment: str | None

    replicaset: str | None

    status: str

    ready: bool

    restarts: int


class NamespaceOverview(BaseModel):

    name: str

    pod_count: int

    running_pods: int

    failed_pods: int

    deployment_count: int

    replicaset_count: int

    pods: list[PodOverview]


class ClusterOverview(BaseModel):

    cluster_id: str

    status: str

    namespaces: list[NamespaceOverview]