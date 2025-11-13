from typing import Any, Dict, Iterable, List, Optional

from utils.logger import get_logger

logger = get_logger(__name__)

def _coerce_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def _coerce_bool(value: Any) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "1"}:
            return True
        if lowered in {"false", "no", "0"}:
            return False
    return None

def _coerce_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    try:
        s = str(value)
        return s.strip()
    except Exception:  # noqa: BLE001
        return None

def _coerce_list(value: Any) -> Optional[List[Any]]:
    if value is None:
        return None
    if isinstance(value, list):
        return value
    if isinstance(value, (set, tuple)):
        return list(value)
    return None

def sanitize_guild(guild: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure types are consistent and drop obviously invalid data.
    """
    sanitized: Dict[str, Any] = {}

    sanitized["id"] = _coerce_str(guild.get("id"))
    sanitized["name"] = _coerce_str(guild.get("name"))
    sanitized["description"] = _coerce_str(guild.get("description"))
    sanitized["icon"] = _coerce_str(guild.get("icon"))
    sanitized["splash"] = _coerce_str(guild.get("splash"))
    sanitized["banner"] = _coerce_str(guild.get("banner"))
    sanitized["approximate_presence_count"] = _coerce_int(
        guild.get("approximate_presence_count")
    )
    sanitized["approximate_member_count"] = _coerce_int(
        guild.get("approximate_member_count")
    )
    sanitized["premium_subscription_count"] = _coerce_int(
        guild.get("premium_subscription_count")
    )
    sanitized["preferred_locale"] = _coerce_str(guild.get("preferred_locale"))
    sanitized["auto_removed"] = _coerce_bool(guild.get("auto_removed"))
    sanitized["discovery_splash"] = _coerce_str(guild.get("discovery_splash"))
    sanitized["primary_category_id"] = _coerce_int(guild.get("primary_category_id"))
    sanitized["vanity_url_code"] = _coerce_str(guild.get("vanity_url_code"))
    sanitized["is_published"] = _coerce_bool(guild.get("is_published"))
    sanitized["keywords"] = _coerce_list(guild.get("keywords"))
    sanitized["features"] = _coerce_list(guild.get("features"))
    sanitized["categories"] = _coerce_list(guild.get("categories"))
    sanitized["primary_category"] = guild.get("primary_category")
    sanitized["objectID"] = _coerce_str(guild.get("objectID"))

    # Drop keys with None values for a cleaner JSON output
    cleaned = {k: v for k, v in sanitized.items() if v is not None}

    logger.debug("Sanitized guild id=%s", cleaned.get("id"))
    return cleaned

def sanitize_guilds(guilds: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    sanitized_list = [sanitize_guild(g) for g in guilds]
    logger.info("Sanitized %d guilds", len(sanitized_list))
    return sanitized_list