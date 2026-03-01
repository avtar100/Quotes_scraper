"""
Quotes Scraper CLI Tool
Author: Avtar Mohan Raj
Description: Scrapes quotes from quotes.toscrape.com and exports them to a CSV file.
"""

import argparse
import csv
import time
import requests
from bs4 import BeautifulSoup

BASE = "http://quotes.toscrape.com/page/{}/"


def scrape_page(page):
    """
    Scrapes a single page and returns a list of quote dictionaries.
    """
    url = BASE.format(page)
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    quotes = []

    blocks = soup.select(".quote")
    for b in blocks:
        text_elem = b.select_one(".text")
        author_elem = b.select_one(".author")
        tag_elems = b.select(".tags .tag")

        text = text_elem.get_text(strip=True) if text_elem else ""
        author = author_elem.get_text(strip=True) if author_elem else ""
        tags = ",".join(t.get_text(strip=True) for t in tag_elems)

        quotes.append({
            "text": text,
            "author": author,
            "tags": tags
        })

    return quotes


def scrape_quotes(pages=1, out="quotes.csv", delay=0.3):
    """
    Scrapes multiple pages and writes output to CSV.
    """
    rows = []

    for p in range(1, pages + 1):
        print(f"[+] Scraping page {p}")
        try:
            rows.extend(scrape_page(p))
        except requests.exceptions.RequestException as e:
            print(f"[!] Error on page {p}: {e}")
            continue

        time.sleep(delay)

    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "author", "tags"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"[+] Saved {len(rows)} quotes to {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scrape quotes from quotes.toscrape.com and save to CSV."
    )

    parser.add_argument(
        "--pages",
        type=int,
        default=2,
        help="Number of pages to scrape (default: 2)"
    )

    parser.add_argument(
        "--out",
        default="quotes.csv",
        help="Output CSV file name (default: quotes.csv)"
    )

    args = parser.parse_args()

    scrape_quotes(pages=args.pages, out=args.out)
