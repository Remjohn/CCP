"""
Firecrawl CLI Wrapper (CCP L1: Perception)
Pattern: firecrawl_wrapper.py
CCP Integration: Used by intelligence-radar, smart-query-generator
TODO: Add rate limiting (max 10 req/min) and response caching (TTL=1h)
"""
import os
import argparse
import requests
import json
import sys
from dotenv import load_dotenv

# Auto-load .env from project root
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

FIRECRAWL_API_KEY = os.environ.get("FIRECRAWL_API_KEY")
FIRECRAWL_API_URL = "https://api.firecrawl.dev/v0"

def firecrawl_search(query: str, limit: int = 5, scrape_results: bool = True):
    if not FIRECRAWL_API_KEY:
        print(json.dumps({"error": "Missing FIRECRAWL_API_KEY environment variable."}))
        return

    endpoint = f"{FIRECRAWL_API_URL}/search"
    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": query,
        "limit": limit,
        "scrapeOptions": {
            "formats": ["markdown"]
        } if scrape_results else {}
    }

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(json.dumps({"error": f"Firecrawl Search failed: {str(e)}"}))

def firecrawl_scrape(url: str):
    if not FIRECRAWL_API_KEY:
        print(json.dumps({"error": "Missing FIRECRAWL_API_KEY environment variable."}))
        return

    endpoint = f"{FIRECRAWL_API_URL}/scrape"
    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "url": url,
        "formats": ["markdown"]
    }

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(json.dumps({"error": f"Firecrawl Scrape failed: {str(e)}"}))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Firecrawl CLI Wrapper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Search Command
    search_parser = subparsers.add_parser("search", help="Search the web")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--limit", type=int, default=5, help="Number of results")
    search_parser.add_argument("--no-scrape", action="store_true", help="Disable scraping details")

    # Scrape Command
    scrape_parser = subparsers.add_parser("scrape", help="Scrape a URL")
    scrape_parser.add_argument("url", help="URL to scrape")

    args = parser.parse_args()

    if args.command == "search":
        firecrawl_search(args.query, args.limit, not args.no_scrape)
    elif args.command == "scrape":
        firecrawl_scrape(args.url)
