from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import time

app = FastAPI()

Instrumentator().instrument(app).expose(app)


@app.get("/")
def home():

    return {
        "status": "running"
    }


@app.get("/health")
def health():

    return {
        "healthy": True
    }


@app.get("/slow")
def slow():

    time.sleep(2)

    return {
        "message": "slow endpoint"
    }


@app.get("/error")
def error():

    raise RuntimeError("Intentional failure")