import json

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from app.workflows.graph_state import (
    InvestigationState
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


        graph.add_edge(
            START,
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
            playbook_context=playbook_context
        )

        return {
            "root_cause":
            result["root_cause"],

            "fix_plan":
            result["fix_plan"],

            "confidence":
            result["confidence"]
        }
