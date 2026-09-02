"""Endpoint resources for the Habbo public API."""

from .abstract_resource import AbstractResource
from .achievements import AchievementsResource
from .badges import BadgesResource
from .groups import GroupsResource
from .lists import ListsResource
from .marketplace import MarketPlaceResource
from .rooms import RoomsResource
from .users import UsersResource

__all__ = [
    "AbstractResource",
    "AchievementsResource",
    "BadgesResource",
    "GroupsResource",
    "ListsResource",
    "MarketPlaceResource",
    "RoomsResource",
    "UsersResource",
]
