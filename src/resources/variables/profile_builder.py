"""Request builders that let you change several variables assigned to a single
target (a furni, a user/pet/bot, or the room's global variables) in one
request.
"""

from __future__ import annotations

from typing import Dict, Optional

from ...datatypes.variables.furni_variables import FurniVariableProfileResult
from ...datatypes.variables.global_variables import GlobalVariableProfileResult
from ...datatypes.variables.user_variables import UserVariableProfileResult
from ...furni_id_sanitiser import sanitise_furni_id
from ...param.furni_target_kind import FurniTargetKind
from ...param.user_target_kind import UserTargetKind
from ...transporter import Transporter
from .abstract_variables_resource import AbstractVariablesResource


class FurniProfileRequestBuilder(AbstractVariablesResource):
    """A furni variable profile request builder.

    Allows changing multiple variables assigned to a single furni at once.
    """

    def __init__(
        self,
        target_kind: FurniTargetKind,
        furni_id: int,
        room_id: int,
        transporter: Transporter,
    ) -> None:
        super().__init__(room_id, transporter)
        self._target_kind = target_kind
        self._furni_id = furni_id
        self._variables: Dict[str, Optional[int]] = {}

    def change_or_give_variable(self, variable_name: str, value: int = -1) -> "FurniProfileRequestBuilder":
        """Change the value of a variable assignment, or give a new one."""
        self._variables[variable_name] = value
        return self

    def remove_variable(self, variable_name: str) -> "FurniProfileRequestBuilder":
        """Remove a variable assignment."""
        self._variables[variable_name] = None
        return self

    def execute_request(self) -> FurniVariableProfileResult:
        """Execute the built request."""
        furni_id = sanitise_furni_id(self._furni_id)
        data = self.transporter.patch(
            f"/api/public/rooms/{self.room_id}/variables_profile/furni/"
            f"{self._target_kind.key()}/{furni_id}",
            {"variables": self._variables},
        )
        return FurniVariableProfileResult.from_dict(data)


class GlobalProfileRequestBuilder(AbstractVariablesResource):
    """A global variable profile request builder.

    Allows changing multiple global variables at once.
    """

    def __init__(self, room_id: int, transporter: Transporter) -> None:
        super().__init__(room_id, transporter)
        self._variables: Dict[str, int] = {}

    def change_variable(self, variable_name: str, value: int) -> "GlobalProfileRequestBuilder":
        """Change the value of a variable."""
        self._variables[variable_name] = value
        return self

    def execute_request(self) -> GlobalVariableProfileResult:
        """Execute the built request."""
        data = self.transporter.patch(
            f"/api/public/rooms/{self.room_id}/variables_profile/global",
            {"variables": self._variables},
        )
        return GlobalVariableProfileResult.from_dict(data)


class UserProfileRequestBuilder(AbstractVariablesResource):
    """A user variable profile request builder.

    Allows changing multiple variables assigned to a single user, pet or bot at once.
    """

    def __init__(
        self,
        target_kind: UserTargetKind,
        entity_id: int,
        room_id: int,
        transporter: Transporter,
    ) -> None:
        super().__init__(room_id, transporter)
        self._target_kind = target_kind
        self._entity_id = entity_id
        self._variables: Dict[str, Optional[int]] = {}

    def change_or_give_variable(self, variable_name: str, value: int = -1) -> "UserProfileRequestBuilder":
        """Change the value of a variable assignment, or give a new one."""
        self._variables[variable_name] = value
        return self

    def remove_variable(self, variable_name: str) -> "UserProfileRequestBuilder":
        """Remove a variable assignment."""
        self._variables[variable_name] = None
        return self

    def execute_request(self) -> UserVariableProfileResult:
        """Execute the built request."""
        data = self.transporter.patch(
            f"/api/public/rooms/{self.room_id}/variables_profile/user/"
            f"{self._target_kind.key()}/{self._entity_id}",
            {"variables": self._variables},
        )
        return UserVariableProfileResult.from_dict(data)
