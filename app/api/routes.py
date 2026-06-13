import json

from fastapi import APIRouter

from app.api.schemas import (
    IncidentRequest,
    IncidentResponse,
    ClusterIncidentRequest,
)
from app.workflows.investigation_graph import (
    InvestigationGraph
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

    prompt = template.replace(
        "<<INCIDENT>>",
        request.description
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


@router.post(
    "/investigate-cluster",
    response_model=IncidentResponse
)
async def investigate_cluster(
    request: ClusterIncidentRequest
):

    graph = (
        InvestigationGraph()
        .build()
    )

    result = await graph.ainvoke(
        {
            "namespace": request.namespace,
            "deployment": request.deployment
        }
    )

    print("=" * 80)
    print("GRAPH RESULT")
    print(result)
    print("=" * 80)

    print("=" * 80)
    print("RISK")
    print(result["risk"])
    print("=" * 80)

    print("REQUIRES APPROVAL")
    print(result["requires_approval"])
    print("=" * 80)

    print("ROLLBACK AVAILABLE")
    print(result["rollback_available"])
    print("=" * 80)

    print("REMEDIATION STEPS")
    for i, step in enumerate(result["remediation_steps"], start=1):

        print(f"{i}. {step['description']}")

        if step.get("kubectl_command"):

            print(f"   $ {step['kubectl_command']}")

    print("=" * 80)

    return IncidentResponse(
        root_cause=result.get(
            "root_cause",
            "Unknown"
        ),
        confidence=float(
            result.get(
                "confidence",
                0.0
            )
        ),
        risk=result.get(
            "risk",
            "UNKNOWN"
        ),
        requires_approval=True,
        rollback_available=result.get(
            "rollback_available",
            False
        ),
        remediation_steps=result.get(
            "remediation_steps",
            []
        )
    )