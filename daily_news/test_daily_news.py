"""
Tests for daily_news formatter and fetch helpers (no network required).
"""
import sys
import os
import unittest
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "daily_news"))

from formatter import format_article, _format_section
from fetch_news import _deduplicate, _is_recent, _entry_matches_keywords, _strip_html


SAMPLE_FINANCE = [
    {"title": "A股大涨", "summary": "上证指数上涨2%", "link": "https://example.com/1", "source": "36氪"},
    {"title": "美联储加息", "summary": "联储宣布加息25个基点", "link": "https://example.com/2", "source": "虎嗅"},
]

SAMPLE_TECH = [
    {"title": "AI大模型发布", "summary": "某公司发布新一代大模型", "link": "https://example.com/3", "source": "IT之家"},
]


class TestFormatter(unittest.TestCase):
    def test_format_article_contains_date(self):
        today = date(2026, 3, 27)
        article = format_article(SAMPLE_FINANCE, SAMPLE_TECH, today=today)
        self.assertIn("2026年03月27日", article)

    def test_format_article_contains_finance_title(self):
        article = format_article(SAMPLE_FINANCE, SAMPLE_TECH)
        self.assertIn("A股大涨", article)

    def test_format_article_contains_tech_title(self):
        article = format_article(SAMPLE_FINANCE, SAMPLE_TECH)
        self.assertIn("AI大模型发布", article)

    def test_empty_sections_show_placeholder(self):
        article = format_article([], [], today=date(2026, 1, 1))
        self.assertIn("今日暂无相关热点", article)

    def test_section_item_count(self):
        section = _format_section(SAMPLE_FINANCE)
        self.assertIn("**1.", section)
        self.assertIn("**2.", section)

    def test_long_summary_truncated(self):
        long_summary = "X" * 300
        articles = [{"title": "Test", "summary": long_summary, "link": "#", "source": "S"}]
        section = _format_section(articles)
        self.assertIn("…", section)


class TestFetchHelpers(unittest.TestCase):
    def test_deduplicate_removes_exact_duplicates(self):
        dupes = SAMPLE_FINANCE + SAMPLE_FINANCE
        result = _deduplicate(dupes)
        self.assertEqual(len(result), 2)

    def test_deduplicate_case_insensitive(self):
        arts = [
            {"title": "Hello World", "link": "a", "summary": "", "source": "S"},
            {"title": "hello world", "link": "b", "summary": "", "source": "S"},
        ]
        result = _deduplicate(arts)
        self.assertEqual(len(result), 1)

    def test_entry_matches_keywords_hit(self):
        self.assertTrue(_entry_matches_keywords("AI大模型", "", ["AI", "芯片"]))

    def test_entry_matches_keywords_miss(self):
        self.assertFalse(_entry_matches_keywords("娱乐新闻", "明星动态", ["AI", "芯片"]))

    def test_entry_matches_no_keywords_always_true(self):
        self.assertTrue(_entry_matches_keywords("任意内容", "任意摘要", []))

    def test_strip_html(self):
        html = "<p>Hello <b>World</b></p>"
        self.assertEqual(_strip_html(html), "Hello World")

    def test_is_recent_no_timestamp(self):
        # Entries without timestamps should be included
        self.assertTrue(_is_recent({}))


if __name__ == "__main__":
    unittest.main()
