import logging
import os
from typing import Optional

_LOGGER_CONFIGURED = False

def _configure_root_logger(level: Optional[str] = None) -> None:
    global _LOGGER_CONFIGURED
    if _LOGGER_CONFIGURED:
        return

    log_level_name = level or os.getenv("DISCORD_SCRAPER_LOG_LEVEL", "INFO")
    numeric_level = getattr(logging, log_level_name.upper(), logging.INFO)

    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    _LOGGER_CONFIGURED = True

def get_logger(name: str) -> logging.Logger:
    _configure_root_logger()
    return logging.getLogger(name)