class NetworkLatencyPlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling a Network Latency incident.

Focus on:

1. Pod-to-Pod communication
2. Service networking
3. DNS latency
4. Node networking
5. External connectivity

Prioritize network metrics and connectivity tests.

Avoid modifying application code unless networking is confirmed healthy.

Verify network latency returns to normal.
"""

    @staticmethod
    def required_evidence():

        from app.models.evidence_types import (
            EvidenceType
        )

        return [

            EvidenceType.PROMETHEUS_METRICS

        ]