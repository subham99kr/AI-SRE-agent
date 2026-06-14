from app.models.report import (
    IncidentReport
)


class ReportService:

    @staticmethod
    def format_terminal(
        report: IncidentReport
    ) -> str:

        output = []

        output.append("=" * 80)
        output.append(report.title)
        output.append("=" * 80)

        output.append("")
        output.append("EXECUTIVE SUMMARY")
        output.append("-" * 80)
        output.append(report.executive_summary)

        output.append("")
        output.append("TECHNICAL SUMMARY")
        output.append("-" * 80)
        output.append(report.technical_summary)

        output.append("")
        output.append("OVERALL STATUS")
        output.append("-" * 80)
        output.append(report.overall_status)

        output.append("")
        output.append("RECOMMENDATIONS")
        output.append("-" * 80)

        for recommendation in report.recommendations:

            output.append(
                f"• {recommendation}"
            )

        output.append("=" * 80)

        return "\n".join(output)