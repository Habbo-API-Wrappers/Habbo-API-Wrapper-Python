from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

__all__ = [
    "HolderCountResult",
    "VariableResult",
    "VariablesListResult",
]


@dataclass
class VariableResult:
    """A variable assignment's data."""

    value: int
    creation_time: str
    update_time: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VariableResult":
        return cls(
            value=data["value"],
            creation_time=data["creation_time"],
            update_time=data["update_time"],
        )


@dataclass
class VariablesListResult:
    """A list of all permanent variables in the room."""

    users: List[str]
    furni: List[str]
    global_: List[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VariablesListResult":
        return cls(users=data["users"], furni=data["furni"], global_=data["global"])


@dataclass
class HolderCountResult:
    """The amount of entities that hold a variable."""

    count: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HolderCountResult":
        return cls(count=data["count"])
