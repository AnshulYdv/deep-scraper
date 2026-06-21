# Deep Scraper 🕷️

An asynchronous Python web scraper built to crawl websites recursively, map site structures, and extract page data up to a specified depth. 

It handles concurrency using `asyncio` and `aiohttp`, keeps track of visited links to prevent loops, and extracts structured content like titles, metadata, and internal/external links.

## Key Features

* **Asynchronous Execution:** Built with `aiohttp` to handle multiple concurrent requests rather than waiting on pages sequentially.
* **Controlled Depth:** Crawls recursively starting from a seed URL down to a user-defined depth limit.
* **Duplicate Prevention:** Tracks visited URLs in memory to avoid redundant network requests.
* **Rate Limiting:** Includes built-in delays and automatically checks `robots.txt` to respect target server limits.
* **Structured Output:** Extracts page titles, meta descriptions, and discovered links directly into a JSON file.

---

## Setup & Installation

### 1. Environment Setup
Clone the repository and set up a Python virtual environment (Python 3.9+ recommended):

```bash
git clone https://github.com/AnshulYdv/deep-scraper.git
cd deep-scraper

python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate