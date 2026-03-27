"""
fetch_news.py - Fetches daily hot topics from finance and technology RSS feeds.
"""
import feedparser
import requests
import logging
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
from sources import FINANCE_SOURCES, TECH_SOURCES

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

MAX_ITEMS_PER_SOURCE = 10
MAX_ITEMS_PER_CATEGORY = 8
# Only include articles published within the last 24 hours
HOURS_THRESHOLD = 24

REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; DailyNewsBot/1.0; "
        "+https://github.com/uno13-jh/ML-homework)"
    )
}


def _is_recent(entry: Any) -> bool:
    """Return True if the RSS entry was published within HOURS_THRESHOLD hours."""
    published = entry.get("published_parsed") or entry.get("updated_parsed")
    if not published:
        return True  # include if no timestamp
    cutoff = datetime.now(timezone.utc) - timedelta(hours=HOURS_THRESHOLD)
    pub_dt = datetime(*published[:6], tzinfo=timezone.utc)
    return pub_dt >= cutoff


def _entry_matches_keywords(title: str, summary: str, keywords: List[str]) -> bool:
    """Return True if any keyword is found in title or summary."""
    if not keywords:
        return True
    text = (title + " " + summary).lower()
    return any(kw.lower() in text for kw in keywords)


def fetch_rss(source: Dict[str, Any]) -> List[Dict[str, str]]:
    """Parse an RSS feed and return a list of article dicts."""
    url = source["url"]
    keywords = source.get("keywords", [])
    name = source["name"]
    results = []
    try:
        feed = feedparser.parse(url, request_headers=REQUEST_HEADERS)
        if feed.bozo and not feed.entries:
            logger.warning("Failed to parse RSS from %s: %s", name, feed.bozo_exception)
            return results
        for entry in feed.entries[:MAX_ITEMS_PER_SOURCE]:
            if not _is_recent(entry):
                continue
            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()
            summary = entry.get("summary", entry.get("description", "")).strip()
            # Strip HTML tags from summary
            summary = _strip_html(summary)[:200]
            if title and _entry_matches_keywords(title, summary, keywords):
                results.append(
                    {
                        "title": title,
                        "link": link,
                        "summary": summary,
                        "source": name,
                    }
                )
    except Exception as exc:
        logger.warning("Error fetching %s: %s", name, exc)
    return results


def _strip_html(text: str) -> str:
    """Remove HTML tags from a string."""
    import re
    clean = re.compile(r"<[^>]+>")
    return clean.sub("", text)


def _deduplicate(articles: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Remove articles with duplicate titles."""
    seen = set()
    unique = []
    for art in articles:
        key = art["title"].lower()
        if key not in seen:
            seen.add(key)
            unique.append(art)
    return unique


def fetch_finance_news() -> List[Dict[str, str]]:
    """Fetch finance hot topics from configured sources."""
    all_items: List[Dict[str, str]] = []
    for source in FINANCE_SOURCES:
        if source.get("type") == "rss":
            all_items.extend(fetch_rss(source))
        # json/other types can be added here
    all_items = _deduplicate(all_items)
    return all_items[:MAX_ITEMS_PER_CATEGORY]


def fetch_tech_news() -> List[Dict[str, str]]:
    """Fetch technology hot topics from configured sources."""
    all_items: List[Dict[str, str]] = []
    for source in TECH_SOURCES:
        if source.get("type") == "rss":
            all_items.extend(fetch_rss(source))
    all_items = _deduplicate(all_items)
    return all_items[:MAX_ITEMS_PER_CATEGORY]
