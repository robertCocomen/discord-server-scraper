import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from client.discord_api import DiscordDiscoveryClient  # noqa: E402
from client.paginator import DiscoveryPaginator  # noqa: E402

class DummyHandler:
    def __init__(self, pages: List[Dict[str, Any]]) -> None:
        self.pages = pages
        self.calls = 0

    def get(self, url: str, params=None, headers=None) -> Dict[str, Any]:
        if self.calls >= len(self.pages):
            return {"guilds": []}
        page = self.pages[self.calls]
        self.calls += 1
        return page

def test_discord_client_uses_guilds_key():
    handler = DummyHandler(
        pages=[{"guilds": [{"id": "1"}, {"id": "2"}]}],
    )
    client = DiscordDiscoveryClient(handler, base_url="https://example.com/api")
    guilds = client.search_guilds("test", limit=2, offset=0)
    assert len(guilds) == 2
    assert guilds[0]["id"] == "1"

def test_discovery_paginator_stops_on_empty_page():
    handler = DummyHandler(
        pages=[
            {"guilds": [{"id": "1"}, {"id": "2"}]},
            {"guilds": []},
        ]
    )
    client = DiscordDiscoveryClient(handler, base_url="https://example.com/api")
    paginator = DiscoveryPaginator(client)

    results = paginator.paginate_search("test", limit_per_page=2, max_results=10)
    assert len(results) == 2
    assert {g["id"] for g in results} == {"1", "2"}

def test_discovery_paginator_respects_max_results():
    handler = DummyHandler(
        pages=[
            {"guilds": [{"id": str(i)} for i in range(5)]},
            {"guilds": [{"id": str(i)} for i in range(5, 10)]},
        ]
    )
    client = DiscordDiscoveryClient(handler, base_url="https://example.com/api")
    paginator = DiscoveryPaginator(client)

    results = paginator.paginate_search("test", limit_per_page=5, max_results=7)
    assert len(results) == 7
    assert results[0]["id"] == "0"
    assert results[-1]["id"] == "6"