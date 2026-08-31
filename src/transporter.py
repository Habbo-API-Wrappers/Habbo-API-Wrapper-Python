from __future__ import annotations

import json
from typing import Any, Dict, Mapping, Optional
from xml.etree.ElementTree import ParseError as XmlParseError

import requests

from .exceptions import HabboApiException
from .xml_cleaner import XmlCleaner

_USER_AGENT = "WiredApiWrapper/1.0"


class Transporter:
    def __init__(
        self,
        base_url: str,
        session: Optional[requests.Session] = None,
        additional_headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._session = session if session is not None else requests.Session()
        self._additional_headers: Dict[str, str] = dict(additional_headers or {})

    def extend_with_headers(self, new_additional_headers: Mapping[str, str]) -> "Transporter":
        """Create a cloned transporter extended with the given new headers.

        Args:
            new_additional_headers: The headers to add to the cloned instance.

        Returns:
            A new transporter instance sharing this one's session and base URL.
        """
        merged = {**self._additional_headers, **new_additional_headers}
        return Transporter(self._base_url, self._session, merged)

    def get(self, path: str, query: Optional[Mapping[str, Any]] = None) -> Any:
        """Perform a GET request and parse the response as JSON."""
        response = self._send("GET", path, query=query)
        return self._handle_json_response(response)

    def get_xml(self, path: str, query: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
        """Perform a GET request and parse the response as XML."""
        response = self._send("GET", path, query=query, accept_type="application/xml")
        return self._handle_xml_response(response)

    def post(
        self, path: str, request_body: Any, query: Optional[Mapping[str, Any]] = None
    ) -> Any:
        """Perform a POST request and parse the response as JSON."""
        response = self._send("POST", path, query=query, body=request_body)
        return self._handle_json_response(response)

    def put(
        self, path: str, request_body: Any, query: Optional[Mapping[str, Any]] = None
    ) -> Any:
        """Perform a PUT request and parse the response as JSON."""
        response = self._send("PUT", path, query=query, body=request_body)
        return self._handle_json_response(response)

    def patch(
        self, path: str, request_body: Any, query: Optional[Mapping[str, Any]] = None
    ) -> Any:
        """Perform a PATCH request and parse the response as JSON."""
        response = self._send("PATCH", path, query=query, body=request_body)
        return self._handle_json_response(response)

    def delete(self, path: str, query: Optional[Mapping[str, Any]] = None) -> None:
        """Perform a DELETE request."""
        response = self._send("DELETE", path, query=query)
        self._handle_raw_response(response)

    # -- internals ---------------------------------------------------------

    def _send(
        self,
        method: str,
        path: str,
        query: Optional[Mapping[str, Any]] = None,
        body: Any = None,
        accept_type: str = "application/json",
    ) -> requests.Response:
        url = f"{self._base_url}/{path.lstrip('/')}"

        headers: Dict[str, str] = {
            "Accept": accept_type,
            "User-Agent": _USER_AGENT,
        }

        kwargs: Dict[str, Any] = {"params": dict(query) if query else None}

        if body:
            try:
                json_body = json.dumps(body)
            except (TypeError, ValueError) as exc:
                raise HabboApiException(
                    f"Failed to encode JSON request body: {exc}", 0, "", exc
                ) from exc
            headers["Content-Type"] = "application/json"
            kwargs["data"] = json_body.encode("utf-8")

        headers.update(self._additional_headers)
        kwargs["headers"] = headers

        try:
            return self._session.request(method, url, **kwargs)
        except requests.RequestException as exc:
            raise HabboApiException(
                f"Failed to connect to the API: {exc}", 0, None, exc
            ) from exc

    @staticmethod
    def _handle_raw_response(response: requests.Response) -> str:
        body = response.text or ""

        if response.status_code < 200 or response.status_code > 299:
            raise HabboApiException(
                f"API Request failed with status code {response.status_code}: "
                f"{response.reason}",
                response.status_code,
                body,
            )

        return body

    def _handle_json_response(self, response: requests.Response) -> Any:
        body = self._handle_raw_response(response)
        body = body if body else "{}"

        try:
            return json.loads(body)
        except json.JSONDecodeError as exc:
            raise HabboApiException(
                f"Failed to parse JSON response: {exc}", 0, body, exc
            ) from exc

    def _handle_xml_response(self, response: requests.Response) -> Dict[str, Any]:
        body = self._handle_raw_response(response)

        try:
            return XmlCleaner.clean_xml(body)
        except XmlParseError as exc:
            raise HabboApiException("Failed to parse XML response", 0, body, exc) from exc
