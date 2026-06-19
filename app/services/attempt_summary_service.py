class AttemptSummaryService:

    MAX_PREVIOUS_ATTEMPTS = 5

    def build(
        self,
        attempts: list[dict]
    ) -> list[str]:

        summaries = []

        #
        # Only latest N attempts
        #

        attempts = attempts[
            -self.MAX_PREVIOUS_ATTEMPTS:
        ]

        for context in attempts:

            incident = context["incident"]

            remediation = context["remediation"]

            verification = context["verification"]

            executions = context["executions"]

            lines = []

            lines.append(
                "=" * 60
            )

            lines.append(
                f"Attempt #{incident.attempt_number}"
            )

            lines.append("")

            lines.append(
                f"Status: {incident.status}"
            )

            lines.append("")

            lines.append(
                "Root Cause:"
            )

            lines.append(
                incident.root_cause
            )

            lines.append("")

            lines.append(
                "Remediation:"
            )

            for step in remediation.steps:

                lines.append(
                    f"- {step['description']}"
                )

            lines.append("")

            lines.append(
                "Execution:"
            )

            for result in executions:

                status = (
                    "SUCCESS"
                    if result.success
                    else "FAILED"
                )

                lines.append(

                    f"- Step {result.step}: "

                    f"{status}"

                )

            lines.append("")

            lines.append(
                "Verification:"
            )

            lines.append(
                verification.message
            )

            if incident.approval_reason:

                lines.append("")

                lines.append(
                    "Operator Feedback:"
                )

                lines.append(
                    incident.approval_reason
                )

            #
            # Lessons Learned
            #

            lines.append("")

            lines.append(
                "Lessons Learned:"
            )

            if verification.success:

                lines.append(
                    "Previous remediation succeeded."
                )

            else:

                lines.append(

                    "Previous remediation failed."

                )

                lines.append(

                    "Avoid repeating the same "

                    "approach unless new "

                    "evidence strongly supports it."

                )

            summaries.append(

                "\n".join(lines)

            )

        return summaries