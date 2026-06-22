class HighCPUPlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling a High CPU utilization incident.

Focus on:

1. CPU resource requests and limits
2. CPU throttling
3. Runaway processes
4. High request load
5. Infinite loops or inefficient workloads

Prioritize resource metrics before recommending scaling.

Avoid restarting workloads unless evidence supports it.

Verify CPU utilization returns to a healthy level.
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