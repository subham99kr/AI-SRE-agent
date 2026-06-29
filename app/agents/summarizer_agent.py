import json

from app.models.report import (
    IncidentReport
)

from app.providers.provider_factory import (
    ProviderFactory
)


class SummarizerAgent:

    def __init__(self):

        self.llm = (
            ProviderFactory
            .get_root_cause_provider()
        )

    async def run(

        self,

        cluster_id : str,
        
        namespace: str,

        deployment: str,

        incident_type: str,

        root_cause: str,

        confidence: float,

        risk: str,

        requires_approval: bool,

        rollback_available: bool,

        remediation_steps: list,

        execution_results: list,

        verification_success: bool,

        verification_message: str

    ) -> IncidentReport:

        with open(

            "app/prompts/incident_summary.txt",

            "r",

            encoding="utf-8"

        ) as file:

            template = file.read()

        payload = json.dumps(

            {
                "cluster_id" : cluster_id,
                "namespace": namespace,

                "deployment": deployment,

                "incident_type": incident_type,

                "root_cause": root_cause,

                "confidence": confidence,

                "risk": risk,

                "requires_approval": requires_approval,

                "rollback_available": rollback_available,

                "remediation_steps": remediation_steps,

                "execution_results": execution_results,

                "verification_success": verification_success,

                "verification_message": verification_message

            },

            indent=2

        )

        prompt = template.replace(

            "<<INPUT>>",

            payload

        )

        print("=" * 80)
        print("SUMMARY PROMPT")
        print(prompt)
        print("=" * 80)

        response = await self.llm.generate(
            prompt
        )

        print("=" * 80)
        print("SUMMARY RESPONSE")
        print(response)
        print("=" * 80)

        try:

            data = json.loads(
                response
            )

            return IncidentReport(
                **data
            )

        except Exception:

            return IncidentReport(

                title="Incident Report",

                executive_summary=(
                    "Unable to generate summary."
                ),

                technical_summary=(
                    "The language model returned an invalid response."
                ),

                overall_status="FAILED",

                recommendations=[

                    "Inspect the raw LLM response."

                ]

            )