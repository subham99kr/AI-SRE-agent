from sqlalchemy.orm import Session

from app.database.session import SessionLocal

from app.storage.incident_repository import (
    IncidentRepository
)


class IncidentService:

    def get_incidents(self):

        db: Session = SessionLocal()

        try:

            repo = IncidentRepository(db)

            return repo.list_incidents()

        finally:

            db.close()

    def get_incident(
        self,
        incident_id: str
    ):

        db: Session = SessionLocal()

        try:

            repo = IncidentRepository(db)

            return repo.get(
                incident_id
            )

        finally:

            db.close()

    def get_latest(
        self,
        limit: int = 10
    ):

        db: Session = SessionLocal()

        try:

            repo = IncidentRepository(db)

            return repo.latest(
                limit
            )

        finally:

            db.close()

    def filter_by_type(
        self,
        incident_type: str
    ):

        db: Session = SessionLocal()

        try:

            repo = IncidentRepository(db)

            return repo.filter_by_type(
                incident_type
            )

        finally:

            db.close()

    def delete_incident(
        self,
        incident_id: str
    ):

        db: Session = SessionLocal()

        try:

            repo = IncidentRepository(db)

            repo.delete(
                incident_id
            )

            db.commit()

        except:

            db.rollback()

            raise

        finally:

            db.close()

    def load_for_execution(
        self,
        incident_id: str
    ):

        db: Session = SessionLocal()

        try:

            repo = IncidentRepository(db)

            return repo.get(
                incident_id
            )

        finally:

            db.close()

    def get_incident(
        self,
        incident_id: str
    ):

        db: Session = SessionLocal()

        try:

            repo = IncidentRepository(db)

            return repo.get(
                incident_id
            )

        finally:

            db.close()

    def approve_incident(
        self,
        incident_id: str,
        approved_by: str
    ):

        db: Session = SessionLocal()

        try:

            repo = IncidentRepository(db)

            incident = repo.get(
                incident_id
            )

            if incident is None:

                return None

            incident.status = "APPROVED"

            incident.approval_status = "APPROVED"

            incident.approved_by = approved_by

            repo.update(
                incident
            )

            db.commit()

            return incident

        except Exception:

            db.rollback()

            raise

        finally:

            db.close()

    def reject_incident(
        self,
        incident_id: str,
        approved_by: str
    ):

        db: Session = SessionLocal()

        try:

            repo = IncidentRepository(db)

            incident = repo.get(
                incident_id
            )

            if incident is None:

                return None

            incident.status = "REJECTED"

            incident.approval_status = "REJECTED"

            incident.approved_by = approved_by

            repo.update(
                incident
            )

            db.commit()

            return incident

        except Exception:

            db.rollback()

            raise

        finally:

            db.close()