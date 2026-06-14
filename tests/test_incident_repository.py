from app.database.incident import Incident

from app.storage.incident_repository import (
    IncidentRepository
)


def main():

    repo = IncidentRepository()

    incident = Incident(

        namespace="default",

        deployment="broken-app",

        incident_type="CRASH_LOOP",

        root_cause="Container exits immediately.",

        confidence=1.0,

        risk="HIGH",

        requires_approval=True,

        rollback_available=True,

        verification_success=False,

        verification_message="Not verified"

    )

    saved = repo.create(incident)

    print()

    print("=" * 80)
    print("INCIDENT CREATED")
    print("=" * 80)

    print(saved.id)

    loaded = repo.get(saved.id)

    print()

    print("=" * 80)
    print("FETCHED INCIDENT")
    print("=" * 80)

    print(loaded)

    repo.close()


if __name__ == "__main__":

    main()