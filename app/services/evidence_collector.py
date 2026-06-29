from app.models.evidence import (
    Evidence,
    PodLog
)

from app.models.evidence_types import (
    EvidenceType
)

from app.tools.kubernetes_reader import (
    KubernetesTool
)

from app.tools.prometheus_reader import (
    PrometheusTool
)


class EvidenceCollector:

    def __init__(
        self,
        cluster_id: str
    ):

        self.k8s = KubernetesTool(cluster_id)

        self.prometheus = PrometheusTool(cluster_id)

        self.collectors = {

            EvidenceType.LOGS:
                self._collect_logs,

            EvidenceType.POD_REPORT:
                self._collect_pod_reports,

            EvidenceType.PROMETHEUS_METRICS:
                self._collect_prometheus_metrics

        }

    def collect(

        self,

        evidence: Evidence,

        required_evidence: list[EvidenceType]

    ) -> Evidence:

        for evidence_type in required_evidence:

            collector = self.collectors.get(
                evidence_type
            )

            if collector:

                collector(
                    evidence
                )

        return evidence

    ####################################################################
    #
    # Logs
    #
    ####################################################################

    def _collect_logs(
        self,
        evidence: Evidence
    ):

        #
        # Already collected
        #

        if evidence.logs:

            return

        MAX_LOG_CHARS = 8000

        for pod in evidence.pods:

            pod_name = pod["name"]

            try:

                waiting_reason = (
                    pod.get("waiting_reason")
                )

                restart_count = (
                    pod.get(
                        "restarts",
                        0
                    )
                )

                #
                # Image Pull
                #

                if waiting_reason in [

                    "ImagePullBackOff",

                    "ErrImagePull"

                ]:

                    evidence.logs.append(

                        PodLog(

                            pod=pod_name,

                            current_logs=(
                                "Container never started. "
                                "Logs unavailable."
                            ),

                            previous_logs=None

                        )

                    )

                    continue

                #
                # CrashLoop / Restarted Container
                #

                if restart_count > 0:

                    previous_logs = (

                        self.k8s.get_previous_logs(

                            pod_name=pod_name,

                            namespace=evidence.namespace

                        )

                    )

                    if isinstance(
                        previous_logs,
                        bytes
                    ):

                        previous_logs = (
                            previous_logs.decode(
                                "utf-8",
                                errors="ignore"
                            )
                        )

                    previous_logs = str(
                        previous_logs
                    )

                    if previous_logs.strip() == "b''":

                        previous_logs = ""

                    if (

                        "unable to retrieve"

                        in previous_logs.lower()

                    ):

                        previous_logs = (
                            "Container terminated before "
                            "logs could be collected."
                        )

                    if not previous_logs.strip():

                        previous_logs = (
                            "No logs emitted before "
                            "container exit."
                        )

                    #
                    # Keep only tail if logs are huge
                    #

                    if len(previous_logs) > MAX_LOG_CHARS:

                        previous_logs = (

                            "... LOG TRUNCATED ...\n\n"

                            + previous_logs[-MAX_LOG_CHARS:]

                        )

                    evidence.logs.append(

                        PodLog(

                            pod=pod_name,

                            current_logs=None,

                            previous_logs=previous_logs

                        )

                    )

                    continue

                #
                # Running container
                #

                current_logs = (

                    self.k8s.get_pod_logs(

                        pod_name=pod_name,

                        namespace=evidence.namespace,

                        tail_lines=300

                    )

                )

                if isinstance(
                    current_logs,
                    bytes
                ):

                    current_logs = (
                        current_logs.decode(
                            "utf-8",
                            errors="ignore"
                        )
                    )

                current_logs = str(
                    current_logs
                )

                if current_logs.strip() == "b''":

                    current_logs = ""

                if not current_logs.strip():

                    current_logs = (
                        "No logs available."
                    )

                if len(current_logs) > MAX_LOG_CHARS:

                    current_logs = (

                        "... LOG TRUNCATED ...\n\n"

                        + current_logs[-MAX_LOG_CHARS:]

                    )

                evidence.logs.append(

                    PodLog(

                        pod=pod_name,

                        current_logs=current_logs,

                        previous_logs=None

                    )

                )

            except Exception as e:

                evidence.logs.append(

                    PodLog(

                        pod=pod_name,

                        current_logs=(
                            f"Failed to fetch logs: {e}"
                        ),

                        previous_logs=None

                    )

                )

    ####################################################################
    #
    # Pod Report
    #
    ####################################################################

    def _collect_pod_reports(
        self,
        evidence: Evidence
    ):

        reports = evidence.reports.setdefault(

            EvidenceType.POD_REPORT.value,

            []

        )

        for pod in evidence.pods:

            pod_obj = self.k8s.get_pod(

                pod["name"],

                evidence.namespace

            )

            report = []

            report.append(

                f"Pod: {pod_obj.metadata.name}"

            )

            report.append(

                f"Phase: {pod_obj.status.phase}"

            )

            report.append(

                f"Node: {pod_obj.spec.node_name}"

            )

            report.append("")

            report.append("Conditions:")

            if pod_obj.status.conditions:

                for condition in pod_obj.status.conditions:

                    report.append(

                        f"- {condition.type}: "

                        f"{condition.status}"

                    )

                    if condition.reason:

                        report.append(

                            f"  Reason: "

                            f"{condition.reason}"

                        )

                    if condition.message:

                        report.append(

                            f"  {condition.message}"

                        )

            report.append("")

            report.append("Containers:")

            for container in pod_obj.spec.containers:

                report.append(

                    f"- {container.name}"

                )

                report.append(

                    f"  Image: "

                    f"{container.image}"

                )

                report.append(

                    f"  Command: "

                    f"{container.command}"

                )

                report.append(

                    f"  Args: "

                    f"{container.args}"

                )

            reports.append(

                "\n".join(report)

            )

