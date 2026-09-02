from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class MarketPlaceHistory:
    """A marketplace history entry."""

    day_offset: str
    average_price: str
    total_sold_items: str
    total_credit_sum: str
    total_open_offers: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MarketPlaceHistory":
        return cls(
            day_offset=data["dayOffset"],
            average_price=data["averagePrice"],
            total_sold_items=data["totalSoldItems"],
            total_credit_sum=data["totalCreditSum"],
            total_open_offers=data["totalOpenOffers"],
        )


@dataclass
class MarketPlaceItemData:
    """The marketplace data for an item."""

    item: str
    stats_date: str
    history: List[MarketPlaceHistory]
    sold_item_count: int
    credit_sum: int
    average_price: int
    total_open_offers: int
    current_open_offers: int
    current_price: int
    history_limit_in_days: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MarketPlaceItemData":
        return cls(
            item=data["item"],
            stats_date=data["statsDate"],
            history=[MarketPlaceHistory.from_dict(item) for item in data["history"]],
            sold_item_count=data["soldItemCount"],
            credit_sum=data["creditSum"],
            average_price=data["averagePrice"],
            total_open_offers=data["totalOpenOffers"],
            current_open_offers=data["currentOpenOffers"],
            current_price=data["currentPrice"],
            history_limit_in_days=data["historyLimitInDays"],
        )


@dataclass
class MarketPlaceStatsBatchResult:
    """The response of a marketplace batch request."""

    status: str
    room_item_data: List[MarketPlaceItemData]
    wall_item_data: List[MarketPlaceItemData]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MarketPlaceStatsBatchResult":
        return cls(
            status=data["status"],
            room_item_data=[
                MarketPlaceItemData.from_dict(item) for item in data["roomItemData"]
            ],
            wall_item_data=[
                MarketPlaceItemData.from_dict(item) for item in data["wallItemData"]
            ],
        )
