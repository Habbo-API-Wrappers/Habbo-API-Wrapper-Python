from __future__ import annotations

from ..datatypes.rooms import RoomResult
from .abstract_resource import AbstractResource


class RoomsResource(AbstractResource):
    """Allows access to the endpoints for rooms."""

    def by_id(self, room_id: int) -> RoomResult:
        """Fetch detailed information about a public room identified by its unique ID."""
        data = self.transporter.get(f"/api/public/rooms/{room_id}")
        return RoomResult.from_dict(data)
