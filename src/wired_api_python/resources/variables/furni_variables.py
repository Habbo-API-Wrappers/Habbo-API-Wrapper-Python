from __future__ import annotations

from typing import Dict, Optional

from ...datatypes.variables import HolderCountResult, VariableResult
from ...datatypes.variables.furni_variables import (
    FurniVariableHoldersResult,
    FurniVariableProfileResult,
)
from ...furni_id_sanitiser import sanitise_furni_id
from ...param.furni_target_kind import FurniTargetKind
from ...param.order_by import OrderBy
from ...param.order_dir import OrderDir
from .abstract_variables_resource import AbstractVariablesResource
from .batch_builder import FurniVarBatchRequestBuilder
from .profile_builder import FurniProfileRequestBuilder


class FurniVariablesResource(AbstractVariablesResource):
    """Allows access to the endpoints for furni variables."""

    def get_variable(
        self, variable_name: str, target_kind: FurniTargetKind, furni_id: int
    ) -> VariableResult:
        """Read a single furni variable assignment."""
        furni_id = sanitise_furni_id(furni_id)
        data = self.transporter.get(
            f"/api/public/rooms/{self.room_id}/variables/furni/{variable_name}/"
            f"{target_kind.key()}/{furni_id}"
        )
        return VariableResult.from_dict(data)

    def give_variable(
        self,
        variable_name: str,
        target_kind: FurniTargetKind,
        furni_id: int,
        value: int = -1,
    ) -> VariableResult:
        """Assign a variable to a furni.

        This method works similarly to ``WIRED Effect: Give Variable`` with the
        "Override existing variable" checkbox enabled.
        """
        furni_id = sanitise_furni_id(furni_id)
        data = self.transporter.put(
            f"/api/public/rooms/{self.room_id}/variables/furni/{variable_name}/"
            f"{target_kind.key()}/{furni_id}",
            {"value": value},
        )
        return VariableResult.from_dict(data)

    def change_variable(
        self, variable_name: str, target_kind: FurniTargetKind, furni_id: int, value: int
    ) -> VariableResult:
        """Change the value of an existing furni variable assignment.

        This method works similarly to the "assign" option in
        ``WIRED Effect: Change Variable Value``.
        """
        furni_id = sanitise_furni_id(furni_id)
        data = self.transporter.patch(
            f"/api/public/rooms/{self.room_id}/variables/furni/{variable_name}/"
            f"{target_kind.key()}/{furni_id}",
            {"value": value},
        )
        return VariableResult.from_dict(data)

    def remove_variable(
        self, variable_name: str, target_kind: FurniTargetKind, furni_id: int
    ) -> None:
        """Remove the variable from the furni.

        This method works similarly to ``WIRED Effect: Remove Variable``.
        """
        furni_id = sanitise_furni_id(furni_id)
        self.transporter.delete(
            f"/api/public/rooms/{self.room_id}/variables/furni/{variable_name}/"
            f"{target_kind.key()}/{furni_id}"
        )

    def list_holders(
        self,
        variable_name: str,
        target_kind: FurniTargetKind,
        order_by: OrderBy = OrderBy.CREATION_TIME,
        order_dir: OrderDir = OrderDir.ASCENDING,
        page: int = 1,
        page_size: int = 50,
    ) -> FurniVariableHoldersResult:
        """List all furni that hold the variable and their assigned values."""
        data = self.transporter.get(
            f"/api/public/rooms/{self.room_id}/variables/furni/{variable_name}/{target_kind.key()}",
            {
                "order_by": order_by.key(),
                "order_dir": order_dir.key(),
                "page": page,
                "size": page_size,
            },
        )
        return FurniVariableHoldersResult.from_dict(data)

    def count_holders(self, variable_name: str, target_kind: FurniTargetKind) -> HolderCountResult:
        """Get the amount of furni that hold the variable."""
        data = self.transporter.get(
            f"/api/public/rooms/{self.room_id}/variables/furni/{variable_name}/"
            f"{target_kind.key()}/count"
        )
        return HolderCountResult.from_dict(data)

    def build_batch_request(self, variable_name: str) -> FurniVarBatchRequestBuilder:
        """Create a batch request builder to give, change or remove the variable to/from
        multiple furni."""
        return FurniVarBatchRequestBuilder(variable_name, self.room_id, self.transporter)

    def get_profile(
        self, target_kind: FurniTargetKind, furni_id: int
    ) -> FurniVariableProfileResult:
        """List all variables assigned to the furni."""
        furni_id = sanitise_furni_id(furni_id)
        data = self.transporter.get(
            f"/api/public/rooms/{self.room_id}/variables_profile/furni/"
            f"{target_kind.key()}/{furni_id}"
        )
        return FurniVariableProfileResult.from_dict(data)

    def change_profile(
        self,
        target_kind: FurniTargetKind,
        furni_id: int,
        variables: Dict[str, Optional[int]],
    ) -> FurniVariableProfileResult:
        """Change variables assigned to the furni.

        Args:
            variables: The new values for the variables, keyed by variable name.
                Assigning ``None`` removes the variable.
        """
        furni_id = sanitise_furni_id(furni_id)
        data = self.transporter.patch(
            f"/api/public/rooms/{self.room_id}/variables_profile/furni/"
            f"{target_kind.key()}/{furni_id}",
            {"variables": variables},
        )
        return FurniVariableProfileResult.from_dict(data)

    def build_change_profile_request(
        self, target_kind: FurniTargetKind, furni_id: int
    ) -> FurniProfileRequestBuilder:
        """Create a profile request builder."""
        return FurniProfileRequestBuilder(target_kind, furni_id, self.room_id, self.transporter)
