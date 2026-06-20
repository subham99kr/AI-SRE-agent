class DNSFailurePlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling a DNS Resolution incident.

Focus on:

1. CoreDNS health
2. DNS resolution failures
3. Service discovery
4. Cluster DNS configuration
5. Network connectivity

Prioritize DNS lookup failures over application-level issues.

Avoid modifying application configuration unless DNS is confirmed healthy.

Verify DNS resolution succeeds after remediation.
"""

    @staticmethod
    def required_evidence():

        from app.models.evidence_types import (
            EvidenceType
        )

        return [

            EvidenceType.SERVICE_REPORT,

            EvidenceType.ENDPOINT_REPORT,

            EvidenceType.PODS,

            EvidenceType.EVENTS

        ]