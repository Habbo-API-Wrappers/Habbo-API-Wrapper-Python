from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List


class GroupType(Enum):
    """The access type of a group."""

    NORMAL = "NORMAL"
    """The group is open, anyone can join."""

    EXCLUSIVE = "EXCLUSIVE"
    """The group is locked, users can request to join, admins can accept new members."""

    CLOSED = "CLOSED"
    """The group is locked, nobody can join."""

    @classmethod
    def from_string(cls, type_: str) -> "GroupType":
        """Parse a received string into a :class:`GroupType`."""
        if type_ == "EXCLUSIVE":
            return cls.EXCLUSIVE
        if type_ == "CLOSED":
            return cls.CLOSED
        return cls.NORMAL


@dataclass
class GroupMember:
    """A member of a group."""

    online: bool
    gender: str
    motto: str
    habbo_figure: str
    member_since: str
    unique_id: str
    name: str
    is_admin: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupMember":
        return cls(
            online=data["online"],
            gender=data["gender"],
            motto=data["motto"],
            habbo_figure=data["habboFigure"],
            member_since=data["memberSince"],
            unique_id=data["uniqueId"],
            name=data["name"],
            is_admin=data["isAdmin"],
        )


@dataclass
class GroupMembersResult:
    """A list of group members."""

    members: List[GroupMember]

    @classmethod
    def from_dict(cls, data: List[Dict[str, Any]]) -> "GroupMembersResult":
        return cls(members=[GroupMember.from_dict(item) for item in data])


@dataclass
class GroupResult:
    """A Habbo group."""

    id: str
    name: str
    description: str
    type: GroupType
    room_id: str
    badge_code: str
    primary_colour: str
    secondary_colour: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupResult":
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            type=GroupType.from_string(data["type"]),
            room_id=data["roomId"],
            badge_code=data["badgeCode"],
            primary_colour=data["primaryColour"],
            secondary_colour=data["secondaryColour"],
        )