####################################################################
#
# Prometheus Metrics
#
####################################################################

    def _collect_prometheus_metrics(
        self,
        evidence: Evidence
    ):

        if evidence.metrics:
            return

        metrics = {

            "cpu": {},

            "memory": {},

            "request_count": {},

            "request_rate": {},

            "error_rate": {},

            "latency_average": {},

            "latency_p95": None

        }

        ############################################################
        # CPU
        ############################################################

        try:

            for item in self.prometheus.cpu_usage(
                evidence.namespace
            ):

                metrics["cpu"][
                    item["metric"]["pod"]
                ] = float(
                    item["value"][1]
                )

        except Exception as e:

            metrics["cpu_error"] = str(e)

        ############################################################
        # Memory
        ############################################################

        try:

            for item in self.prometheus.memory_usage(
                evidence.namespace
            ):

                metrics["memory"][
                    item["metric"]["pod"]
                ] = int(
                    float(
                        item["value"][1]
                    )
                )

        except Exception as e:

            metrics["memory_error"] = str(e)

        ############################################################
        # Restart Count
        ############################################################

        try:

            for item in self.prometheus.restart_count(
                evidence.namespace
            ):

                metrics["restarts"][
                    item["metric"]["pod"]
                ] = int(
                    float(
                        item["value"][1]
                    )
                )

        except Exception as e:

            metrics["restart_error"] = str(e)

        ############################################################
        # Request Rate
        ############################################################

        try:

            for item in self.prometheus.request_rate(
                evidence.deployment
            ):

                handler = item["metric"].get(
                    "handler",
                    "unknown"
                )

                metrics["request_rate"][
                    handler
                ] = float(
                    item["value"][1]
                )

        except Exception as e:

            metrics["request_rate_error"] = str(e)

        ############################################################
        # Request Count
        ############################################################

        try:

            requests = self.prometheus.request_count(
                evidence.deployment
            )

            for item in requests:

                handler = item["metric"].get(
                    "handler",
                    "unknown"
                )

                metrics["request_count"][
                    handler
                ] = int(
                    float(
                        item["value"][1]
                    )
                )

        except Exception as e:

            metrics["request_count_error"] = str(e)

        ############################################################
        # Error Rate
        ############################################################

        try:

            errors = self.prometheus.error_rate(
                evidence.deployment
            )

            for item in errors:

                handler = item["metric"].get(
                    "handler",
                    "unknown"
                )

                metrics["error_rate"][
                    handler
                ] = float(
                    item["value"][1]
                )

        except Exception as e:

            metrics["error_rate_error"] = str(e)

        ############################################################
        # Average Latency
        ############################################################

        try:

            latency = self.prometheus.latency_average(
                evidence.deployment
            )

            for item in latency:

                handler = item["metric"].get(
                    "handler",
                    "unknown"
                )

                metrics["latency_average"][
                    handler
                ] = float(
                    item["value"][1]
                )

        except Exception as e:

            metrics["latency_average_error"] = str(e)

        ############################################################
        # P95 Latency
        ############################################################

        try:

            latency = self.prometheus.latency_p95(
                evidence.deployment
            )

            if latency:

                metrics["latency_p95"] = float(
                    latency[0]["value"][1]
                )

        except Exception as e:

            metrics["latency_error"] = str(e)

        evidence.metrics = metrics