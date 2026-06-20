class IngressFailurePlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling an Ingress failure.

Focus on:

1. Ingress configuration
2. Backend service availability
3. Ingress controller health
4. TLS configuration
5. Routing rules

Prioritize Ingress events and backend connectivity.

Avoid restarting application Pods unless routing is confirmed healthy.

Verify external traffic successfully reaches the application.
"""

    @staticmethod
    def required_evidence():

        from app.models.evidence_types import (
            EvidenceType
        )

        return [

            EvidenceType.INGRESS,

            EvidenceType.SERVICE_REPORT,

            EvidenceType.ENDPOINT_REPORT

        ]