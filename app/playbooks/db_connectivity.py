from app.models.evidence_types import (
    EvidenceType
)


class DBConnectivityPlaybook:

    @staticmethod
    def get_context() -> str:

        return """
You are handling a Database Connectivity incident.

Focus on:

1. Database connection failures
2. Connection timeouts
3. Authentication failures
4. DNS resolution failures
5. Service discovery issues
6. Network connectivity between the application and the database
7. Database availability
8. Missing or incorrect environment variables
9. Incorrect Secrets or ConfigMaps
10. Recent configuration changes

Prioritize application logs and Kubernetes events before assuming the database itself is unavailable.

Suggest Kubernetes-native remediation whenever possible.

Avoid recommending database restarts unless the evidence clearly indicates a database-side failure.

Verify that the application successfully reconnects to the database after remediation.
"""

    @staticmethod
    def required_evidence():

        return [

            EvidenceType.PODS,

            EvidenceType.LOGS,

            EvidenceType.EVENTS,

            EvidenceType.SERVICE_REPORT,

            EvidenceType.ENDPOINT_REPORT,

            EvidenceType.CONFIGMAP_REPORT,

            EvidenceType.SECRET_REPORT

        ]