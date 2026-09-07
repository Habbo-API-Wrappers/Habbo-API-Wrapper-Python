from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from . import VariableResult


@dataclass
class BotHolder:
    """A bot holder of a variable."""

    name: str
    id: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BotHolder":
        return cls(name=data["name"], id=data["id"])


@dataclass
class PetHolder:
    """A pet holder of a variable."""

    name: str
    id: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PetHolder":
        return cls(name=data["name"], id=data["id"])


@dataclass
class UserHolder:
    """A user holder of a variable."""

    unique_id: str
    name: str
    id: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserHolder":
        return cls(unique_id=data["unique_id"], name=data["name"], id=data["id"])


@dataclass
class UserVariableHolder:
    """A variable assigned to a user, pet or bot."""

    variable: VariableResult
    user: Optional[UserHolder]
    pet: Optional[PetHolder]
    bot: Optional[BotHolder]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserVariableHolder":
        return cls(
            variable=VariableResult.from_dict(data["variable"]),
            user=UserHolder.from_dict(data["user"]) if "user" in data else None,
            pet=PetHolder.from_dict(data["pet"]) if "pet" in data else None,
            bot=BotHolder.from_dict(data["bot"]) if "bot" in data else None,
        )


@dataclass
class UserVariableHoldersResult:
    """A page of user variable holders."""

    items: List[UserVariableHolder]
    page: int
    size: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserVariableHoldersResult":
        return cls(
            items=[UserVariableHolder.from_dict(item) for item in data["items"]],
            page=data["page"],
            size=data["size"],
        )


@dataclass
class UserVariableProfileResult:
    """A dictionary of variables assigned to a user, pet or bot, keyed by variable name."""

    variables: Dict[str, VariableResult]
    user: Optional[UserHolder]
    pet: Optional[PetHolder]
    bot: Optional[BotHolder]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserVariableProfileResult":
        return cls(
            variables={
                name: VariableResult.from_dict(item)
                for name, item in data.get("variables", {}).items()
            },
            user=UserHolder.from_dict(data["user"]) if "user" in data and data["user"] is not None else None,
            pet=PetHolder.from_dict(data["pet"]) if "pet" in data and data["pet"] is not None else None,
            bot=BotHolder.from_dict(data["bot"]) if "bot" in data and data["bot"] is not None else None,
        )
