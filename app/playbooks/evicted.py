class EvictedPlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling an Evicted Pod incident.

Focus on:

1. Node memory pressure
2. Node disk pressure
3. Ephemeral storage exhaustion
4. Resource limits
5. Node health

Prioritize node conditions and eviction events.

Avoid restarting workloads without resolving node pressure.

Verify Pods are successfully rescheduled.
"""

    @staticmethod
    def required_evidence():

        from app.models.evidence_types import (
            EvidenceType
        )

        return [

            EvidenceType.NODES,

            EvidenceType.NODE_REPORT,

            EvidenceType.PODS,

            EvidenceType.EVENTS

        ]