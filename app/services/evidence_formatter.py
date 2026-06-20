import json

from app.models.evidence import (
    Evidence
)


class EvidenceFormatter:

    @staticmethod
    def format(
        evidence: Evidence
    ) -> str:

        sections = []

        # =====================================================
        # Deployment
        # =====================================================

        sections.append("=" * 80)
        sections.append("DEPLOYMENT")
        sections.append("=" * 80)

        sections.append(
            f"Namespace : {evidence.namespace}"
        )

        sections.append(
            f"Deployment : {evidence.deployment}"
        )

        sections.append("")

        if evidence.deployment_spec:

            sections.append("Deployment Spec")

            sections.append(

                json.dumps(

                    evidence.deployment_spec,

                    indent=2,

                    default=str

                )

            )

        # =====================================================
        # Pods
        # =====================================================

        sections.append("")
        sections.append("=" * 80)
        sections.append("PODS")
        sections.append("=" * 80)

        sections.append(

            json.dumps(

                evidence.pods,

                indent=2,

                default=str

            )

        )

        # =====================================================
        # Reports
        # =====================================================

        if evidence.reports:

            sections.append("")
            sections.append("=" * 80)
            sections.append("REPORTS")
            sections.append("=" * 80)

            for report_type, reports in evidence.reports.items():

                sections.append("")
                sections.append(report_type.upper())
                sections.append("-" * 40)

                for report in reports:

                    sections.append(report)
                    sections.append("")

        # =====================================================
        # Logs
        # =====================================================

        if evidence.logs:

            sections.append("")
            sections.append("=" * 80)
            sections.append("LOGS")
            sections.append("=" * 80)

            for log in evidence.logs:

                sections.append(
                    f"Pod : {log.pod}"
                )

                if log.current_logs:

                    sections.append("")
                    sections.append("Current Logs")
                    sections.append(log.current_logs)

                if log.previous_logs:

                    sections.append("")
                    sections.append("Previous Logs")
                    sections.append(log.previous_logs)

                sections.append("")

        # =====================================================
        # Events
        # =====================================================

        if evidence.events:

            sections.append("=" * 80)
            sections.append("EVENTS")
            sections.append("=" * 80)

            sections.append(

                json.dumps(

                    evidence.events,

                    indent=2,

                    default=str

                )

            )

        # =====================================================
        # Metrics
        # =====================================================

        if evidence.metrics:

            sections.append("")
            sections.append("=" * 80)
            sections.append("METRICS")
            sections.append("=" * 80)

            sections.append(

                json.dumps(

                    evidence.metrics,

                    indent=2,

                    default=str

                )

            )

        return "\n".join(
            sections
        )