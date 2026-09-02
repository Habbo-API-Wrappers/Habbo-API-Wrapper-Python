from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class HotLook:
    """A "hot look" outfit."""

    gender: str
    figure: str
    hash: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HotLook":
        return cls(gender=data["GENDER"], figure=data["FIGURE"], hash=data["HASH"])


@dataclass
class HotLooksResult:
    """The list of current hot looks."""

    url: str
    looks: List[HotLook]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HotLooksResult":
        habbos = data["HABBOS"][0]
        return cls(
            url=habbos["URL"],
            looks=[HotLook.from_dict(item) for item in habbos["HABBO"]],
        )
