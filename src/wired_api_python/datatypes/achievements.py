from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List


class AchievementState(Enum):
    """The state of an achievement."""

    ENABLED = "ENABLED"
    """The achievement is currently enabled in game."""

    OFF_SEASON = "OFF_SEASON"
    """The achievement is currently not available."""

    ARCHIVED = "ARCHIVED"
    """The achievement is no longer available."""

    @classmethod
    def from_string(cls, s: str) -> "AchievementState":
        """Parse a received string into an :class:`AchievementState`."""
        if s == "ENABLED":
            return cls.ENABLED
        if s == "OFF_SEASON":
            return cls.OFF_SEASON
        return cls.ARCHIVED


@dataclass
class AchievementData:
    """The metadata of an achievement."""

    id: int
    name: str
    creation_time: str
    state: AchievementState
    category: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AchievementData":
        return cls(
            id=data["id"],
            name=data["name"],
            creation_time=data["creationTime"],
            state=AchievementState.from_string(data["state"]),
            category=data["category"],
        )


@dataclass
class LevelRequirement:
    """The required score for a level of an achievement."""

    level: int
    required_score: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LevelRequirement":
        return cls(level=data["level"], required_score=data["requiredScore"])


@dataclass
class Achievement:
    """An achievement and its level requirements."""

    achievement: AchievementData
    level_requirements: List[LevelRequirement]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Achievement":
        return cls(
            achievement=AchievementData.from_dict(data["achievement"]),
            level_requirements=[
                LevelRequirement.from_dict(item) for item in data["levelRequirements"]
            ],
        )


@dataclass
class AchievementsResult:
    """A list of achievements."""

    achievements: List[Achievement]

    @classmethod
    def from_dict(cls, data: List[Dict[str, Any]]) -> "AchievementsResult":
        return cls(achievements=[Achievement.from_dict(item) for item in data])


@dataclass
class UserAchievement:
    """An achievement held by a user."""

    achievement: AchievementData
    level: int
    score: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserAchievement":
        return cls(
            achievement=AchievementData.from_dict(data["achievement"]),
            level=data["level"],
            score=data["score"],
        )


@dataclass
class UserAchievementsResult:
    """A list of user achievements."""

    achievements: List[UserAchievement]

    @classmethod
    def from_dict(cls, data: List[Dict[str, Any]]) -> "UserAchievementsResult":
        return cls(achievements=[UserAchievement.from_dict(item) for item in data])
