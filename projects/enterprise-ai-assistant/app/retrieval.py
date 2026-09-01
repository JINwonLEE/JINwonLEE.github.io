from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path
from typing import Iterable

from .domain import Document, SearchHit


TOKEN_PATTERN = re.compile(r"[\w-]{2,}", re.UNICODE)
STOP_WORDS = frozenset(
    {
        "and",
        "are",
        "before",
        "can",
        "could",
        "for",
        "from",
        "how",
        "into",
        "show",
        "that",
        "the",
        "this",
        "what",
        "when",
        "where",
        "which",
        "with",
        "would",
    }
)


def load_documents(path: Path) -> list[Document]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [
        Document(
            id=item["id"],
            title=item["title"],
            department=item["department"],
            allowed_roles=frozenset(item["allowed_roles"]),
            content=item["content"],
        )
        for item in data
    ]


class KnowledgeIndex:
    """Small, inspectable retrieval layer backed by SQLite FTS5/BM25."""

    def __init__(self, documents: Iterable[Document]):
        self._documents = {document.id: document for document in documents}
        self._db = sqlite3.connect(":memory:", check_same_thread=False)
        self._db.execute(
            "CREATE VIRTUAL TABLE knowledge USING fts5(doc_id UNINDEXED, title, content)"
        )
        self._db.executemany(
            "INSERT INTO knowledge(doc_id, title, content) VALUES (?, ?, ?)",
            [
                (document.id, document.title, document.content)
                for document in self._documents.values()
            ],
        )

    @staticmethod
    def _match_expression(query: str) -> str:
        tokens = [
            token
            for token in TOKEN_PATTERN.findall(query.lower())
            if token not in STOP_WORDS
        ]
        unique_tokens = list(dict.fromkeys(tokens))[:12]
        return " OR ".join(f'"{token.replace(chr(34), chr(34) * 2)}"' for token in unique_tokens)

    def search(self, query: str, limit: int = 12) -> list[SearchHit]:
        expression = self._match_expression(query)
        if not expression:
            return []
        rows = self._db.execute(
            """
            SELECT doc_id, bm25(knowledge) AS rank
            FROM knowledge
            WHERE knowledge MATCH ?
            ORDER BY rank
            LIMIT ?
            """,
            (expression, limit),
        ).fetchall()
        if rows:
            best_rank = float(rows[0][1])
            rows = [row for row in rows if float(row[1]) <= best_rank * 0.5]
        return [
            SearchHit(document=self._documents[doc_id], score=float(rank))
            for doc_id, rank in rows
        ]
