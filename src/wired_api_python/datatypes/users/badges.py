from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class Badge:
    """A Habbo badge."""

    code: str
    name: str
    description: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Badge":
        return cls(code=data["code"], name=data["name"], description=data["description"])


@dataclass
class UserBadgesResult:
    """The list of badges obtained by a user."""

    badges: List[Badge]

    @classmethod
    def from_dict(cls, data: List[Dict[str, Any]]) -> "UserBadgesResult":
        return cls(badges=[Badge.from_dict(item) for item in data])
