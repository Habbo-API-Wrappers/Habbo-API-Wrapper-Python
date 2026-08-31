from __future__ import annotations

from ..transporter import Transporter


class AbstractResource:
    """The base for an endpoint resource."""

    def __init__(self, transporter: Transporter) -> None:
        self.transporter = transporter
