"""Request builders that let you give, change, remove or read the same
variable for multiple furni / users / pets / bots in a single request.
"""

from __future__ import annotations

from typing import Any, Dict, List

from ...datatypes.variables.batch_request import BatchResult
from ...furni_id_sanitiser import sanitise_furni_id
from ...param.furni_target_kind import FurniTargetKind
from ...param.user_target_kind import UserTargetKind
from ...transporter import Transporter
from .abstract_variables_resource import AbstractVariablesResource


class FurniVarBatchRequestBuilder(AbstractVariablesResource):
    """A request builder to build a batch request for a furni variable."""

    def __init__(self, var_name: str, room_id: int, transporter: Transporter) -> None:
        super().__init__(room_id, transporter)
        self._var_name = var_name
        self._requests: List[Dict[str, Any]] = []

    def get_variable(
        self, op_id: str, target_kind: FurniTargetKind, furni_id: int
    ) -> "FurniVarBatchRequestBuilder":
        """Get the value of a variable."""
        furni_id = sanitise_furni_id(furni_id)
        self._requests.append(
            {"op_id": op_id, "method": "GET", "path": f"{target_kind.key()}/{furni_id}"}
        )
        return self

    def give_variable(
        self,
        op_id: str,
        target_kind: FurniTargetKind,
        furni_id: int,
        value: int = -1,
    ) -> "FurniVarBatchRequestBuilder":
        """Assign a variable to a furni."""
        furni_id = sanitise_furni_id(furni_id)
        self._requests.append(
            {
                "op_id": op_id,
                "method": "PUT",
                "path": f"{target_kind.key()}/{furni_id}",
                "body": {"value": value},
            }
        )
        return self

    def change_variable(
        self, op_id: str, target_kind: FurniTargetKind, furni_id: int, value: int
    ) -> "FurniVarBatchRequestBuilder":
        """Change the value of a variable assigned to a furni."""
        furni_id = sanitise_furni_id(furni_id)
        self._requests.append(
            {
                "op_id": op_id,
                "method": "PATCH",
                "path": f"{target_kind.key()}/{furni_id}",
                "body": {"value": value},
            }
        )
        return self

    def remove_variable(
        self, op_id: str, target_kind: FurniTargetKind, furni_id: int
    ) -> "FurniVarBatchRequestBuilder":
        """Remove a variable assigned to a furni."""
        furni_id = sanitise_furni_id(furni_id)
        self._requests.append(
            {"op_id": op_id, "method": "DELETE", "path": f"{target_kind.key()}/{furni_id}"}
        )
        return self

    def execute_request(self) -> BatchResult:
        """Execute the built batch request."""
        data = self.transporter.post(
            f"/api/public/rooms/{self.room_id}/variables/furni/{self._var_name}/batch",
            {"requests": self._requests},
        )
        return BatchResult.from_dict(data)


class UserVarBatchRequestBuilder(AbstractVariablesResource):
    """A request builder to build a batch request for a user variable."""

    def __init__(self, var_name: str, room_id: int, transporter: Transporter) -> None:
        super().__init__(room_id, transporter)
        self._var_name = var_name
        self._requests: List[Dict[str, Any]] = []

    def get_variable(
        self, op_id: str, target_kind: UserTargetKind, entity_id: int
    ) -> "UserVarBatchRequestBuilder":
        """Get the value of a variable."""
        self._requests.append(
            {"op_id": op_id, "method": "GET", "path": f"{target_kind.key()}/{entity_id}"}
        )
        return self

    def give_variable(
        self,
        op_id: str,
        target_kind: UserTargetKind,
        entity_id: int,
        value: int = -1,
    ) -> "UserVarBatchRequestBuilder":
        """Assign a variable to a user, pet or bot."""
        self._requests.append(
            {
                "op_id": op_id,
                "method": "PUT",
                "path": f"{target_kind.key()}/{entity_id}",
                "body": {"value": value},
            }
        )
        return self

    def change_variable(
        self, op_id: str, target_kind: UserTargetKind, entity_id: int, value: int
    ) -> "UserVarBatchRequestBuilder":
        """Change the value of a variable assigned to a user, pet or bot."""
        self._requests.append(
            {
                "op_id": op_id,
                "method": "PATCH",
                "path": f"{target_kind.key()}/{entity_id}",
                "body": {"value": value},
            }
        )
        return self

    def remove_variable(
        self, op_id: str, target_kind: UserTargetKind, entity_id: int
    ) -> "UserVarBatchRequestBuilder":
        """Remove a variable assigned to a user, pet or bot."""
        self._requests.append(
            {"op_id": op_id, "method": "DELETE", "path": f"{target_kind.key()}/{entity_id}"}
        )
        return self

    def execute_request(self) -> BatchResult:
        """Execute the built batch request."""
        data = self.transporter.post(
            f"/api/public/rooms/{self.room_id}/variables/user/{self._var_name}/batch",
            {"requests": self._requests},
        )
        return BatchResult.from_dict(data)
