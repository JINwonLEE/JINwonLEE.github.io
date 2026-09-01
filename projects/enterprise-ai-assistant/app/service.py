from __future__ import annotations

import time
import uuid
from collections import deque
from threading import Lock

from .domain import AssistantResult, AuditEvent, Citation
from .policy import AccessPolicy
from .providers import AnswerProvider
from .retrieval import KnowledgeIndex


class AuditLog:
    def __init__(self, max_events: int = 200):
        self._events: deque[AuditEvent] = deque(maxlen=max_events)
        self._lock = Lock()

    def append(self, event: AuditEvent) -> None:
        with self._lock:
            self._events.appendleft(event)

    def list(self) -> list[AuditEvent]:
        with self._lock:
            return list(self._events)


class AssistantService:
    def __init__(
        self,
        index: KnowledgeIndex,
        policy: AccessPolicy,
        provider: AnswerProvider,
        audit_log: AuditLog | None = None,
    ):
        self.index = index
        self.policy = policy
        self.provider = provider
        self.audit_log = audit_log or AuditLog()

    def answer(self, query: str, role: str) -> AssistantResult:
        request_id = str(uuid.uuid4())
        normalized_role = self.policy.normalize_role(role)
        started = time.perf_counter()

        candidates = self.index.search(query)
        authorized = [
            hit.document for hit in candidates if self.policy.can_read(normalized_role, hit.document)
        ][:4]
        denied_count = sum(
            not self.policy.can_read(normalized_role, hit.document) for hit in candidates
        )
        provider_output = self.provider.generate(query, authorized)
        latency_ms = max(1, round((time.perf_counter() - started) * 1000))
        decision = "allowed" if authorized else "no-authorized-context"

        citations = [
            Citation(
                document_id=document.id,
                title=document.title,
                department=document.department,
                excerpt=document.content[:180].rstrip() + ("..." if len(document.content) > 180 else ""),
            )
            for document in authorized
        ]
        result = AssistantResult(
            answer=provider_output.text,
            citations=citations,
            provider=provider_output.provider,
            model=provider_output.model,
            latency_ms=latency_ms,
            input_tokens=provider_output.input_tokens,
            output_tokens=provider_output.output_tokens,
            access_decision=decision,
            denied_candidate_count=denied_count,
        )
        self.audit_log.append(
            AuditEvent.now(
                request_id=request_id,
                role=normalized_role,
                query=query[:180],
                access_decision=decision,
                citation_count=len(citations),
                denied_candidate_count=denied_count,
                provider=provider_output.provider,
                latency_ms=latency_ms,
            )
        )
        return result
