import os
import sys
import time
import argparse
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

# Define file extensions you want to catch
TARGET_EXTENSIONS = ['.pdf', '.docx', '.xlsx', '.zip', '.jpg', '.jpeg', '.png']

def is_valid_internal_url(url, base_domain):
    """Ensure the link stays within the target website and isn't an external jump."""
    parsed = urlparse(url)
    return parsed.netloc == base_domain

def crawl_site(start_url, max_pages=100):
    parsed_start = urlparse(start_url)
    base_domain = parsed_start.netloc
    
    # Trackers to avoid infinite loops
    pages_to_visit = [start_url]
    visited_pages = set()
    found_files = set()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0"
    }

    print(f"\n[+] Starting deep crawl on: {start_url}")
    print(f"[+] Target extensions: {', '.join(TARGET_EXTENSIONS)}")
    print("-" * 60)

    page_count = 0
    while pages_to_visit and page_count < max_pages:
        current_url = pages_to_visit.pop(0)

        if current_url in visited_pages:
            continue

        print(f"[{page_count + 1}/{max_pages}] Crawling: {current_url}")
        visited_pages.add(current_url)
        page_count += 1

        try:
            # Short politeness delay so the server doesn't block you
            time.sleep(0.5) 
            response = requests.get(current_url, headers=headers, timeout=10)
            
            # Skip if the page isn't actual HTML text (e.g. accidentally hitting a massive media file)
            if "text/html" not in response.headers.get("Content-Type", ""):
                continue
                
        except Exception:
            continue # Skip broken links seamlessly

        soup = BeautifulSoup(response.text, "html.parser")
        
        for link in soup.find_all("a"):
            href = link.get("href")
            if not href:
                continue

            # Standardize relative paths to absolute URLs
            absolute_url = urljoin(current_url, href)
            parsed_url = urlparse(absolute_url)
            file_ext = os.path.splitext(parsed_url.path)[1].lower()

            # Case A: It's a downloadable target file
            if file_ext in TARGET_EXTENSIONS:
                if absolute_url not in found_files:
                    found_files.add(absolute_url)
                    print(f"  📄 Found File ({file_ext.upper()}): {absolute_url}")
            
            # Case B: It's another web page inside the same website
            elif is_valid_internal_url(absolute_url, base_domain):
                # Clean URL components (remove #fragments)
                clean_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
                if clean_url not in visited_pages and clean_url not in pages_to_visit:
                    pages_to_visit.append(clean_url)

    print("-" * 60)
    print(f"[+] Crawl Finished. Scanned {page_count} pages.")
    print(f"[+] Total unique downloadable files discovered: {len(found_files)}")
    
    # Save results to a text file so you don't lose them in the Termux terminal scroll
    if found_files:
        with open("discovered_links.txt", "w") as f:
            for item in sorted(found_files):
                f.write(f"{item}\n")
        print("[+] All links saved cleanly to 'discovered_links.txt'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Whole-Site Recursive File Scraper")
    parser.add_argument("url", help="Target root URL")
    parser.add_argument("--max", type=int, default=50, help="Max web pages to deep-crawl (default 50)")
    args = parser.parse_args()

    target = args.url if args.url.startswith(("http://", "https://")) else "https://" + args.url
    crawl_site(target, max_pages=args.max)
