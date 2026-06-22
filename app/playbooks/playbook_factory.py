from app.playbooks.api_server_failure import (
    APIServerFailurePlaybook
)

from app.playbooks.autoscaler_failure import (
    AutoscalerFailurePlaybook
)

from app.playbooks.container_config_error import (
    ContainerConfigErrorPlaybook
)

from app.playbooks.container_create_error import (
    ContainerCreateErrorPlaybook
)

from app.playbooks.crashloop import (
    CrashLoopPlaybook
)

from app.playbooks.db_connectivity import (
    DBConnectivityPlaybook
)

from app.playbooks.deployment_regression import (
    DeploymentRegressionPlaybook
)

from app.playbooks.disk_pressure import (
    DiskPressurePlaybook
)

from app.playbooks.dns_failure import (
    DNSFailurePlaybook
)

from app.playbooks.evicted import (
    EvictedPlaybook
)

from app.playbooks.high_cpu import (
    HighCPUPlaybook
)

from app.playbooks.high_error_rate import (
    HighErrorRatePlaybook
)

from app.playbooks.high_memory import (
    HighMemoryPlaybook
)

from app.playbooks.image_pull import (
    ImagePullPlaybook
)

from app.playbooks.ingress_failure import (
    IngressFailurePlaybook
)

from app.playbooks.init_container_failure import (
    InitContainerFailurePlaybook
)

from app.playbooks.latency import (
    LatencyPlaybook
)

from app.playbooks.network_latency import (
    NetworkLatencyPlaybook
)

from app.playbooks.network_policy_failure import (
    NetworkPolicyFailurePlaybook
)

from app.playbooks.node_failure import (
    NodeFailurePlaybook
)

from app.playbooks.oomkill import (
    OOMKillPlaybook
)

from app.playbooks.pending import (
    PendingPlaybook
)

from app.playbooks.service_failure import (
    ServiceFailurePlaybook
)

from app.playbooks.statefulset_failure import (
    StatefulSetFailurePlaybook
)

from app.playbooks.storage_failure import (
    StorageFailurePlaybook
)

from app.playbooks.tls_failure import (
    TLSFailurePlaybook
)

from app.playbooks.unschedulable import (
    UnschedulablePlaybook
)
from app.playbooks.general_investigation import (
    GeneralInvestigationPlaybook
)


class PlaybookFactory:

    PLAYBOOKS = {

        "CRASH_LOOP": CrashLoopPlaybook,

        "IMAGE_PULL": ImagePullPlaybook,

        "PENDING": PendingPlaybook,

        "OOM_KILLED": OOMKillPlaybook,

        "CONTAINER_CONFIG_ERROR":
        ContainerConfigErrorPlaybook,

        "CONTAINER_CREATE_ERROR":
        ContainerCreateErrorPlaybook,

        "INIT_CONTAINER_FAILURE":
        InitContainerFailurePlaybook,

        "EVICTED":
        EvictedPlaybook,

        "UNSCHEDULABLE":
        UnschedulablePlaybook,

        "NODE_FAILURE":
        NodeFailurePlaybook,

        "STORAGE_FAILURE":
        StorageFailurePlaybook,

        "SERVICE_FAILURE":
        ServiceFailurePlaybook,

        "DNS_FAILURE":
        DNSFailurePlaybook,

        "INGRESS_FAILURE":
        IngressFailurePlaybook,

        "NETWORK_POLICY_FAILURE":
        NetworkPolicyFailurePlaybook,

        "HIGH_CPU":
        HighCPUPlaybook,

        "HIGH_MEMORY":
        HighMemoryPlaybook,

        "DEPLOYMENT_REGRESSION":
        DeploymentRegressionPlaybook,

        "DB_CONNECTIVITY":
        DBConnectivityPlaybook,

        "STATEFULSET_FAILURE":
        StatefulSetFailurePlaybook,

        "DISK_PRESSURE":
        DiskPressurePlaybook,

        "LATENCY":
        LatencyPlaybook,

        "HIGH_ERROR_RATE":
        HighErrorRatePlaybook,

        "NETWORK_LATENCY":
        NetworkLatencyPlaybook,

        "AUTOSCALER_FAILURE":
        AutoscalerFailurePlaybook,

        "TLS_FAILURE":
        TLSFailurePlaybook,

        "API_SERVER_FAILURE":
        APIServerFailurePlaybook,

        "UNKNOWN":
        GeneralInvestigationPlaybook,

    }

    @classmethod
    def get_playbook(
        cls,
        incident_type: str
    ):

        playbook = cls.PLAYBOOKS.get(
            incident_type
        )

        if playbook:

            return playbook()

        return None