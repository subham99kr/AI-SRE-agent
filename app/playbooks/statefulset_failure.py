from app.models.evidence_types import (
    EvidenceType
)


class StatefulSetFailurePlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling a StatefulSet incident.

Focus on:

1. StatefulSet rollout failures
2. PersistentVolumeClaim binding issues
3. PersistentVolume availability
4. StorageClass configuration
5. Pod ordinal startup failures
6. Volume mount failures
7. OrderedReady rollout behavior
8. Init container failures
9. Readiness probe failures
10. Stateful application startup issues

Prioritize StatefulSet status, Pod events, PVC status, and storage-related evidence before suggesting application-level debugging.

Prefer Kubernetes-native remediation.

Avoid deleting StatefulSets or PersistentVolumeClaims unless absolutely necessary.

Verify that all StatefulSet replicas become Ready and that PVC_REPORT are successfully Bound.
"""

    @staticmethod
    def required_evidence():

        return [

            EvidenceType.STATEFULSET_REPORT,

            EvidenceType.PODS,

            EvidenceType.EVENTS,

            EvidenceType.POD_REPORT,

            EvidenceType.PVC_REPORT,

            EvidenceType.PV_REPORT,

            EvidenceType.STORAGE_CLASSES,

            EvidenceType.LOGS

        ]