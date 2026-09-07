from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from . import VariableResult


@dataclass
class GlobalVariableProfileResult:
    """A dictionary of permanent global variables in the room, keyed by variable name."""

    variables: Dict[str, VariableResult]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GlobalVariableProfileResult":
        return cls(
            variables={
                name: VariableResult.from_dict(item)
                for name, item in data.get("variables", {}).items()
            }
        )
