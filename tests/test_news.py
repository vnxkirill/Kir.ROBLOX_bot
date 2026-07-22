"""Тесты новостного модуля: парсинг RSS и форматирование."""

import pytest

from app.core.exceptions import ExternalServiceError
from app.modules.news.api import RobloxNewsClient
from app.modules.news.handlers import _format
from app.schemas.news import NewsItem

_SAMPLE_RSS = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
  <item>
    <title>Weekly Recap: Animation Graphs Go Live</title>
    <link>https://devforum.roblox.com/t/weekly-recap/123</link>
    <pubDate>Mon, 21 Jul 2026 10:00:00 +0000</pubDate>
  </item>
  <item>
    <title>Changes to Private Server Limits</title>
    <link>https://devforum.roblox.com/t/changes/456</link>
  </item>
</channel></rss>"""


def test_parse_valid_rss() -> None:
    items = RobloxNewsClient._parse(_SAMPLE_RSS)
    assert len(items) == 2
    assert items[0].title == "Weekly Recap: Animation Graphs Go Live"
    assert items[0].url.endswith("/123")


def test_parse_skips_incomplete_items() -> None:
    rss = "<rss><channel><item><title>No link</title></item></channel></rss>"
    assert RobloxNewsClient._parse(rss) == []


def test_parse_malformed_raises() -> None:
    with pytest.raises(ExternalServiceError):
        RobloxNewsClient._parse("<rss><broken>")


def test_format_escapes_and_links() -> None:
    items = [NewsItem(title="Update <b> & more", url="https://x.test/1")]
    text = _format(items)
    assert "https://x.test/1" in text
    assert "&lt;b&gt;" in text  # HTML экранирован
    assert "&amp;" in text
