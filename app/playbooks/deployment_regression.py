class DeploymentRegressionPlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling a Deployment Regression incident.

Focus on:

1. Recently deployed images
2. Recent configuration changes
3. Environment variable modifications
4. Deployment rollout history
5. ReplicaSet revisions

Prioritize recent deployment changes over infrastructure issues.

Suggest Kubernetes-native rollback or deployment correction when appropriate.

Verify that the deployment becomes Available after remediation.
"""

    @staticmethod
    def required_evidence():

        from app.models.evidence_types import (
            EvidenceType
        )

        return [

            EvidenceType.DEPLOYMENT,

            EvidenceType.REPLICASET_REPORT,

            EvidenceType.PODS,

            EvidenceType.EVENTS

        ]