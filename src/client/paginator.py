from typing import Any, Dict, List, Optional

from utils.logger import get_logger

logger = get_logger(__name__)

class DiscoveryPaginator:
    """
    Responsible for walking through paginated discovery search results.
    """

    def __init__(self, client: "DiscordDiscoveryClient") -> None:  # type: ignore[name-defined]
        self.client = client

    def paginate_search(
        self,
        keyword: str,
        limit_per_page: int = 100,
        max_results: int = 3000,
        category_id: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetch multiple pages of search results.

        Stops when:
        - Reaching max_results, or
        - The API returns fewer results than requested (last page), or
        - A page returns no results.
        """
        limit_per_page = max(1, min(limit_per_page, 100))
        max_results = max(1, max_results)

        results: List[Dict[str, Any]] = []
        offset = 0

        while len(results) < max_results:
            logger.info(
                "Fetching page (keyword=%s, offset=%d, limit=%d, category_id=%s)",
                keyword,
                offset,
                limit_per_page,
                category_id,
            )
            page = self.client.search_guilds(
                keyword=keyword,
                limit=limit_per_page,
                offset=offset,
                category_id=category_id,
            )

            if not page:
                logger.info("No more results returned; stopping pagination.")
                break

            results.extend(page)
            logger.debug("Accumulated %d results so far", len(results))

            if len(page) < limit_per_page:
                logger.info("Last page detected (page_size=%d); stopping.", len(page))
                break

            offset += limit_per_page
            if offset >= max_results:
                logger.info("Reached max_results limit (%d); stopping.", max_results)
                break

        return results[:max_results]