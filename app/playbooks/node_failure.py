class NodeFailurePlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling a Node failure.

Focus on:

1. Node readiness
2. Node pressure conditions
3. Kubelet failures
4. Network partition
5. Node resource exhaustion

Prioritize node status and events.

Avoid unnecessary workload changes if the issue is infrastructure related.

Verify the node returns to Ready status.
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