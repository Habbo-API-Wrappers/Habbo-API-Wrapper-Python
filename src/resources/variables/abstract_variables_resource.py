from __future__ import annotations

from ...transporter import Transporter
from ..abstract_resource import AbstractResource


class AbstractVariablesResource(AbstractResource):
    """The base for a variable endpoint resource, scoped to a single room."""

    def __init__(self, room_id: int, transporter: Transporter) -> None:
        super().__init__(transporter)
        self.room_id = room_id
