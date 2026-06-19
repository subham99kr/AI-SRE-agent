class PendingPlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling a Pending Pod incident.

Focus on:

1. Insufficient CPU resources
2. Insufficient Memory resources
3. Node scheduling failures
4. Node affinity or anti-affinity rules
5. Taints and tolerations
6. ResourceQuota restrictions
7. PersistentVolumeClaim binding issues
8. Node readiness

Prioritize scheduler events over speculation.

Suggest Kubernetes-native remediation.

Avoid restarting Pods unless scheduling has already succeeded.

Verify that the Pod transitions from Pending to Running after remediation.
"""


    @staticmethod
    def required_evidence():

        from app.models.evidence_types import (
            EvidenceType
        )

        return [

            EvidenceType.PODS,

            EvidenceType.EVENTS,

            EvidenceType.POD_DESCRIPTION,

            EvidenceType.NODES,

            EvidenceType.NODE_DESCRIPTION,

            EvidenceType.PVCS

        ]