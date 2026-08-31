from __future__ import annotations

from enum import Enum


class OrderBy(str, Enum):
    """What value a variable holders listing should be ordered by."""

    VALUE = "value"
    CREATION_TIME = "creation_time"
    UPDATE_TIME = "update_time"

    def key(self) -> str:
        """The query-parameter value for this option."""
        return self.value
