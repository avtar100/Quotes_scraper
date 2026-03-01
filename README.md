# Quotes Scraper — Python Web Scraping Project

A simple and efficient Python script that scrapes quotes, authors, and tags from **QuotesToScrape.com** — a free site designed specifically for practicing web scraping.  
This scraper supports pagination, structured CSV export, and safe execution in both terminal and Jupyter Notebook environments.

---

## 📌 Features

- Scrapes quotes, authors, and tags
- Supports multiple pages (`--pages` argument)
- Saves output to CSV
- Proxy-free (no blocks)
- Built using `requests` + `BeautifulSoup4`
- Jupyter-safe argument parsing (`parse_known_args`)
- Lightweight and easy to customize

---

## 🛠️ Technologies Used

- Python 3
- requests  
- beautifulsoup4

## Installation

pip install -r requirements.txt

## Usage

python quotes_scraper.py --pages 3 --output quotes.csv
- csv  
- argparse  

---


