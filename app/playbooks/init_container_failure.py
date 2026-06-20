class InitContainerFailurePlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling an Init Container failure.

Focus on:

1. Init container exit codes
2. Failed initialization scripts
3. Missing dependencies
4. Configuration failures
5. Secret or ConfigMap issues

Prioritize init container logs over application logs.

Avoid diagnosing the main application container until initialization succeeds.

Verify all init containers complete successfully.
"""

    @staticmethod
    def required_evidence():

        from app.models.evidence_types import (
            EvidenceType
        )

        return [

            EvidenceType.PODS,

            EvidenceType.EVENTS,

            EvidenceType.LOGS,

            EvidenceType.POD_REPORT

        ]