from __future__ import annotations

from ..datatypes.hotlooks import HotLooksResult
from .abstract_resource import AbstractResource


class ListsResource(AbstractResource):
    """Allows access to the list endpoints."""

    def hot_looks(self) -> HotLooksResult:
        """Retrieve a list of popular avatars' "hot looks"."""
        data = self.transporter.get_xml("/api/public/lists/hotlooks")
        return HotLooksResult.from_dict(data)
