from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Room:
    """A room, as requested through a user (owner's public rooms)."""

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
    unique_id: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Room":
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
            unique_id=data["uniqueId"],
        )


@dataclass
class UserRoomsResult:
    """A list of rooms owned by a user."""

    rooms: List[Room]

    @classmethod
    def from_dict(cls, data: List[Dict[str, Any]]) -> "UserRoomsResult":
        return cls(rooms=[Room.from_dict(item) for item in data])
