from sqlalchemy import text

from app.database.session import (
    engine,
    DATABASE_URL
)
from app.config.settings import settings

print(settings.POSTGRES_HOST)
print(settings.POSTGRES_PORT)
print(settings.POSTGRES_DB)
print(settings.POSTGRES_USER)
print(settings.POSTGRES_PASSWORD)

print(DATABASE_URL)

def test_connection():

    try:

        with engine.connect() as connection:

            result = connection.execute(
                text("SELECT version();")
            )

            print(result.scalar())

    except Exception as e:

        print(e)


if __name__ == "__main__":
    test_connection()