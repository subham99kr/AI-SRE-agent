class TLSFailurePlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling a TLS or Certificate incident.

Focus on:

1. Expired certificates
2. Invalid certificates
3. TLS configuration
4. Secret references
5. Ingress TLS settings

Prioritize certificate validation and TLS events.

Avoid application debugging until TLS is functioning correctly.

Verify secure connections are successfully established.
"""

    @staticmethod
    def required_evidence():

        from app.models.evidence_types import (
            EvidenceType
        )

        return [

            EvidenceType.INGRESS,

            EvidenceType.SECRETS,
            
            EvidenceType.SERVICES,

        ]