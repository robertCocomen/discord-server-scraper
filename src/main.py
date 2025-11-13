import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from client.discord_api import DiscordDiscoveryClient
from client.paginator import DiscoveryPaginator
from processors.parser import parse_guilds
from processors.sanitizer import sanitize_guilds
from utils.logger import get_logger
from utils.request_handler import RequestHandler, RequestError

logger = get_logger(__name__)

def load_settings(config_path: Path) -> Dict[str, Any]:
    if not config_path.exists():
        logger.warning("Settings file %s not found. Using default settings.", config_path)
        return {
            "max_results_per_keyword": 300,
            "results_per_page": 100,
            "output_path": "data/sample.json",
            "category_id": None,
            "request": {
                "timeout": 10,
                "retries": 3,
                "backoff_factor": 0.5,
            },
        }

    try:
        with config_path.open("r", encoding="utf-8") as f:
            settings = json.load(f)
        logger.info("Loaded settings from %s", config_path)
        return settings
    except json.JSONDecodeError as exc:
        logger.error("Failed to parse settings JSON: %s", exc)
        raise SystemExit("Invalid settings JSON") from exc
    except OSError as exc:
        logger.error("Failed to read settings file: %s", exc)
        raise SystemExit("Unable to read settings file") from exc

def load_keywords(keywords_path: Path) -> List[str]:
    if not keywords_path.exists():
        logger.warning("Keywords file %s not found. Using default keyword 'discord'.", keywords_path)
        return ["discord"]

    try:
        with keywords_path.open("r", encoding="utf-8") as f:
            keywords = [line.strip() for line in f if line.strip()]
        if not keywords:
            logger.warning("Keywords file is empty. Using default keyword 'discord'.")
            return ["discord"]
        logger.info("Loaded %d keywords from %s", len(keywords), keywords_path)
        return keywords
    except OSError as exc:
        logger.error("Failed to read keywords file: %s", exc)
        return ["discord"]

def save_results(output_path: Path, results: List[Dict[str, Any]]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        logger.info("Saved %d servers to %s", len(results), output_path)
    except OSError as exc:
        logger.error("Failed to write output file %s: %s", output_path, exc)
        raise SystemExit("Unable to write output file") from exc

def run_scraper(
    keywords: List[str],
    settings: Dict[str, Any],
    root_dir: Optional[Path] = None,
) -> List[Dict[str, Any]]:
    root_dir = root_dir or Path(__file__).resolve().parents[1]

    request_cfg = settings.get("request", {})
    handler = RequestHandler(
        timeout=request_cfg.get("timeout", 10),
        retries=request_cfg.get("retries", 3),
        backoff_factor=request_cfg.get("backoff_factor", 0.5),
    )
    client = DiscordDiscoveryClient(handler)
    paginator = DiscoveryPaginator(client)

    max_results_per_keyword = int(settings.get("max_results_per_keyword", 300))
    results_per_page = int(settings.get("results_per_page", 100))
    category_id = settings.get("category_id")

    all_parsed: Dict[str, Dict[str, Any]] = {}

    for keyword in keywords:
        logger.info("Starting scrape for keyword '%s'", keyword)
        try:
            raw_guilds = paginator.paginate_search(
                keyword=keyword,
                limit_per_page=results_per_page,
                max_results=max_results_per_keyword,
                category_id=category_id,
            )
        except RequestError as exc:
            logger.error("Network error while scraping keyword '%s': %s", keyword, exc)
            continue
        except Exception as exc:  # noqa: BLE001
            logger.exception("Unexpected error while scraping keyword '%s': %s", keyword, exc)
            continue

        parsed = parse_guilds(raw_guilds)
        sanitized = sanitize_guilds(parsed)

        for guild in sanitized:
            gid = guild.get("id")
            if gid is not None:
                all_parsed[gid] = guild

        logger.info(
            "Finished keyword '%s': %d raw, %d parsed, %d unique total",
            keyword,
            len(raw_guilds),
            len(sanitized),
            len(all_parsed),
        )

    output_path = root_dir / settings.get("output_path", "data/sample.json")
    save_results(output_path, list(all_parsed.values()))
    return list(all_parsed.values())

def main() -> None:
    root_dir = Path(__file__).resolve().parents[1]
    config_path = root_dir / "src" / "config" / "settings.example.json"
    keywords_path = root_dir / "data" / "keywords.txt"

    settings = load_settings(config_path)
    keywords = load_keywords(keywords_path)

    logger.info("Discord Server Scraper starting up.")
    results = run_scraper(keywords, settings, root_dir=root_dir)
    logger.info("Scraper finished. Total unique servers collected: %d", len(results))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Scraper interrupted by user.")
        sys.exit(1)