from __future__ import annotations

from typing import Optional


class HabboApiException(Exception):
    def __init__(
        self,
        message: str,
        code: int = 0,
        response_body: Optional[str] = None,
        previous: Optional[BaseException] = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.response_body = response_body
        self.previous = previous
        if previous is not None:
            self.__cause__ = previous

    def get_response_body(self) -> Optional[str]:
        return self.response_body

    def get_previous(self) -> Optional[BaseException]:
        return self.previous

    def __repr__(self) -> str:  # pragma: no cover - cosmetic only
        return (
            f"HabboApiException(message={str(self)!r}, code={self.code!r}, "
            f"response_body={self.response_body!r})"
        )
