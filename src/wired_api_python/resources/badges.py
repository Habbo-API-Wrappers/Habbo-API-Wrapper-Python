from __future__ import annotations

from ..datatypes.badges import BadgeOwnersResult
from .abstract_resource import AbstractResource


class BadgesResource(AbstractResource):
    """Allows access to the endpoints for badges."""

    def owner_count(self, badge_code: str) -> BadgeOwnersResult:
        """Return the amount of users who own the badge plus localized name/description."""
        data = self.transporter.get(f"/api/public/badge/owners/{badge_code}")
        return BadgeOwnersResult.from_dict(data)
