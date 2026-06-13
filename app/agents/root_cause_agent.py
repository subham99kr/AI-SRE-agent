import json

from app.providers.provider_factory import (
    ProviderFactory
)


class RootCauseAgent:

    def __init__(self):

        self.llm = (
            ProviderFactory
            .get_root_cause_provider()
        )

    async def run(
        self,
        evidence_json: str,
        incident_type: str,
        playbook_context: str
    ) -> dict:

        with open(
            "app/prompts/root_cause.txt",
            "r",
            encoding="utf-8"
        ) as file:

            template = file.read()

        prompt = template.replace(
            "<<INCIDENT>>",
            (
                f"\nDetected Incident Type:\n"
                f"{incident_type}\n\n"
                f"Playbook Guidance:\n\n"
                f"{playbook_context}\n\n"
                f"Evidence:\n"
                f"{evidence_json}"
            )
        )

        print("=" * 80)
        print("PROMPT")
        print(prompt)
        print("=" * 80)

        response = await self.llm.generate(
            prompt
        )

        print("=" * 80)
        print("LLM RESPONSE")
        print(response)
        print("=" * 80)

        try:

            return json.loads(
                response
            )

        except Exception:

            return {
                "root_cause":
                "Unable to parse LLM response",

                "confidence":
                0.0,

                "fix_plan": [
                    "Inspect raw response"
                ]
            }