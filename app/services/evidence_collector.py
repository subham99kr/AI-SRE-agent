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


class EvidenceCollector:

    def __init__(self):

        self.k8s = KubernetesTool()

        self.collectors = {

            EvidenceType.LOGS:
                self._collect_logs,

            EvidenceType.POD_REPORT:
                self._collect_pod_reports

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