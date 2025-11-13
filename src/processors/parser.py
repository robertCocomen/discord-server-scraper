from typing import Any, Dict, Iterable, List

from utils.logger import get_logger

logger = get_logger(__name__)

_FIELDS = [
    "id",
    "name",
    "description",
    "icon",
    "splash",
    "banner",
    "approximate_presence_count",
    "approximate_member_count",
    "premium_subscription_count",
    "preferred_locale",
    "auto_removed",
    "discovery_splash",
    "primary_category_id",
    "vanity_url_code",
    "is_published",
    "keywords",
    "features",
    "categories",
    "primary_category",
    "objectID",
]

def parse_guild(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracts the fields defined in the README from a raw guild object.

    Unknown fields are ignored. Missing fields are simply omitted;
    sanitization happens later.
    """
    parsed: Dict[str, Any] = {}

    for field in _FIELDS:
        if field in raw:
            parsed[field] = raw[field]

    # Map potential alternative ID fields that sometimes appear in discovery
    if "id" not in parsed:
        for candidate in ("guild_id", "objectID"):
            if candidate in raw:
                parsed["id"] = raw[candidate]
                break

    # Some responses place keywords/tags under "keywords" or "discovery_keywords"
    if "keywords" not in parsed:
        if "discovery_keywords" in raw:
            parsed["keywords"] = raw.get("discovery_keywords")

    # objectID is often just the guild ID; ensure it's set if possible
    if "objectID" not in parsed and "id" in parsed:
        parsed["objectID"] = parsed["id"]

    logger.debug("Parsed guild with id=%s", parsed.get("id"))
    return parsed

def parse_guilds(raw_guilds: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Parse a collection of raw guild objects.
    """
    parsed_list = [parse_guild(g) for g in raw_guilds if isinstance(g, dict)]
    logger.info("Parsed %d guilds from raw data", len(parsed_list))
    return parsed_list

_FIELDS = _FIELDS  # expose for tests