from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class Friend:
    """A Habbo friend."""

    unique_id: str
    name: str
    motto: str
    online: bool
    figure_string: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Friend":
        return cls(
            unique_id=data["uniqueId"],
            name=data["name"],
            motto=data["motto"],
            online=data["online"],
            figure_string=data["figureString"],
        )


@dataclass
class UserFriendsResult:
    """A list of friends of a user."""

    friends: List[Friend]

    @classmethod
    def from_dict(cls, data: List[Dict[str, Any]]) -> "UserFriendsResult":
        return cls(friends=[Friend.from_dict(item) for item in data])
