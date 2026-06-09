import json

from fastapi import APIRouter

from app.api.schemas import (
    IncidentRequest,
    IncidentResponse,
)

from app.providers.provider_factory import ProviderFactory


router = APIRouter()


@router.post(
    "/investigate",
    response_model=IncidentResponse
)
async def investigate_incident(
    request: IncidentRequest
):

    llm = ProviderFactory.get_root_cause_provider()

    with open(
        "app/prompts/root_cause.txt",
        "r",
        encoding="utf-8"
    ) as file:

        template = file.read()

        prompt = template.format(
            incident=request.description
        )

        analysis = await llm.generate(prompt)

        try:

            result = json.loads(analysis)

            return IncidentResponse(**result)

        except Exception:

            return IncidentResponse(
                root_cause="Unable to parse LLM response",
                confidence=0.0,
                fix_plan=[
                    "Inspect raw response in logs"
                ]
            )