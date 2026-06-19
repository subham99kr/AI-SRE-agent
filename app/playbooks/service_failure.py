class ServiceFailurePlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling a Kubernetes Service failure.

Focus on:

1. Service selectors
2. Endpoint availability
3. Label mismatches
4. Port configuration
5. ClusterIP accessibility

Prioritize Service and Endpoint resources.

Avoid application-level debugging until Service routing is validated.

Verify traffic reaches healthy Pods.
"""

    @staticmethod
    def required_evidence():

        from app.models.evidence_types import (
            EvidenceType
        )

        return [

            EvidenceType.SERVICES,

            EvidenceType.ENDPOINTS,

            EvidenceType.PODS,

            EvidenceType.EVENTS,

            EvidenceType.PODS

        ]