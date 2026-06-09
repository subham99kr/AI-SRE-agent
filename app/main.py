from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="AI SRE Agent",
    description="AI-powered SRE Copilot with Human-in-the-Loop approvals",
    version="1.0.0",
)

app.include_router(router)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "ai-sre-agent"
    }