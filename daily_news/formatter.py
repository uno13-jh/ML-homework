"""
formatter.py - Format fetched news into a WeChat 公众号 article (Markdown).
"""
from datetime import date
from typing import List, Dict


# WeChat public account article template (Markdown-friendly)
ARTICLE_TEMPLATE = """\
# 📰 今日财经科技热点 · {date}

> 每日精选金融与科技领域的重要动态，助你快速掌握行业脉搏。

---

## 💰 金融热点

{finance_section}

---

## 🖥️ 科技热点

{tech_section}

---

*本文由每日热点速递 Bot 自动整理，数据来源于36氪、虎嗅、IT之家等媒体，仅供参考。*
"""

ITEM_TEMPLATE = """\
**{index}. {title}**
> {summary}
🔗 [阅读原文]({link})（来源：{source}）
"""

EMPTY_SECTION = "_今日暂无相关热点，请稍后再试。_\n"


def _format_section(articles: List[Dict[str, str]]) -> str:
    """Format a list of article dicts into a Markdown section."""
    if not articles:
        return EMPTY_SECTION
    lines = []
    for idx, art in enumerate(articles, start=1):
        title = art.get("title", "（无标题）")
        summary = art.get("summary", "").strip()
        link = art.get("link", "#")
        source = art.get("source", "未知来源")
        # Fall back to title if no summary
        if not summary:
            summary = title
        lines.append(
            ITEM_TEMPLATE.format(
                index=idx,
                title=title,
                summary=summary[:180] + ("…" if len(summary) > 180 else ""),
                link=link,
                source=source,
            )
        )
    return "\n".join(lines)


def format_article(
    finance_articles: List[Dict[str, str]],
    tech_articles: List[Dict[str, str]],
    today: date | None = None,
) -> str:
    """Render the full WeChat article as Markdown."""
    if today is None:
        today = date.today()
    date_str = today.strftime("%Y年%m月%d日")
    finance_section = _format_section(finance_articles)
    tech_section = _format_section(tech_articles)
    return ARTICLE_TEMPLATE.format(
        date=date_str,
        finance_section=finance_section,
        tech_section=tech_section,
    )
