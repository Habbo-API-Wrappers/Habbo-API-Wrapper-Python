from __future__ import annotations

from enum import Enum


class FurniTargetKind(str, Enum):

    FURNI = "furni"
    FURNI_BC = "furni-bc"
    WALL_ITEMS = "wall-items"
    WALL_ITEMS_BC = "wall-items-bc"

    def key(self) -> str:
        return self.value
