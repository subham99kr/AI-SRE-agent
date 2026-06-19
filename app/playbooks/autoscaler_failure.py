class AutoscalerFailurePlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling a Horizontal Pod Autoscaler incident.

Focus on:

1. HPA configuration
2. Metrics availability
3. CPU and Memory targets
4. Replica scaling events
5. Metrics Server health

Prioritize HPA events and metrics.

Avoid manual scaling until autoscaler issues are understood.

Verify automatic scaling resumes successfully.
"""

    @staticmethod
    def required_evidence():

        from app.models.evidence_types import (
            EvidenceType
        )

        return [

            EvidenceType.METRICS,

            EvidenceType.PODS

        ]