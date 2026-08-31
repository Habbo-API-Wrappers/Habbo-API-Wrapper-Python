from __future__ import annotations

from typing import Dict, Optional

from ...datatypes.variables import HolderCountResult, VariableResult
from ...datatypes.variables.user_variables import (
    UserVariableHoldersResult,
    UserVariableProfileResult,
)
from ...param.order_by import OrderBy
from ...param.order_dir import OrderDir
from ...param.user_target_kind import UserTargetKind
from .abstract_variables_resource import AbstractVariablesResource
from .batch_builder import UserVarBatchRequestBuilder
from .profile_builder import UserProfileRequestBuilder


class UserVariablesResource(AbstractVariablesResource):
    """Allows access to the endpoints for user variables."""

    def get_variable(
        self, variable_name: str, target_kind: UserTargetKind, entity_id: int
    ) -> VariableResult:
        """Read a single user variable assignment."""
        data = self.transporter.get(
            f"/api/public/rooms/{self.room_id}/variables/user/{variable_name}/"
            f"{target_kind.key()}/{entity_id}"
        )
        return VariableResult.from_dict(data)

    def give_variable(
        self,
        variable_name: str,
        target_kind: UserTargetKind,
        entity_id: int,
        value: int = -1,
    ) -> VariableResult:
        """Assign a variable to a user, pet or bot.

        This method works similarly to ``WIRED Effect: Give Variable`` with the
        "Override existing variable" checkbox enabled.
        """
        data = self.transporter.put(
            f"/api/public/rooms/{self.room_id}/variables/user/{variable_name}/"
            f"{target_kind.key()}/{entity_id}",
            {"value": value},
        )
        return VariableResult.from_dict(data)

    def change_variable(
        self, variable_name: str, target_kind: UserTargetKind, entity_id: int, value: int
    ) -> VariableResult:
        """Change the value of an existing user variable assignment.

        This method works similarly to the "assign" option in
        ``WIRED Effect: Change Variable Value``.
        """
        data = self.transporter.put(
            f"/api/public/rooms/{self.room_id}/variables/user/{variable_name}/"
            f"{target_kind.key()}/{entity_id}",
            {"value": value},
        )
        return VariableResult.from_dict(data)

    def remove_variable(
        self, variable_name: str, target_kind: UserTargetKind, entity_id: int
    ) -> None:
        """Remove the variable from the user, pet or bot.

        This method works similarly to ``WIRED Effect: Remove Variable``.
        """
        self.transporter.delete(
            f"/api/public/rooms/{self.room_id}/variables/user/{variable_name}/"
            f"{target_kind.key()}/{entity_id}"
        )

    def list_holders(
        self,
        variable_name: str,
        target_kind: UserTargetKind,
        order_by: OrderBy = OrderBy.CREATION_TIME,
        order_dir: OrderDir = OrderDir.ASCENDING,
        page: int = 1,
        page_size: int = 50,
    ) -> UserVariableHoldersResult:
        """List all users, pets or bots that hold the variable and their assigned values."""
        data = self.transporter.get(
            f"/api/public/rooms/{self.room_id}/variables/user/{variable_name}/{target_kind.key()}",
            {
                "order_by": order_by.key(),
                "order_dir": order_dir.key(),
                "page": page,
                "size": page_size,
            },
        )
        return UserVariableHoldersResult.from_dict(data)

    def count_holders(self, variable_name: str, target_kind: UserTargetKind) -> HolderCountResult:
        """Get the amount of users, pets or bots that hold the variable."""
        data = self.transporter.get(
            f"/api/public/rooms/{self.room_id}/variables/user/{variable_name}/"
            f"{target_kind.key()}/count"
        )
        return HolderCountResult.from_dict(data)

    def build_batch_request(self, variable_name: str) -> UserVarBatchRequestBuilder:
        """Create a batch request builder to give, change or remove the variable to/from
        multiple users, pets and bots."""
        return UserVarBatchRequestBuilder(variable_name, self.room_id, self.transporter)

    def get_profile_by_username(self, username: str) -> UserVariableProfileResult:
        """List all variables assigned to the user, looked up by username."""
        data = self.transporter.get(
            f"/api/public/rooms/{self.room_id}/variables_profile/user/users",
            {"name": username},
        )
        return UserVariableProfileResult.from_dict(data)

    def get_profile_by_unique_id(self, unique_id: str) -> UserVariableProfileResult:
        """List all variables assigned to the user, looked up by unique ID."""
        data = self.transporter.get(
            f"/api/public/rooms/{self.room_id}/variables_profile/user/users",
            {"unique_id": unique_id},
        )
        return UserVariableProfileResult.from_dict(data)

    def get_profile(
        self, target_kind: UserTargetKind, entity_id: int
    ) -> UserVariableProfileResult:
        """List all variables assigned to the user, pet or bot."""
        data = self.transporter.get(
            f"/api/public/rooms/{self.room_id}/variables_profile/user/"
            f"{target_kind.key()}/{entity_id}"
        )
        return UserVariableProfileResult.from_dict(data)

    def remove_profile(self, target_kind: UserTargetKind, entity_id: int) -> None:
        """Remove all variables assigned to the user, pet or bot."""
        self.transporter.delete(
            f"/api/public/rooms/{self.room_id}/variables_profile/user/"
            f"{target_kind.key()}/{entity_id}"
        )

    def change_profile(
        self,
        target_kind: UserTargetKind,
        entity_id: int,
        variables: Dict[str, Optional[int]],
    ) -> UserVariableProfileResult:
        """Change variables assigned to the user, pet or bot.

        Args:
            variables: The new values for the variables, keyed by variable name.
                Assigning ``None`` removes the variable.
        """
        data = self.transporter.patch(
            f"/api/public/rooms/{self.room_id}/variables_profile/user/"
            f"{target_kind.key()}/{entity_id}",
            {"variables": variables},
        )
        return UserVariableProfileResult.from_dict(data)

    def build_change_profile_request(
        self, target_kind: UserTargetKind, entity_id: int
    ) -> UserProfileRequestBuilder:
        """Create a profile request builder."""
        return UserProfileRequestBuilder(target_kind, entity_id, self.room_id, self.transporter)
