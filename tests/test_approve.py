from app.services.incident_service import IncidentService

service = IncidentService()

incident = service.approve_incident(
    "3a8aa87a-856d-4ceb-865c-e6b29d827cc8",
    "admin"
)

if incident is None:
    print("Incident not found")
else:
    print("Status:", incident.status)
    print("Approval Status:", incident.approval_status)
    print("Approved By:", incident.approved_by)