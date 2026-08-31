from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from . import VariableResult


@dataclass
class GlobalVariableProfileResult:
    """A list of permanent global variables in the room."""

    variables: List[VariableResult]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GlobalVariableProfileResult":
        return cls(variables=[VariableResult.from_dict(item) for item in data["variables"]])
