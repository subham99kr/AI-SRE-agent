class ContainerConfigErrorPlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling a CreateContainerConfigError incident.

Focus on:

1. Missing ConfigMaps
2. Missing Secrets
3. Invalid environment variables
4. Incorrect volume references
5. Invalid container configuration

Prioritize Deployment configuration and Pod events.

Suggest fixing configuration rather than restarting workloads.

Verify that the container starts successfully after configuration changes.
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

            EvidenceType.CONFIGMAPS,

            EvidenceType.SECRETS,

            EvidenceType.POD_DESCRIPTION

        ]