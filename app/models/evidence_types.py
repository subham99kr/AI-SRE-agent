class EvidenceType(StrEnum):

    #
    # Workloads
    #

    DEPLOYMENT = "deployment"

    DEPLOYMENTS = "deployments"

    PODS = "pods"

    POD_DESCRIPTION = "pod_description"

    EVENTS = "events"

    LOGS = "logs"

    REPLICASETS = "replicasets"

    STATEFULSETS = "statefulsets"

    DAEMONSETS = "daemonsets"

    JOBS = "jobs"

    CRONJOBS = "cronjobs"

    #
    # Networking
    #

    SERVICES = "services"

    ENDPOINTS = "endpoints"

    INGRESS = "ingress"

    NETWORK_POLICIES = "network_policies"

    DNS = "dns"

    #
    # Storage
    #

    PVCS = "pvcs"

    PVS = "pvs"

    STORAGE_CLASSES = "storage_classes"

    #
    # Configuration
    #

    CONFIGMAPS = "configmaps"

    SECRETS = "secrets"

    #
    # Cluster
    #

    NODES = "nodes"

    NODE_DESCRIPTION = "node_description"

    NAMESPACES = "namespaces"

    HPA = "horizontal_pod_autoscaler"

    #
    # Observability
    #

    METRICS = "metrics"

    PROMETHEUS = "prometheus"

    GRAFANA = "grafana"