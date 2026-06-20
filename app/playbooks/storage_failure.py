class StorageFailurePlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling a Storage-related incident.

Focus on:

1. PersistentVolumeClaims
2. PersistentVolumes
3. Volume attachment
4. Mount failures
5. StorageClass issues

Prioritize PVC and PV events.

Avoid restarting workloads until storage is healthy.

Verify volumes are successfully mounted.
"""

    @staticmethod
    def required_evidence():

        from app.models.evidence_types import (
            EvidenceType
        )

        return [

            EvidenceType.PODS,

            EvidenceType.EVENTS,

            EvidenceType.PVC_REPORT,

            EvidenceType.PV_REPORT,

            EvidenceType.STORAGE_CLASSES

        ]