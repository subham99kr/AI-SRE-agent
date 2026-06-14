from sqlalchemy import select

from app.database.report import Report

from app.storage.base_repository import (
    BaseRepository
)


class ReportRepository(BaseRepository):

    def create(
        self,
        report: Report
    ) -> Report:

        self.add(
            report
        )

        return report

    def get(
        self,
        incident_id: str
    ) -> Report | None:

        statement = select(
            Report
        ).where(
            Report.incident_id == incident_id
        )

        return self.db.scalar(
            statement
        )