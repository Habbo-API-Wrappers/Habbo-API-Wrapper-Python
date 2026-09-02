from __future__ import annotations

from enum import Enum


class OrderDir(str, Enum):
    """Whether a variable holders listing is ascending or descending."""

    ASCENDING = "asc"
    DESCENDING = "desc"

    def key(self) -> str:
        """The query-parameter value for this option."""
        return self.value
