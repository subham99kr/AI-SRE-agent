class ContainerCreateErrorPlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling a CreateContainerError incident.

Focus on:

1. Invalid container commands
2. Invalid entrypoints
3. Missing files or directories
4. Volume mount failures
5. Permission issues

Prioritize Pod events and container configuration.

Suggest correcting container configuration before restarting.

Verify the container reaches the Running state.
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

            EvidenceType.POD_DESCRIPTION

        ]