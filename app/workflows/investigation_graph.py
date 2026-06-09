from langgraph.graph import (
    StateGraph,
    END
)

from app.workflows.graph_state import (
    InvestigationState
)

from app.services.evidence_builder import (
    EvidenceBuilder
)

from app.services.incident_classifier import (
    IncidentClassifier
)

from app.playbooks.crashloop import (
    CrashLoopPlaybook
)

from app.playbooks.image_pull import (
    ImagePullPlaybook
)

from app.agents.root_cause_agent import (
    RootCauseAgent
)


class InvestigationGraph:

    def __init__(self):

        self.builder = EvidenceBuilder()

        self.rca_agent = RootCauseAgent()

    async def collect_evidence(
        self,
        state: InvestigationState
    ):

        evidence = (
            self.builder
            .build_incident_context(
                namespace=state["namespace"],
                deployment=state["deployment"]
            )
        )

        return {
            "evidence": evidence
        }

    async def classify_incident(
        self,
        state: InvestigationState
    ):

        incident_type = (
            IncidentClassifier.classify(
                state["evidence"]
            )
        )

        print("=" * 80)
        print("INCIDENT TYPE")
        print(incident_type)
        print("=" * 80)

        return {
            "incident_type": incident_type
        }

    async def analyze_root_cause(
        self,
        state: InvestigationState
    ):

        playbook_text = ""

        if (
            state["incident_type"]
            == "CRASH_LOOP"
        ):

            playbook_text = (
                CrashLoopPlaybook.get_prompt()
            )

        elif (
            state["incident_type"]
            == "IMAGE_PULL"
        ):

            playbook_text = (
                ImagePullPlaybook.get_prompt()
            )

        result = (
            await self.rca_agent.analyze(
                evidence=state["evidence"],
                incident_type=(
                    state["incident_type"]
                ),
                playbook_text=playbook_text
            )
        )

        return {
            "root_cause": result.get(
                "root_cause"
            ),
            "confidence": result.get(
                "confidence",
                0.0
            ),
            "fix_plan": result.get(
                "fix_plan",
                []
            )
        }

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

        graph.set_entry_point(
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
            END
        )

        return graph.compile()