from __future__ import annotations

from typing import List

from ..datatypes.marketplace import MarketPlaceStatsBatchResult
from .abstract_resource import AbstractResource


class MarketPlaceResource(AbstractResource):
    """Allows access to the endpoints for the marketplace."""

    def stats_batch(
        self, floor_items: List[str], wall_items: List[str]
    ) -> MarketPlaceStatsBatchResult:
        """Provide statistical data for multiple room and wall items.

        Args:
            floor_items: The classnames of the floor furni you want to request data on.
            wall_items: The classnames of the wall furni you want to request data on.
        """
        body = {
            "roomItems": [{"item": item} for item in floor_items],
            "wallItems": [{"item": item} for item in wall_items],
        }
        data = self.transporter.post("/api/public/marketplace/stats/batch", body)
        return MarketPlaceStatsBatchResult.from_dict(data)
