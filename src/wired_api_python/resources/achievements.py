from __future__ import annotations

from ..datatypes.achievements import AchievementsResult, UserAchievementsResult
from .abstract_resource import AbstractResource


class AchievementsResource(AbstractResource):
    """Allows access to the endpoints for achievements."""

    def all(self) -> AchievementsResult:
        """Retrieve a list of all achievements including their details and level requirements."""
        data = self.transporter.get("/api/public/achievements")
        return AchievementsResult.from_dict(data)

    def for_user(self, id: str) -> UserAchievementsResult:
        """Retrieve a list of achievements for a user based on their unique ID."""
        data = self.transporter.get(f"/api/public/achievements/{id}")
        return UserAchievementsResult.from_dict(data)
