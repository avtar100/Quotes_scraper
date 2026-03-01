
import argparse
import csv
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "http://quotes.toscrape.com/page/{}/"

def scrape_page(page):
    url = BASE.format(page)
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    quotes = []
    blocks = soup.select(".quote")
    for b in blocks:
        text = b.select_one(".text").get_text(strip=True) if b.select_one(".text") else ""
        author = b.select_one(".author").get_text(strip=True) if b.select_one(".author") else ""
        tag_elems = b.select(".tags .tag")
        tags = ",".join(t.get_text(strip=True) for t in tag_elems)
        quotes.append({"text": text, "author": author, "tags": tags})
    return quotes

def scrape_quotes(pages=1, out="quotes.csv", delay=0.3):
    rows = []
    for p in range(1, pages+1):
        print(f"[+] Scraping page {p}")
        rows.extend(scrape_page(p))
        time.sleep(delay)
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text","author","tags"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"[+] Saved {len(rows)} quotes to {out}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", type=int, default=2)
    parser.add_argument("--out", default="quotes.csv")

    args, unknown = parser.parse_known_args()
    scrape_quotes(pages=args.pages, out=args.out)


