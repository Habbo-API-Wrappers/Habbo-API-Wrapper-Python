from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from ..groups import GroupType


@dataclass
class Group:
    """A Habbo group, as requested through a user."""

    online: bool
    id: str
    name: str
    description: str
    type: GroupType
    badge_code: str
    room_id: str
    primary_colour: str
    secondary_colour: str
    is_admin: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Group":
        return cls(
            online=data["online"],
            id=data["id"],
            name=data["name"],
            description=data["description"],
            type=GroupType.from_string(data["type"]),
            badge_code=data["badgeCode"],
            room_id=data["roomId"],
            primary_colour=data["primaryColour"],
            secondary_colour=data["secondaryColour"],
            is_admin=data["isAdmin"],
        )


@dataclass
class UserGroupsResult:
    """A list of groups that a user is in."""

    groups: List[Group]

    @classmethod
    def from_dict(cls, data: List[Dict[str, Any]]) -> "UserGroupsResult":
        return cls(groups=[Group.from_dict(item) for item in data])
