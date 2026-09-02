from __future__ import annotations

from typing import Optional

import requests

from .param.hotel import Hotel
from .resources.achievements import AchievementsResource
from .resources.badges import BadgesResource
from .resources.groups import GroupsResource
from .resources.lists import ListsResource
from .resources.marketplace import MarketPlaceResource
from .resources.rooms import RoomsResource
from .resources.users import UsersResource
from .resources.variables import VariablesResource
from .transporter import Transporter


class HabboPublicAPI:

    def __init__(self, base_domain: str, session: Optional[requests.Session] = None) -> None:
        self._transporter = Transporter(base_domain, session)
        self._achievements: Optional[AchievementsResource] = None
        self._badges: Optional[BadgesResource] = None
        self._groups: Optional[GroupsResource] = None
        self._marketplace: Optional[MarketPlaceResource] = None
        self._rooms: Optional[RoomsResource] = None
        self._lists: Optional[ListsResource] = None
        self._users: Optional[UsersResource] = None

    @classmethod
    def from_hotel(cls, hotel: Hotel, session: Optional[requests.Session] = None) -> "HabboPublicAPI":

        return cls(hotel.domain, session)

    def achievements(self) -> AchievementsResource:
        """Access the achievement related endpoints."""
        if self._achievements is None:
            self._achievements = AchievementsResource(self._transporter)
        return self._achievements

    def badges(self) -> BadgesResource:
        """Access the badge related endpoints."""
        if self._badges is None:
            self._badges = BadgesResource(self._transporter)
        return self._badges

    def groups(self) -> GroupsResource:
        """Access the group related endpoints."""
        if self._groups is None:
            self._groups = GroupsResource(self._transporter)
        return self._groups

    def marketplace(self) -> MarketPlaceResource:
        """Access the marketplace related endpoints."""
        if self._marketplace is None:
            self._marketplace = MarketPlaceResource(self._transporter)
        return self._marketplace

    def rooms(self) -> RoomsResource:
        """Access the room related endpoints."""
        if self._rooms is None:
            self._rooms = RoomsResource(self._transporter)
        return self._rooms

    def lists(self) -> ListsResource:
        """Access the list related endpoints."""
        if self._lists is None:
            self._lists = ListsResource(self._transporter)
        return self._lists

    def users(self) -> UsersResource:
        """Access the user related endpoints."""
        if self._users is None:
            self._users = UsersResource(self._transporter)
        return self._users

    def variables(self, room_id: int, wired_read_key: str, wired_write_key: str) -> VariablesResource:
        return VariablesResource(
            room_id,
            self._transporter.extend_with_headers(
                {
                    "X-Wired-Read-Key": wired_read_key,
                    "X-Wired-Write-Key": wired_write_key,
                }
            ),
        )

    def ping(self) -> bool:
        try:
            self._transporter.get("/api/public/ping")
            return True
        except Exception:
            return False
