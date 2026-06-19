import json
import asyncio

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from app.workflows.graph_state import (
    InvestigationState
)

from app.agents.execution_agent import (
    ExecutionAgent
)


from app.models.evidence import (
    Evidence
)

from app.services.evidence_builder import (
    EvidenceBuilder
)

from app.services.incident_classifier import (
    IncidentClassifier
)

from app.playbooks.playbook_factory import (
    PlaybookFactory
)

from app.agents.root_cause_agent import (
    RootCauseAgent
)

from app.agents.remediation_agent import (
    RemediationAgent
)

from app.agents.verification_agent import (
    VerificationAgent
)

from app.agents.summarizer_agent import (
    SummarizerAgent,
)

from app.services.persistence_service import (
    PersistenceService,
)
from app.services.retry_memory_service import (
    RetryMemoryService
)



class InvestigationGraph:

    def build(self):

        graph = StateGraph(
            InvestigationState
        )

        graph.add_node(
            "collect_evidence",
            self.collect_evidence
        )

        graph.add_node(
            "classify_incident",
            self.classify_incident
        )

        graph.add_node(
            "analyze_root_cause",
            self.analyze_root_cause
        )

        graph.add_node(
            "plan_remediation",
            self.plan_remediation
        )

        graph.add_node(
            "approval",
            self.approval_node
        )

        # graph.add_node(
        #     "execute_remediation",
        #     self.execute_remediation
        # )
        # graph.add_node(
        #     "verify_remediation",
        #     self.verify_remediation
        # )
        # graph.add_node(
        #     "generate_summary",
        #     self.generate_summary
        # )
        graph.add_node(
            "persist",
            self.persist_node
        )
        graph.add_node(
            "load_previous_attempt",
            self.load_previous_attempt
        )


        graph.add_edge(
            START,
            "load_previous_attempt"
        )

        graph.add_edge(
            "load_previous_attempt",
            "collect_evidence"
        )

        graph.add_edge(
            "collect_evidence",
            "classify_incident"
        )

        graph.add_edge(
            "classify_incident",
            "analyze_root_cause"
        )

        graph.add_edge(
            "analyze_root_cause",
            "plan_remediation"
        )

        graph.add_edge(
            "plan_remediation",
            "approval"
        )

        graph.add_edge(
            "approval",
            "persist"
        )

        # graph.add_edge(
        #     "execute_remediation",
        #     "verify_remediation"
        # )

        # graph.add_edge(
        #     "verify_remediation",
        #     "generate_summary"
        # )

        # graph.add_edge(
        #     "generate_summary",
        #     "persist"
        # )
        graph.add_edge(
            "persist",
            END
        )

        return graph.compile()

    async def collect_evidence(
        self,
        state: InvestigationState
    ):

        print("=" * 80)
        print("COLLECT_EVIDENCE NODE")
        print("=" * 80)

        builder = EvidenceBuilder()

        evidence = (
            builder.build_incident_context(
                namespace=state["namespace"],
                deployment=state["deployment"]
            )
        )

        return {
            "evidence":
            evidence.model_dump()
        }

    async def classify_incident(
        self,
        state: InvestigationState
    ):

        print("=" * 80)
        print("CLASSIFY_INCIDENT NODE")
        print("=" * 80)

        evidence = Evidence(
            **state["evidence"]
        )

        incident_type = (
            IncidentClassifier.classify(
                evidence
            )
        )

        print(
            f"INCIDENT TYPE: {incident_type}"
        )

        return {
            "incident_type":
            incident_type
        }

    async def analyze_root_cause(
        self,
        state: InvestigationState
    ):

        print("=" * 80)
        print("ROOT_CAUSE NODE")
        print("=" * 80)

        evidence = Evidence(
            **state["evidence"]
        )

        playbook = (
            PlaybookFactory
            .get_playbook(
                state["incident_type"]
            )
        )

        playbook_context = ""

        if playbook:

            playbook_context = (
                playbook.get_context()
            )

        agent = RootCauseAgent()

        result = await agent.run(

            evidence_json=json.dumps(
                state["evidence"],
                indent=2
            ),

            incident_type=state[
                "incident_type"
            ],

            playbook_context=playbook_context,

            previous_attempt_summary=
            state.get(
                "previous_attempt_summary",
                ""
            )

        )

        return {
            "root_cause":
            result["root_cause"],

            # "fix_plan":
            # result["fix_plan"],

            "confidence":
            result["confidence"]
        }



    async def plan_remediation(
        self,
        state: InvestigationState
    ):

        print("=" * 80)
        print("REMEDIATION NODE")
        print("=" * 80)

        agent = RemediationAgent()

        result = await agent.run(

            root_cause=
            state["root_cause"],

            incident_type=
            state["incident_type"],

            evidence_json=json.dumps(
                state["evidence"],
                indent=2
            ),

            previous_attempt_summary=
            state.get(
                "previous_attempt_summary",
                ""
            )

        )

        return {
            "risk":
            result["risk"],

            "requires_approval":
            result["requires_approval"],

            "approval_reason":
            result["approval_reason"],

            "rollback_available":
            result["rollback_available"],

            "remediation_reasoning":
            result.get(
                "reasoning",
                ""
            ),

            "remediation_steps":
            result["steps"]

        }
    

    async def execute_remediation(
        self,
        state: InvestigationState
    ):

        print("=" * 80)
        print("EXECUTION NODE")
        print("=" * 80)

        agent = ExecutionAgent()

        execution_results = await agent.run(
            remediation_steps = state["remediation_steps"],
            approved =  state["requires_approval"]
        )

        return {
            "execution_results": execution_results
        }
            
    async def verify_remediation(
        self,
        state: InvestigationState
    ):

        print("=" * 80)
        print("VERIFICATION NODE")
        print("=" * 80)

        agent = VerificationAgent()

        last_result = None

        MAX_RETRIES = 3

        WAIT_SECONDS = 5

        for attempt in range(
            MAX_RETRIES
        ):

            print(
                f"Verification Attempt "
                f"{attempt + 1}/"
                f"{MAX_RETRIES}"
            )

            last_result = await agent.run(

                namespace=state["namespace"],

                deployment=state["deployment"]

            )

            if last_result.success:

                print(
                    "Deployment verified successfully."
                )

                break

            print(

                f"Verification failed. "

                f"Retrying in "

                f"{WAIT_SECONDS} seconds..."

            )

            await asyncio.sleep(
                WAIT_SECONDS
            )

        return {

            "verification_success":
            last_result.success,

            "verification_message":
            last_result.message,

            "verification_checks":
            last_result.checks

        }
    

    async def generate_summary(
        self,
        state: InvestigationState
    ):

        print("=" * 80)
        print("SUMMARY NODE")
        print("=" * 80)

        agent = SummarizerAgent()

        report = await agent.run(

            namespace=state["namespace"],

            deployment=state["deployment"],

            incident_type=state["incident_type"],

            root_cause=state["root_cause"],

            confidence=state["confidence"],

            risk=state["risk"],

            requires_approval=state["requires_approval"],

            rollback_available=state["rollback_available"],

            remediation_steps=state["remediation_steps"],

            execution_results=state["execution_results"],

            verification_success=state["verification_success"],

            verification_message=state["verification_message"]

        )

        return {

            "incident_report": report

        }
    

    async def persist_node(
        self,
        state: InvestigationState
    ):

        incident_id = (
            PersistenceService()
            .save(state)
        )

        state["incident_id"] = incident_id

        return state
    

    async def approval_node(
        self,
        state: InvestigationState
    ):

        print("=" * 80)
        print("APPROVAL NODE")
        print("=" * 80)

        #
        # LOW risk → execute automatically
        #

        if not state["requires_approval"]:

            print("AUTO APPROVED")

            return {

                "approval_status":
                "AUTO_APPROVED",

                "status":
                "APPROVED"

            }

        #
        # MEDIUM/HIGH/CRITICAL
        #

        print("WAITING FOR HUMAN APPROVAL")

        print(
            state["approval_reason"]
        )

        return {

            "approval_status":
            "PENDING",

            "status":
            "PENDING_APPROVAL"

        }
    
    async def route_after_approval(
        self,
        state: InvestigationState
    ):

        return "persist"
    
    async def load_previous_attempt(
        self,
        state: InvestigationState
    ):

        print("=" * 80)
        print("LOAD PREVIOUS ATTEMPT")
        print("=" * 80)

        #
        # Fresh investigation
        #

        if not state.get("retry", False):

            print("Fresh investigation.")

            return {}

        #
        # Retry
        #

        print("Retry investigation.")

        summary = RetryMemoryService().load(
            root_incident_id=state["root_incident_id"],
            limit=5
        )

        print("=" * 80)
        print("PREVIOUS ATTEMPT SUMMARY")
        print(summary)
        print("=" * 80)

        return {
            "previous_attempt_summary": summary
        }
        
    # async def route_after_approval(
    #     self,
    #     state: InvestigationState
    # ):

    #     if state["approval_status"] == "AUTO_APPROVED":

    #         state["status"] = "APPROVED"

    #         return "persist"

    #     state["status"] = "PENDING_APPROVAL"

    #     return "persist_pending"