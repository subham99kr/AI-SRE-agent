class APIServerFailurePlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling a Kubernetes API Server incident.

Focus on:

1. API Server availability
2. Authentication failures
3. Authorization failures
4. etcd connectivity
5. Control plane health

Prioritize control plane diagnostics over workload investigation.

Avoid modifying workloads while the control plane is unhealthy.

Verify API Server health is restored before further remediation.
"""


    @staticmethod
    def required_evidence():

        from app.models.evidence_types import (
            EvidenceType
        )

        return [

            EvidenceType.NODES,

            EvidenceType.EVENTS

        ]