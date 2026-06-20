class NetworkPolicyFailurePlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling a NetworkPolicy incident.

Focus on:

1. NetworkPolicy rules
2. Blocked ingress traffic
3. Blocked egress traffic
4. Namespace isolation
5. Pod communication failures

Prioritize NetworkPolicy configuration before investigating applications.

Avoid disabling NetworkPolicies unless absolutely necessary.

Verify Pod-to-Pod communication succeeds after remediation.
"""

    @staticmethod
    def required_evidence():

        from app.models.evidence_types import (
            EvidenceType
        )

        return [

            EvidenceType.NETWORK_POLICY_REPORT,

            EvidenceType.PODS,

            EvidenceType.EVENTS,

            EvidenceType.SERVICE_REPORT

        ]