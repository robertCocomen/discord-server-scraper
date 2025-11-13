from typing import Any, Dict, List, Optional

from utils.logger import get_logger
from utils.request_handler import RequestHandler

logger = get_logger(__name__)

class DiscordDiscoveryClient:
    """
    Minimal client for Discord's public server discovery search.

    It targets the same endpoint used by the web client. The exact
    schema may change over time, so this client is defensive and
    focused on reliability rather than strict typing.
    """

    def __init__(
        self,
        request_handler: RequestHandler,
        base_url: str = "https://discord.com/api/v9/discovery",
        user_agent: Optional[str] = None,
    ) -> None:
        self.request_handler = request_handler
        self.base_url = base_url.rstrip("/")
        self.user_agent = (
            user_agent
            or "Mozilla/5.0 (compatible; DiscordServerScraper/1.0; +https://discord.com)"
        )

    def _build_headers(self) -> Dict[str, str]:
        # Only public discovery endpoints are used; no authentication is needed.
        return {
            "User-Agent": self.user_agent,
            "Accept": "application/json",
        }

    def search_guilds(
        self,
        keyword: str,
        limit: int = 100,
        offset: int = 0,
        category_id: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Call the discovery search API and return a list of guild objects.

        Parameters
        ----------
        keyword: str
            Search term for servers.
        limit: int
            Number of results to request in this page.
        offset: int
            Offset for pagination.
        category_id: Optional[int]
            Optional category filter.

        Returns
        -------
        List[Dict[str, Any]]
        """
        params: Dict[str, Any] = {
            "term": keyword,
            "limit": max(1, min(limit, 100)),
            "offset": max(0, offset),
        }
        if category_id is not None:
            params["category_id"] = int(category_id)

        url = f"{self.base_url}/search"
        logger.debug("Requesting discovery search: %s params=%s", url, params)

        response_json = self.request_handler.get(url, params=params, headers=self._build_headers())

        guilds = response_json.get("guilds") or response_json.get("results") or []
        if not isinstance(guilds, list):
            logger.warning("Unexpected guilds payload type: %s", type(guilds))
            return []

        logger.debug("Received %d guilds from discovery search", len(guilds))
        return guilds