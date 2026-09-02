from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class BadgeOwnersResult:
    """The badge owner count."""

    owner_count: int
    name: str
    description: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BadgeOwnersResult":
        return cls(
            owner_count=data["ownerCount"],
            name=data["name"],
            description=data["description"],
        )
