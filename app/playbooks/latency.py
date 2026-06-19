class LatencyPlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling a High Latency incident.

Focus on:

1. Service response times
2. Backend dependency latency
3. Network latency
4. Resource saturation
5. Request queue buildup

Prioritize latency metrics before recommending scaling.

Avoid assuming application bugs without supporting evidence.

Verify response times return to normal.
"""

    @staticmethod
    def required_evidence():

        from app.models.evidence_types import (
            EvidenceType
        )

        return [

            EvidenceType.METRICS

        ]