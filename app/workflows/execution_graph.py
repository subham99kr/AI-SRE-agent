from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from app.agents.execution_agent import (
    ExecutionAgent
)

import asyncio

from app.agents.verification_agent import (
    VerificationAgent
)

from app.workflows.execution_state import (
    ExecutionState,
)

from app.services.execution_context_service import (
    ExecutionContextService
)
from app.agents.summarizer_agent import (
    SummarizerAgent
)

from app.services.execution_persistence_service import (
    ExecutionPersistenceService
)

class ExecutionGraph:

    def build(self):

        graph = StateGraph(
            ExecutionState
        )

        graph.add_node(
            "execute_remediation",
            self.execute_remediation
        )
        graph.add_node(
            "load_incident",
            self.load_incident
        )
        graph.add_node(
            "verify_remediation",
            self.verify_remediation
        )
        graph.add_node(
            "generate_summary",
            self.generate_summary
        )

        graph.add_node(
            "persist",
            self.persist
        )

        graph.add_edge(
            START,
            "load_incident"
        )

        graph.add_edge(
            "load_incident",
            "execute_remediation"
        )

        graph.add_edge(
            "execute_remediation",
            "verify_remediation"
        )

        graph.add_edge(
            "verify_remediation",
            "generate_summary"
        )

        graph.add_edge(
            "generate_summary",
            "persist"
        )

        graph.add_edge(
            "persist",
            END
        )

        return graph.compile()

    async def load_incident(
        self,
        state: ExecutionState
    ):

        print("=" * 80)
        print("LOAD INCIDENT NODE")
        print("=" * 80)

        context = (
            ExecutionContextService()
            .load(
                state["incident_id"]
            )
        )

        if context is None:

            raise ValueError(
                "Incident not found."
            )

        print(context["incident"].id)
        print(context["incident"].status)
        print(context["incident"].root_cause)

        print(context["remediation"].risk)
        print(len(context["remediation"].steps))

        return {

            "incident_id":
            context["incident"].id,

            "incident":
            context["incident"],

            "evidence":
            context["evidence"],

            "remediation":
            context["remediation"]

        }
        
    async def execute_remediation(
        self,
        state: ExecutionState
    ):

        print("=" * 80)
        print("EXECUTION NODE")
        print("=" * 80)

        agent = ExecutionAgent()

        execution_results = await agent.run(

            remediation_steps=
            state["remediation"].steps,

            approved=True

        )

        print("=" * 80)
        print("EXECUTION RESULTS")
        print("=" * 80)

        for result in execution_results:

            print(result)

        return {

            "execution_results":
            execution_results

        }
        
    async def verify_remediation(
        self,
        state: ExecutionState
    ):

        print("=" * 80)
        print("VERIFICATION NODE")
        print("=" * 80)

        agent = VerificationAgent()

        last_result = None

        MAX_RETRIES = 6

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

                namespace=
                state["incident"].namespace,

                deployment=
                state["incident"].deployment

            )
            print(last_result.message)

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
        state: ExecutionState
    ):

        print("=" * 80)
        print("SUMMARY NODE")
        print("=" * 80)

        agent = SummarizerAgent()

        report = await agent.run(

            namespace=state["incident"].namespace,

            deployment=state["incident"].deployment,

            incident_type=state["incident"].incident_type,

            root_cause=state["incident"].root_cause,

            confidence=state["incident"].confidence,

            risk=state["incident"].risk,

            requires_approval=state["incident"].requires_approval,

            rollback_available=state["incident"].rollback_available,

            remediation_steps=state["remediation"].steps,

            execution_results=state["execution_results"],

            verification_success=state["verification_success"],

            verification_message=state["verification_message"]

        )

        print("=" * 80)
        print("SUMMARY GENERATED")
        print("=" * 80)

        return {

            "incident_report": report

        }
    
    async def persist(
        self,
        state: ExecutionState
    ):

        ExecutionPersistenceService().save(
            state
        )

        print("=" * 80)
        print("EXECUTION RESULTS SAVED")
        print("=" * 80)

        return state