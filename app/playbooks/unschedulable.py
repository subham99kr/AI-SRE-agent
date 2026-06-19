class UnschedulablePlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling an Unschedulable Pod incident.

Focus on:

1. Insufficient cluster resources
2. Taints and tolerations
3. Node affinity
4. Pod affinity
5. Resource requests
6. Node availability

Prioritize scheduler events.

Avoid deleting Pods.

Verify the scheduler successfully places the Pod on a node.
"""

    @staticmethod
    def required_evidence():

        from app.models.evidence_types import (
            EvidenceType
        )

        return [

            EvidenceType.NODES,

            EvidenceType.NODE_DESCRIPTION,

            EvidenceType.PODS,

            EvidenceType.EVENTS

        ]