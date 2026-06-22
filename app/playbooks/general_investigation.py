class GeneralInvestigationPlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are investigating a Kubernetes workload that does not exhibit any obvious Kubernetes-native failure.

The deployment is currently running and no deterministic Kubernetes failure (such as CrashLoopBackOff, ImagePullBackOff, Pending, OOMKilled or FailedScheduling) has been detected.

Investigate the workload using all available evidence.

Focus on:

1. CPU utilization
2. Memory utilization
3. HTTP request rate
4. HTTP error rate
5. Request latency
6. Application logs
7. Pod configuration

Do not assume an incident exists.

If the collected evidence indicates the deployment is healthy, explicitly conclude that no active incident is present.

Only identify an application-level incident when the supplied evidence supports it.
"""

    @staticmethod
    def required_evidence():

        from app.models.evidence_types import (
            EvidenceType
        )

        return [

            EvidenceType.LOGS,

            EvidenceType.POD_REPORT,

            EvidenceType.PROMETHEUS_METRICS

        ]