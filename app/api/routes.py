import json

from fastapi import APIRouter
from fastapi import HTTPException

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

from app.services.report_service import (
    ReportService
)

from app.services.incident_service import (
    IncidentService
)
from app.workflows.execution_graph import (
    ExecutionGraph
)

from app.api.schemas import (
    IncidentListItem,
    IncidentDetailsResponse,
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

    print("APPROVAL STATUS")
    print(graph_result["approval_status"])
    print("=" * 80)

    print("WORKFLOW STATUS")
    print(graph_result["status"])
    print("=" * 80)

    print("APPROVAL REASON")
    print(graph_result["approval_reason"])
    print("=" * 80)

    print("REMEDIATION STEPS")

    for i, step in enumerate(
        graph_result["remediation_steps"],
        start=1
    ):

        print(f"{i}. {step['description']}")

        if step.get("kubectl_command"):

            print(
                f"   $ {step['kubectl_command']}"
            )

    print("=" * 80)

    print(
        f"INCIDENT SAVED : "
        f"{graph_result['incident_id']}"
    )

    print("=" * 80)

    return IncidentResponse(

        root_cause=graph_result["root_cause"],

        confidence=graph_result["confidence"],

        risk=graph_result["risk"],

        status=graph_result["status"],

        approval_status=graph_result["approval_status"],

        approval_reason=graph_result["approval_reason"],

        requires_approval=graph_result[
            "requires_approval"
        ],

        rollback_available=graph_result[
            "rollback_available"
        ],

        remediation_steps=graph_result[
            "remediation_steps"
        ],

        verification_success=False,

        verification_message="Pending approval.",

        verification_checks=[],

        incident_report=None,

        incident_id=graph_result[
            "incident_id"
        ]

    )


@router.get(
    "/incidents",
    response_model=list[IncidentListItem]
)
async def get_incidents():

    incidents = (
        IncidentService()
        .get_incidents()
    )

    return incidents


@router.get(
    "/incidents/latest",
    response_model=list[IncidentListItem]
)
async def get_latest_incidents():

    incidents = (
        IncidentService()
        .get_latest()
    )

    return incidents

@router.get(
    "/incidents/latest",
    response_model=list[IncidentListItem]
)
async def get_latest_incidents():

    incidents = (
        IncidentService()
        .get_latest()
    )

    return incidents


@router.delete(
    "/incidents/{incident_id}"
)
async def delete_incident(
    incident_id: str
):

    IncidentService().delete_incident(
        incident_id
    )

    return {
        "message": "Incident deleted successfully."
    }
@router.post(
    "/incidents/{incident_id}/approve"
)
async def approve_incident(
    incident_id: str
):

    #
    # Approve Incident
    #

    incident = (
        IncidentService()
        .approve_incident(
            incident_id,
            "admin"
        )
    )

    if incident is None:

        raise HTTPException(
            status_code=404,
            detail="Incident not found."
        )

    #
    # Execute Approved Incident
    #

    graph = (
        ExecutionGraph()
        .build()
    )

    result = await graph.ainvoke(
        {
            "incident_id": incident_id
        }
    )

    #
    # Return Final Result
    #

    return {

        "message":
        "Incident executed successfully.",

        "incident_id":
        incident.id,

        "status":
        result["incident"].status,

        "approval_status":
        result["incident"].approval_status,

        "approved_by":
        result["incident"].approved_by,

        "verification_success":
        result["verification_success"],

        "verification_message":
        result["verification_message"],

        "report":
        result["incident_report"]

    }