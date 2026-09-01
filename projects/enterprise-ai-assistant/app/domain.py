from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Sequence


@dataclass(frozen=True)
class Document:
    id: str
    title: str
    department: str
    allowed_roles: frozenset[str]
    content: str


@dataclass(frozen=True)
class SearchHit:
    document: Document
    score: float


@dataclass(frozen=True)
class ProviderOutput:
    text: str
    provider: str
    model: str
    input_tokens: int | None = None
    output_tokens: int | None = None


@dataclass(frozen=True)
class Citation:
    document_id: str
    title: str
    department: str
    excerpt: str


@dataclass(frozen=True)
class AssistantResult:
    answer: str
    citations: Sequence[Citation]
    provider: str
    model: str
    latency_ms: int
    input_tokens: int | None
    output_tokens: int | None
    access_decision: str
    denied_candidate_count: int


@dataclass(frozen=True)
class AuditEvent:
    request_id: str
    timestamp: str
    role: str
    query: str
    access_decision: str
    citation_count: int
    denied_candidate_count: int
    provider: str
    latency_ms: int

    @classmethod
    def now(cls, **kwargs) -> "AuditEvent":
        return cls(timestamp=datetime.now(timezone.utc).isoformat(), **kwargs)


@dataclass(frozen=True)
class EvaluationCase:
    name: str
    role: str
    query: str
    expected_document_ids: frozenset[str] = field(default_factory=frozenset)
    forbidden_document_ids: frozenset[str] = field(default_factory=frozenset)
    required_terms: frozenset[str] = field(default_factory=frozenset)
