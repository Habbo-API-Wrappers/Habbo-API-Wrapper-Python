from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class RoomDoorMode(Enum):
    """The door mode of a room."""

    OPEN = "open"
    """The room is open, anyone can enter."""

    CLOSED = "closed"
    """The room is locked, users without rights and not in the group have to ring the bell."""

    PASSWORD = "password"
    """The room is locked, users without rights and not in the group have to enter the
    correct password."""

    FRIENDS = "friends"
    """The room is locked for users the owner is not friends with."""

    @classmethod
    def from_string(cls, s: str) -> "RoomDoorMode":
        """Parse a received string into a :class:`RoomDoorMode`."""
        if s == "closed":
            return cls.CLOSED
        if s == "password":
            return cls.PASSWORD
        if s == "friends":
            return cls.FRIENDS
        return cls.OPEN


@dataclass
class RoomResult:
    """A Habbo room."""

    id: int
    name: str
    description: str
    creation_time: str
    habbo_group_id: Optional[str]
    tags: List[str]
    maximum_visitors: int
    show_owner_name: bool
    owner_name: str
    owner_unique_id: str
    categories: List[str]
    thumbnail_url: str
    image_url: str
    rating: int
    public_room: bool
    door_mode: RoomDoorMode
    unique_id: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RoomResult":
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            creation_time=data["creationTime"],
            habbo_group_id=data.get("habboGroupId"),
            tags=data["tags"],
            maximum_visitors=data["maximumVisitors"],
            show_owner_name=data["showOwnerName"],
            owner_name=data["ownerName"],
            owner_unique_id=data["ownerUniqueId"],
            categories=data["categories"],
            thumbnail_url=data["thumbnailUrl"],
            image_url=data["imageUrl"],
            rating=data["rating"],
            public_room=data["publicRoom"],
            door_mode=RoomDoorMode.from_string(data["doorMode"]),
            unique_id=data["uniqueId"],
        )
