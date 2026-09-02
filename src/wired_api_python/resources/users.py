from __future__ import annotations

from ..datatypes.users import (
    UserBadgesResult,
    UserFriendsResult,
    UserGroupsResult,
    UserProfileResult,
    UserResult,
    UserRoomsResult,
)
from .abstract_resource import AbstractResource


class UsersResource(AbstractResource):
    """Allows access to the endpoints for users."""

    def by_name(self, name: str) -> UserResult:
        """Retrieve user information by name.

        Less information is shown for users with limited profile visibility.
        """
        data = self.transporter.get("/api/public/users", {"name": name})
        return UserResult.from_dict(data)

    def by_unique_id(self, unique_id: str) -> UserResult:
        """Retrieve detailed public information about a user by their unique ID.

        Less information is shown for users with limited profile visibility.
        """
        data = self.transporter.get(f"/api/public/users/{unique_id}")
        return UserResult.from_dict(data)

    def friends(self, unique_id: str) -> UserFriendsResult:
        """Fetch a list of friends for a user identified by their unique ID.

        Only returned if the user is found and the profile is visible.
        """
        data = self.transporter.get(f"/api/public/users/{unique_id}/friends")
        return UserFriendsResult.from_dict(data)

    def groups(self, unique_id: str) -> UserGroupsResult:
        """Fetch a list of groups that a user is a member of, identified by their unique ID."""
        data = self.transporter.get(f"/api/public/users/{unique_id}/groups")
        return UserGroupsResult.from_dict(data)

    def rooms(self, unique_id: str) -> UserRoomsResult:
        """Fetch a list of public rooms that a user owns, identified by their unique ID."""
        data = self.transporter.get(f"/api/public/users/{unique_id}/rooms")
        return UserRoomsResult.from_dict(data)

    def badges(self, unique_id: str) -> UserBadgesResult:
        """Fetch a list of badges that a user has earned, identified by their unique ID."""
        data = self.transporter.get(f"/api/public/users/{unique_id}/badges")
        return UserBadgesResult.from_dict(data)

    def profile(self, unique_id: str) -> UserProfileResult:
        """Fetch detailed profile information for a user identified by their unique ID."""
        data = self.transporter.get(f"/api/public/users/{unique_id}/profile")
        return UserProfileResult.from_dict(data)
