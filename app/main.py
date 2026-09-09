from fastapi import FastAPI

from app.api.claims import router as claims_router
from app.api.documents import router as documents_router
from app.api.chat import router as chat_router

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI(
    title="AI Claims Support Assistant",
    description="GenAI-powered insurance claims support solution",
    version="1.0.0"
)


app.include_router(claims_router)
app.include_router(documents_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": "AI Claims Support Assistant is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

FRONTEND_DIR = Path(__file__).resolve().parents[1] / "frontend"

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)


@app.get("/app")
def frontend():
    return FileResponse(FRONTEND_DIR / "index.html")