import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from processors.parser import parse_guild, parse_guilds  # noqa: E402
from processors.sanitizer import sanitize_guild, sanitize_guilds  # noqa: E402

def load_sample() -> dict:
    data_path = ROOT / "data" / "sample.json"
    with data_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    # sample.json is an array with one object
    return data[0]

def test_parse_guild_extracts_expected_fields():
    raw = load_sample()
    parsed = parse_guild(raw)

    assert parsed["id"] == raw["id"]
    assert parsed["name"] == raw["name"]
    assert parsed["approximate_member_count"] == raw["approximate_member_count"]
    assert parsed["keywords"] == raw["keywords"]
    assert parsed["objectID"] == raw["objectID"]

def test_parse_guilds_handles_iterable():
    raw = [load_sample(), load_sample()]
    parsed_list = parse_guilds(raw)
    assert len(parsed_list) == 2
    assert all("id" in g for g in parsed_list)

def test_sanitize_guild_normalizes_types():
    raw = load_sample()
    # introduce some type noise
    raw["approximate_member_count"] = str(raw["approximate_member_count"])
    raw["auto_removed"] = "false"
    raw["primary_category_id"] = str(raw["primary_category_id"])

    sanitized = sanitize_guild(raw)

    assert isinstance(sanitized["approximate_member_count"], int)
    assert sanitized["auto_removed"] is False
    assert isinstance(sanitized["primary_category_id"], int)

def test_sanitize_guilds_drops_null_fields():
    raw = load_sample()
    raw["description"] = None
    sanitized_list = sanitize_guilds([raw])
    sanitized = sanitized_list[0]
    assert "description" not in sanitized

@pytest.mark.parametrize("bad_value", ["abc", [], {}])
def test_int_coercion_failure_drops_field(bad_value):
    raw = load_sample()
    raw["approximate_member_count"] = bad_value
    sanitized = sanitize_guild(raw)
    assert "approximate_member_count" not in sanitized