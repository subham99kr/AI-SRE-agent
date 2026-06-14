from app.services.persistence_service import (
    PersistenceService
)

state = {

    "namespace": "default",

    "deployment": "broken-app",

    "incident_type": "CrashLoopBackOff",

    "root_cause": "Container exits immediately due to invalid startup command.",

    "confidence": 0.99,

    "risk": "HIGH",

    "requires_approval": True,

    "rollback_available": True,

    "verification_success": True,

    "verification_message": "Deployment successfully recovered.",

    "verification_checks": [
        "Deployment exists.",
        "Pods are Ready."
    ],

    "evidence": {

        "deployment": {
            "replicas": 1
        },

        "pods": [
            {
                "name": "broken-app"
            }
        ],

        "events": [],

        "logs": [
            "CrashLoopBackOff"
        ]
    },

    "remediation_steps": [

        {
            "description": "Patch deployment",
            "kubectl_command": "kubectl patch ..."
        }

    ],

    "execution_results": [

        {
            "step": "Patch deployment",

            "command": "kubectl patch ...",

            "success": True,

            "stdout": "patched",

            "stderr": ""
        }

    ],

    "incident_report": {

        "title": "CrashLoopBackOff Incident",

        "executive_summary": "Recovered successfully.",

        "technical_summary": "Container command updated.",

        "overall_status": "Resolved",

        "recommendations": [

            "Validate startup commands"

        ]

    }

}
service = PersistenceService()

incident_id = service.save(state)

print()

print("=" * 80)

print("INCIDENT SAVED")

print("=" * 80)

print(incident_id)

