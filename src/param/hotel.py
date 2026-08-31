from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    import requests

    from ..client import HabboPublicAPI

_DOMAINS = {
    "BR": "https://www.habbo.com.br/",
    "COM": "https://www.habbo.com/",
    "DE": "https://www.habbo.de/",
    "ES": "https://www.habbo.es/",
    "FI": "https://www.habbo.fi/",
    "FR": "https://www.habbo.fr/",
    "IT": "https://www.habbo.it/",
    "NL": "https://www.habbo.nl/",
    "S2": "https://sandbox.habbo.com/",
    "TR": "https://www.habbo.com.tr/",
}


class Hotel(Enum):

    BR = "BR"
    COM = "COM"
    DE = "DE"
    ES = "ES"
    FI = "FI"
    FR = "FR"
    IT = "IT"
    NL = "NL"
    S2 = "S2"
    TR = "TR"

    @property
    def domain(self) -> str:
        return _DOMAINS[self.value]

    def get_domain(self) -> str:
        return self.domain

    def get_api_wrapper(self, session: Optional["requests.Session"] = None) -> "HabboPublicAPI":

        from ..client import HabboPublicAPI

        return HabboPublicAPI(self.domain, session)
