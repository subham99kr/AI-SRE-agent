import json

from app.models.evidence import Evidence
from app.providers.provider_factory import ProviderFactory


class RootCauseAgent:

    def __init__(self):

        self.llm = (
            ProviderFactory
            .get_root_cause_provider()
        )

    async def analyze(
        self,
        evidence: Evidence,
        incident_type: str,
        playbook_text: str
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
                f"{playbook_text}\n\n"
                f"Evidence:\n"
                f"{evidence.model_dump_json(indent=2)}"
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

        return json.loads(response)