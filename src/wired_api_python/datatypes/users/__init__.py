from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .badges import Badge, UserBadgesResult
from .friends import Friend, UserFriendsResult
from .groups import Group, UserGroupsResult
from .rooms import Room, UserRoomsResult

__all__ = [
    "Badge",
    "UserBadgesResult",
    "Friend",
    "UserFriendsResult",
    "Group",
    "UserGroupsResult",
    "Room",
    "UserRoomsResult",
    "SelectedBadge",
    "UserResult",
    "UserProfileResult",
]


@dataclass
class SelectedBadge:
    """A badge worn by a user."""

    badge_index: int
    code: str
    name: str
    description: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SelectedBadge":
        return cls(
            badge_index=data["badgeIndex"],
            code=data["code"],
            name=data["name"],
            description=data["description"],
        )


@dataclass
class UserResult:
    """A user's profile."""

    unique_id: str
    name: str
    figure_string: str
    motto: str
    online: Optional[bool]
    last_access_time: Optional[str]
    member_since: Optional[str]
    profile_visible: bool
    current_level: Optional[int]
    current_level_complete_percent: Optional[int]
    total_experience: Optional[int]
    star_gem_count: Optional[int]
    selected_badges: List[SelectedBadge]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserResult":
        return cls(
            unique_id=data["uniqueId"],
            name=data["name"],
            figure_string=data["figureString"],
            motto=data["motto"],
            online=data.get("online"),
            last_access_time=data.get("lastAccessTime"),
            member_since=data.get("memberSince"),
            profile_visible=data["profileVisible"],
            current_level=data.get("currentLevel"),
            current_level_complete_percent=data.get("currentLevelCompletePercent"),
            total_experience=data.get("totalExperience"),
            star_gem_count=data.get("starGemCount"),
            selected_badges=[
                SelectedBadge.from_dict(item) for item in data["selectedBadges"]
            ],
        )


@dataclass
class UserProfileResult:
    """A user's extended profile."""

    user: UserResult
    groups: List[Group]
    badges: List[Badge]
    friends: List[Friend]
    rooms: List[Room]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserProfileResult":
        return cls(
            user=UserResult.from_dict(data["user"]),
            groups=[Group.from_dict(item) for item in data["groups"]],
            badges=[Badge.from_dict(item) for item in data["badges"]],
            friends=[Friend.from_dict(item) for item in data["friends"]],
            rooms=[Room.from_dict(item) for item in data["rooms"]],
        )
