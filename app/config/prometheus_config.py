import os

PROMETHEUS_URL = os.getenv(
    "PROMETHEUS_URL",
    "http://localhost:9090"
)

PROMETHEUS_TIMEOUT = int(
    os.getenv(
        "PROMETHEUS_TIMEOUT",
        "15"
    )
)