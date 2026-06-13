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

from app.providers.provider_factory import (
    ProviderFactory
)


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

            risk="UNKNOWN",

            requires_approval=True,

            rollback_available=False,

            remediation_steps=[],

            verification_success=False,

            verification_message="Verification not executed.",

            verification_checks=[]

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

    graph_result = await graph.ainvoke(
        {
            "namespace": request.namespace,
            "deployment": request.deployment
        }
    )

    print("=" * 80)
    print("GRAPH RESULT")
    print(graph_result)
    print("=" * 80)

    print("=" * 80)
    print("RISK")
    print(graph_result["risk"])
    print("=" * 80)

    print("REQUIRES APPROVAL")
    print(graph_result["requires_approval"])
    print("=" * 80)

    print("ROLLBACK AVAILABLE")
    print(graph_result["rollback_available"])
    print("=" * 80)

    print("REMEDIATION STEPS")

    for i, step in enumerate(
        graph_result["remediation_steps"],
        start=1
    ):

        print(f"{i}. {step['description']}")

        if step.get("kubectl_command"):

            print(f"   $ {step['kubectl_command']}")

    print("=" * 80)

    print("EXECUTION RESULTS")

    for execution in graph_result.get(
        "execution_results",
        []
    ):

        print(execution)

    print("=" * 80)

    print("VERIFICATION")
    print("=" * 80)

    print(
        f"SUCCESS: {graph_result['verification_success']}"
    )

    print(
        f"MESSAGE: {graph_result['verification_message']}"
    )

    print()

    print("CHECKS")

    for check in graph_result[
        "verification_checks"
    ]:

        print(f"- {check}")

    print("=" * 80)

    return IncidentResponse(

        root_cause=graph_result.get(
            "root_cause",
            "Unknown"
        ),

        confidence=float(
            graph_result.get(
                "confidence",
                0.0
            )
        ),

        risk=graph_result.get(
            "risk",
            "UNKNOWN"
        ),

        requires_approval=graph_result.get(
            "requires_approval",
            True
        ),

        rollback_available=graph_result.get(
            "rollback_available",
            False
        ),

        remediation_steps=graph_result.get(
            "remediation_steps",
            []
        ),

        verification_success=graph_result.get(
            "verification_success",
            False
        ),

        verification_message=graph_result.get(
            "verification_message",
            "Verification not executed."
        ),

        verification_checks=graph_result.get(
            "verification_checks",
            []
        )

    )