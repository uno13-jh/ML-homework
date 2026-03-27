"""
main.py - Entry point for the daily finance & tech hot-topics digest.

Usage:
    python main.py              # writes output/YYYY-MM-DD.md and prints to stdout
    python main.py --stdout     # prints to stdout only
"""
import argparse
import sys
import os
import logging
from datetime import date

# Ensure sibling modules are importable when run directly
sys.path.insert(0, os.path.dirname(__file__))

from fetch_news import fetch_finance_news, fetch_tech_news
from formatter import format_article

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate daily finance & tech hot-topics digest for WeChat 公众号."
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print the article to stdout only (do not write a file).",
    )
    args = parser.parse_args()

    today = date.today()
    logger.info("Fetching finance news…")
    finance_articles = fetch_finance_news()
    logger.info("Got %d finance articles.", len(finance_articles))

    logger.info("Fetching tech news…")
    tech_articles = fetch_tech_news()
    logger.info("Got %d tech articles.", len(tech_articles))

    article = format_article(finance_articles, tech_articles, today)

    if args.stdout:
        print(article)
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, f"{today.isoformat()}.md")
    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write(article)
    logger.info("Article written to %s", output_path)
    print(article)


if __name__ == "__main__":
    main()
