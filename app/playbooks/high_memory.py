class HighMemoryPlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling a High Memory utilization incident.

Focus on:

1. Memory requests and limits
2. Memory leaks
3. Excessive cache usage
4. Application memory growth
5. Resource pressure

Prioritize memory metrics and container resource usage.

Avoid restarting workloads without identifying the underlying cause.

Verify memory utilization stabilizes after remediation.
"""
    @staticmethod
    def required_evidence():

        from app.models.evidence_types import (
            EvidenceType
        )

        return [

            EvidenceType.PODS,

            EvidenceType.PROMETHEUS_METRICS

        ]