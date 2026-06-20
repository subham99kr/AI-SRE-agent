from enum import StrEnum


class EvidenceType(StrEnum):

    #
    # Initial Investigation
    #

    DEPLOYMENT = "deployment"

    PODS = "pods"

    EVENTS = "events"

    #
    # Adaptive Investigation
    #

    LOGS = "logs"

    POD_REPORT = "pod_report"

    NODE_REPORT = "node_report"

    PVC_REPORT = "pvc_report"

    PV_REPORT = "pv_report"

    STORAGE_CLASS_REPORT = "storage_class_report"

    SERVICE_REPORT = "service_report"

    ENDPOINT_REPORT = "endpoint_report"

    CONFIGMAP_REPORT = "configmap_report"

    SECRET_REPORT = "secret_report"

    REPLICASET_REPORT = "replicaset_report"

    STATEFULSET_REPORT = "statefulset_report"

    NETWORK_POLICY_REPORT = "network_policy_report"

    INGRESS_REPORT = "ingress_report"

    METRICS = "metrics"

    PROMETHEUS = "prometheus"

    GRAFANA = "grafana"