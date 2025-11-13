import time
from typing import Any, Dict, Optional

import requests

from .logger import get_logger

logger = get_logger(__name__)

class RequestError(RuntimeError):
    """Raised when an HTTP request fails after retries."""

class RequestHandler:
    """
    Thin wrapper around requests.Session providing retry and logging.
    """

    def __init__(
        self,
        timeout: float = 10.0,
        retries: int = 3,
        backoff_factor: float = 0.5,
    ) -> None:
        self.timeout = timeout
        self.retries = max(0, retries)
        self.backoff_factor = max(0.0, backoff_factor)
        self.session = requests.Session()

    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        attempt = 0
        last_exc: Optional[Exception] = None

        while attempt <= self.retries:
            attempt += 1
            try:
                logger.debug(
                    "HTTP GET %s attempt=%d params=%s headers=%s",
                    url,
                    attempt,
                    params,
                    headers,
                )
                response = self.session.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=self.timeout,
                )
                if 200 <= response.status_code < 300:
                    logger.debug(
                        "HTTP %s %s succeeded status=%d",
                        "GET",
                        response.url,
                        response.status_code,
                    )
                    try:
                        return response.json()
                    except ValueError as exc:
                        logger.error("Failed to decode JSON response: %s", exc)
                        raise RequestError("Invalid JSON response") from exc

                logger.warning(
                    "HTTP GET %s failed status=%d body=%s",
                    response.url,
                    response.status_code,
                    response.text[:200],
                )
                last_exc = RequestError(
                    f"Unexpected status code: {response.status_code}"
                )
            except (requests.Timeout, requests.ConnectionError) as exc:
                logger.warning("Request to %s failed: %s", url, exc)
                last_exc = exc

            if attempt <= self.retries:
                sleep_time = self.backoff_factor * (2 ** (attempt - 1))
                logger.debug("Retrying in %.2f seconds", sleep_time)
                time.sleep(sleep_time)

        logger.error("All retries failed for URL %s", url)
        if isinstance(last_exc, RequestError):
            raise last_exc
        raise RequestError(str(last_exc) if last_exc else "Request failed")