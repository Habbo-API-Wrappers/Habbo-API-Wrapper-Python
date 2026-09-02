from __future__ import annotations

from typing import Dict

from ...datatypes.variables import VariableResult
from ...datatypes.variables.global_variables import GlobalVariableProfileResult
from .abstract_variables_resource import AbstractVariablesResource
from .profile_builder import GlobalProfileRequestBuilder


class GlobalVariablesResource(AbstractVariablesResource):
    """Allows access to the endpoints for global variables."""

    def get_variable(self, var_name: str) -> VariableResult:
        """Get the value of a variable."""
        data = self.transporter.get(f"/api/public/rooms/{self.room_id}/variables/global/{var_name}")
        return VariableResult.from_dict(data)

    def change_variable(self, var_name: str, value: int) -> VariableResult:
        """Change the value of a variable."""
        data = self.transporter.patch(
            f"/api/public/rooms/{self.room_id}/variables/global/{var_name}",
            {"value": value},
        )
        return VariableResult.from_dict(data)

    def get_profile(self) -> GlobalVariableProfileResult:
        """List all global variables and their values."""
        data = self.transporter.get(f"/api/public/rooms/{self.room_id}/variables_profile/global")
        return GlobalVariableProfileResult.from_dict(data)

    def change_profile(self, variables: Dict[str, int]) -> GlobalVariableProfileResult:
        """Change multiple global variable values.

        Args:
            variables: The new values for the variables, keyed by variable name.
        """
        data = self.transporter.patch(
            f"/api/public/rooms/{self.room_id}/variables_profile/global",
            {"variables": variables},
        )
        return GlobalVariableProfileResult.from_dict(data)

    def build_change_profile_request(self) -> GlobalProfileRequestBuilder:
        """Create a profile request builder."""
        return GlobalProfileRequestBuilder(self.room_id, self.transporter)
