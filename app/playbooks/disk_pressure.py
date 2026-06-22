class DiskPressurePlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling a Disk Pressure incident.

Focus on:

1. Node disk utilization
2. Ephemeral storage usage
3. Log growth
4. Image garbage collection
5. Disk pressure conditions

Prioritize node conditions and storage metrics.

Avoid restarting workloads until storage pressure is resolved.

Verify disk pressure clears and workloads stabilize.
"""

    @staticmethod
    def required_evidence():

        from app.models.evidence_types import (
            EvidenceType
        )

        return [

            EvidenceType.NODES,

            EvidenceType.PROMETHEUS_METRICS

        ]