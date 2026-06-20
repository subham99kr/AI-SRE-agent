class OOMKillPlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling an OOMKilled incident.

Focus on:

1. Memory limit exceeded
2. Memory requests and limits
3. Memory leaks
4. Excessive application memory usage
5. Node memory pressure

Prioritize Kubernetes termination reasons and exit codes.

Prefer adjusting resource limits only when evidence supports it.

Avoid suggesting unrelated networking or image fixes.

Verify the container no longer terminates with OOMKilled.
"""

    @staticmethod
    def required_evidence():

        from app.models.evidence_types import (
            EvidenceType
        )

        return [

            EvidenceType.DEPLOYMENT,

            EvidenceType.PODS,

            EvidenceType.EVENTS,

            EvidenceType.LOGS,

            EvidenceType.POD_REPORT

        ]