from __future__ import annotations

from .domain import Document


SUPPORTED_ROLES = frozenset({"engineer", "manager", "contractor"})


class AccessPolicy:
    def normalize_role(self, role: str) -> str:
        normalized = role.strip().lower()
        if normalized not in SUPPORTED_ROLES:
            raise ValueError(f"Unsupported role: {role}")
        return normalized

    def can_read(self, role: str, document: Document) -> bool:
        return self.normalize_role(role) in document.allowed_roles
