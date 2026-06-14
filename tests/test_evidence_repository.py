from app.database.incident import Incident
from app.database.evidence import Evidence

from app.storage.incident_repository import IncidentRepository
from app.storage.evidence_repository import EvidenceRepository


incident_repo = IncidentRepository()

incident = Incident(

    namespace="default",

    deployment="broken-app",

    incident_type="CRASH_LOOP",

    root_cause="Test",

    confidence=1.0,

    risk="HIGH",

    requires_approval=True,

    rollback_available=True,

    verification_success=False,

    verification_message="Pending"

)

incident = incident_repo.create(incident)

repo = EvidenceRepository()

evidence = Evidence(

    incident_id=incident.id,

    deployment_spec={"replicas": 1},

    pods=[{"name": "broken-app"}],

    events=[],

    logs=["CrashLoopBackOff"]

)

saved = repo.create(evidence)

print(saved.incident_id)

loaded = repo.get(incident.id)

print(loaded.logs)

repo.close()
incident_repo.close()