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

        evidence_json: str

    ) -> dict:

        with open(

            "app/prompts/remediation.txt",

            "r",

            encoding="utf-8"

        ) as file:

            template = file.read()

        payload = f"""
Incident Type:
{incident_type}

Root Cause:
{root_cause}

Evidence:
{evidence_json}
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

            return json.loads(response)

        except Exception:

            return {

                "risk": "UNKNOWN", 

                "rollback_available": False,

                "steps": [

                    {

                        "description":
                        "Unable to parse remediation.",

                        "kubectl_command": None

                    }

                ]
            }