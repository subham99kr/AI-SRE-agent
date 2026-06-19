class HighErrorRatePlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling a High Error Rate incident.

Focus on:

1. HTTP 5xx responses
2. Application exceptions
3. Backend failures
4. Dependency outages
5. Recent deployments

Prioritize application logs and service metrics.

Avoid restarting workloads unless evidence indicates recovery is likely.

Verify the error rate returns to acceptable levels.
"""

    @staticmethod
    def required_evidence():

        from app.models.evidence_types import (
            EvidenceType
        )

        return [

            EvidenceType.METRICS,

            EvidenceType.LOGS

        ]