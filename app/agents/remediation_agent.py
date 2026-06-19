import json

from app.providers.provider_factory import (
    ProviderFactory
)


class RemediationAgent:

    def __init__(self):

        self.llm = (
            ProviderFactory
            .get_root_cause_provider()
        )

    async def run(

        self,

        root_cause: str,

        incident_type: str,

        evidence_json: str,

        previous_attempt_summary: str = ""

    ) -> dict:

        with open(

            "app/prompts/remediation.txt",

            "r",

            encoding="utf-8"

        ) as file:

            template = file.read()

        history = previous_attempt_summary

        if not history:

            history = "NONE"

        payload = f"""
        Incident Type

        {incident_type}

        ======================================

        Root Cause

        {root_cause}

        ======================================

        Evidence

        {evidence_json}

        ======================================

        Previous Attempts

        {history}
        """

        prompt = template.replace(
            "<<INPUT>>",
            payload
        )

        print("=" * 80)
        print("REMEDIATION PROMPT")
        print(prompt)
        print("=" * 80)

        response = await self.llm.generate(
            prompt
        )

        print("=" * 80)
        print("REMEDIATION RESPONSE")
        print(response)
        print("=" * 80)

        try:

            result = json.loads(response)
            ##### remove this after test################
            

            return result

        except Exception:

            return {

                "risk": "UNKNOWN",

                "requires_approval": True,

                "approval_reason": (
                    "Unable to determine remediation safety."
                ),

                "rollback_available": False,

                "reasoning":
                "The remediation response could not be parsed.",

                "steps": [

                    {
                        "description":
                        "Unable to parse remediation.",

                        "kubectl_command": None
                    }

                ]
            }