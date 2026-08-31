"""Access WIRED variable endpoints for a specific room via
:class:`VariablesResource`, obtained from
``HabboPublicAPI.variables(room_id, wired_read_key, wired_write_key)``.
"""

from __future__ import annotations

from typing import Optional

from ...datatypes.variables import VariablesListResult
from ...transporter import Transporter
from .abstract_variables_resource import AbstractVariablesResource
from .furni_variables import FurniVariablesResource
from .global_variables import GlobalVariablesResource
from .user_variables import UserVariablesResource

__all__ = [
    "AbstractVariablesResource",
    "FurniVariablesResource",
    "GlobalVariablesResource",
    "UserVariablesResource",
    "VariablesResource",
]


class VariablesResource(AbstractVariablesResource):
    """Allows access to the endpoints for variables for a specified room."""

    def __init__(self, room_id: int, transporter: Transporter) -> None:
        super().__init__(room_id, transporter)
        self._user_variables_resource: Optional[UserVariablesResource] = None
        self._furni_variables_resource: Optional[FurniVariablesResource] = None
        self._global_variables_resource: Optional[GlobalVariablesResource] = None

    def list_all(self) -> VariablesListResult:
        """List the names of all permanent variables in the room."""
        data = self.transporter.get(f"/api/public/rooms/{self.room_id}/variables")
        return VariablesListResult.from_dict(data)

    def bulk_delete(self, *var_names: str) -> bool:
        """Delete all variable assignments for the given variables.

        Returns:
            Whether the variable assignments have been removed. Like the PHP
            original, any error talking to the API is swallowed and reported
            as ``False`` rather than raised.
        """
        try:
            self.transporter.post(
                f"/api/public/rooms/{self.room_id}/variables/bulk-delete",
                {"variables": list(var_names)},
            )
            return True
        except Exception:
            return False

    def user(self) -> UserVariablesResource:
        """Access the endpoints related to user variables."""
        if self._user_variables_resource is None:
            self._user_variables_resource = UserVariablesResource(self.room_id, self.transporter)
        return self._user_variables_resource

    def furni(self) -> FurniVariablesResource:
        """Access the endpoints related to furni variables."""
        if self._furni_variables_resource is None:
            self._furni_variables_resource = FurniVariablesResource(self.room_id, self.transporter)
        return self._furni_variables_resource

    def global_(self) -> GlobalVariablesResource:
        """Access the endpoints related to global variables.

        Named ``global_`` (trailing underscore) because ``global`` is a
        reserved word in Python -- the PHP original calls this ``global()``.
        """
        if self._global_variables_resource is None:
            self._global_variables_resource = GlobalVariablesResource(
                self.room_id, self.transporter
            )
        return self._global_variables_resource
