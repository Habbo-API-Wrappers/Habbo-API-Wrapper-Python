from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from . import VariableResult


@dataclass
class FurniHolder:
    """A furni holder of a variable."""

    id: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FurniHolder":
        return cls(id=data["id"])


@dataclass
class FurniVariableHolder:
    """A variable assigned to a furni."""

    variable: VariableResult
    furni: Optional[FurniHolder]
    furni_bc: Optional[FurniHolder]
    wall_item: Optional[FurniHolder]
    wall_item_bc: Optional[FurniHolder]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FurniVariableHolder":
        return cls(
            variable=VariableResult.from_dict(data["variable"]),
            furni=FurniHolder.from_dict(data["furni"]) if "furni" in data else None,
            furni_bc=FurniHolder.from_dict(data["furni_bc"]) if "furni_bc" in data else None,
            wall_item=FurniHolder.from_dict(data["wall_item"]) if "wall_item" in data else None,
            wall_item_bc=(
                FurniHolder.from_dict(data["wall_item_bc"]) if "wall_item_bc" in data else None
            ),
        )


@dataclass
class FurniVariableHoldersResult:
    """A page of furni variable holders."""

    items: List[FurniVariableHolder]
    page: int
    size: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FurniVariableHoldersResult":
        return cls(
            items=[FurniVariableHolder.from_dict(item) for item in data["items"]],
            page=data["page"],
            size=data["size"],
        )


@dataclass
class FurniVariableProfileResult:
    """A dictionary of variables assigned to a furni, keyed by variable name."""

    variables: Dict[str, VariableResult]
    furni: Optional[FurniHolder]
    furni_bc: Optional[FurniHolder]
    wall_item: Optional[FurniHolder]
    wall_item_bc: Optional[FurniHolder]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FurniVariableProfileResult":
        return cls(
            variables={
                name: VariableResult.from_dict(item)
                for name, item in data.get("variables", {}).items()
            },
            furni=FurniHolder.from_dict(data["furni"]) if "furni" in data and data["furni"] is not None else None,
            furni_bc=FurniHolder.from_dict(data["furni_bc"]) if "furni_bc" in data and data["furni_bc"] is not None else None,
            wall_item=FurniHolder.from_dict(data["wall_item"]) if "wall_item" in data and data["wall_item"] is not None else None,
            wall_item_bc=(
                FurniHolder.from_dict(data["wall_item_bc"]) if "wall_item_bc" in data and data["wall_item_bc"] is not None else None
            ),
        )
