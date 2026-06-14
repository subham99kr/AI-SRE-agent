from app.database.base import Base
from app.database.session import engine

# Import every ORM model so SQLAlchemy registers them

import app.database.incident
import app.database.evidence
import app.database.execution
import app.database.remediation
import app.database.verification
import app.database.report


def create_tables():

    Base.metadata.create_all(bind=engine)

    print()

    print("=" * 80)
    print("DATABASE TABLES CREATED")
    print("=" * 80)


if __name__ == "__main__":

    create_tables()