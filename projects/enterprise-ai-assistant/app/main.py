from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .evaluation import Evaluator
from .policy import AccessPolicy
from .providers import build_provider
from .retrieval import KnowledgeIndex, load_documents
from .service import AssistantService, AuditLog


ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS_PATH = ROOT / "app" / "data" / "documents.json"
WEB_PATH = ROOT / "web"

audit_log = AuditLog()
service = AssistantService(
    index=KnowledgeIndex(load_documents(DOCUMENTS_PATH)),
    policy=AccessPolicy(),
    provider=build_provider(),
    audit_log=audit_log,
)

app = FastAPI(
    title="Enterprise AI Assistant",
    description="Access-aware retrieval, grounded answers, audit events, and evaluations.",
    version="1.0.0",
)


class AskRequest(BaseModel):
    query: str = Field(min_length=3, max_length=1200)
    role: str


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "provider": service.provider.__class__.__name__}


@app.post("/api/ask")
def ask(request: AskRequest) -> dict:
    try:
        return asdict(service.answer(request.query, request.role))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/audit")
def audit() -> list[dict]:
    return [asdict(event) for event in audit_log.list()]


@app.post("/api/evaluations/run")
def run_evaluations() -> dict:
    return Evaluator(service).run()


app.mount("/", StaticFiles(directory=WEB_PATH, html=True), name="web")
