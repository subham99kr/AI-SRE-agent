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


# from app.services.evidence_builder import (
#     EvidenceBuilder
# )

# from app.services.incident_classifier import (
#     IncidentClassifier
# )

# from app.playbooks.playbook_factory import (
#     PlaybookFactory
# )


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
        fix_plan=result.get(
            "fix_plan",
            [
                "No remediation plan generated"
            ]
        )
    )

# @router.post(
#     "/investigate-cluster",
#     response_model=IncidentResponse
# )
# async def investigate_cluster(
#     request: ClusterIncidentRequest
# ):

#     builder = EvidenceBuilder()

#     evidence = builder.build_incident_context(
#         namespace=request.namespace,
#         deployment=request.deployment
#     )

#     incident_type = (
#         IncidentClassifier.classify(
#             evidence
#         )
#     )

#     playbook = (
#         PlaybookFactory.get_playbook(
#             incident_type
#         )
#     )

#     playbook_context = ""

#     if playbook:

#         playbook_context = (
#             playbook.get_context()
#         )

#     print("=" * 80)
#     print("INCIDENT TYPE")
#     print(incident_type)
#     print("=" * 80)

#     print("=" * 80)
#     print("EVIDENCE")
#     print(evidence.model_dump_json(indent=2))
#     print("=" * 80)

#     llm = ProviderFactory.get_root_cause_provider()

#     with open(
#         "app/prompts/root_cause.txt",
#         "r",
#         encoding="utf-8"
#     ) as file:

#         template = file.read()

#     incident_payload = f"""
# Detected Incident Type:
# {incident_type}

# Playbook Guidance:
# {playbook_context}

# Incident Evidence:
# {evidence.model_dump_json(indent=2)}
# """

#     prompt = template.replace(
#         "<<INCIDENT>>",
#         incident_payload
#     )

#     print("=" * 80)
#     print("PROMPT")
#     print(prompt)
#     print("=" * 80)

#     analysis = await llm.generate(prompt)

#     print("=" * 80)
#     print("LLM RESPONSE")
#     print(analysis)
#     print("=" * 80)

#     try:

#         result = json.loads(
#             analysis
#         )

#         return IncidentResponse(
#             **result
#         )

#     except Exception:

#         return IncidentResponse(
#             root_cause="Unable to parse LLM response",
#             confidence=0.0,
#             fix_plan=[
#                 "Inspect raw response in logs"
#             ]
#         )