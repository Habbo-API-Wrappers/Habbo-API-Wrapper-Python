from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from . import VariableResult


@dataclass
class BatchError:
    """An error that occurred in a batch request."""

    code: str
    message: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BatchError":
        return cls(code=data["code"], message=data["message"])


@dataclass
class BatchResultEntry:
    """The result of a single batch request entry."""

    op_id: str
    status: int
    body: Optional[VariableResult]
    error: Optional[BatchError]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BatchResultEntry":
        return cls(
            op_id=data["op_id"],
            status=data["status"],
            body=VariableResult.from_dict(data["body"]) if "body" in data else None,
            error=BatchError.from_dict(data["error"]) if "error" in data else None,
        )


@dataclass
class BatchResult:
    """The result of a batch request."""

    results: List[BatchResultEntry]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BatchResult":
        return cls(results=[BatchResultEntry.from_dict(item) for item in data["results"]])
