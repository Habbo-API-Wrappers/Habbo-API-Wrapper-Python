from __future__ import annotations

from ..datatypes.groups import GroupMembersResult, GroupResult
from .abstract_resource import AbstractResource


class GroupsResource(AbstractResource):
    """Allows access to the endpoints for groups."""

    def by_id(self, group_id: str) -> GroupResult:
        """Retrieve detailed information about a specific group identified by its unique ID."""
        data = self.transporter.get(f"/api/public/groups/{group_id}")
        return GroupResult.from_dict(data)

    def members_by_id(self, group_id: str) -> GroupMembersResult:
        """Retrieve a list of members for a specified group, including details."""
        data = self.transporter.get(f"/api/public/groups/{group_id}/members")
        return GroupMembersResult.from_dict(data)
