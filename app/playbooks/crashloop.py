class CrashLoopPlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling a CrashLoopBackOff incident.

Focus on:

1. Container exit codes
2. Restart counts
3. Application startup failures
4. Configuration errors
5. Missing secrets
6. Environment variables
7. Health probe failures

Suggest Kubernetes-specific remediation steps.

Do not suggest image pull fixes unless evidence supports it.
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

            EvidenceType.POD_DESCRIPTION,

            EvidenceType.CONFIGMAPS,

            EvidenceType.SECRETS

        ]