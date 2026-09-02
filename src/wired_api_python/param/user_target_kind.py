from __future__ import annotations

from enum import Enum


class UserTargetKind(str, Enum):
    """The kind of entity a WIRED variable endpoint targets."""

    USERS = "users"
    PETS = "pets"
    BOTS = "bots"

    def key(self) -> str:
        """The path-segment value for this option."""
        return self.value
