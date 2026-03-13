"""
Google Trends CLI Wrapper (CCP L1: Perception — Intelligence Radar)
Pattern: firecrawl_wrapper.py
CCP Integration: Used by intelligence-radar for velocity context
TODO: Add RTTR (Real-Time Trend Relevance) scoring output

Usage:
  python google_trends_wrapper.py interest "keyword1,keyword2" --timeframe "today 3-m"
  python google_trends_wrapper.py related "keyword" --limit 10
  python google_trends_wrapper.py trending --geo "FR"

Requires: RAPIDAPI_KEY environment variable
API: Google Trends via RapidAPI (serpapi or similar)
"""

import os
import argparse
import requests
import json
import sys

RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
RAPIDAPI_HOST = "google-trends8.p.rapidapi.com"


def check_interest(keywords: str, timeframe: str = "today 3-m", geo: str = ""):
    """Check interest over time for given keywords."""
    if not RAPIDAPI_KEY:
        print(json.dumps({"error": "Missing RAPIDAPI_KEY environment variable."}))
        return

    url = f"https://{RAPIDAPI_HOST}/interestOverTime"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    params = {
        "keyword": keywords,
        "timeframe": timeframe,
        "geo": geo or "",
        "dataType": "TIMESERIES"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        # Simplify output for agent consumption
        result = {
            "keywords": keywords.split(","),
            "timeframe": timeframe,
            "geo": geo or "global",
            "interest_data": data
        }
        print(json.dumps(result, indent=2))
    except requests.exceptions.RequestException as e:
        print(json.dumps({"error": f"Google Trends interest check failed: {str(e)}"}))


def get_related(keyword: str, limit: int = 10):
    """Get related queries and topics for a keyword."""
    if not RAPIDAPI_KEY:
        print(json.dumps({"error": "Missing RAPIDAPI_KEY environment variable."}))
        return

    url = f"https://{RAPIDAPI_HOST}/relatedQueries"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    params = {
        "keyword": keyword,
        "dataType": "QUERY"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        result = {
            "keyword": keyword,
            "related_queries": data
        }
        print(json.dumps(result, indent=2))
    except requests.exceptions.RequestException as e:
        print(json.dumps({"error": f"Google Trends related queries failed: {str(e)}"}))


def get_trending(geo: str = "US"):
    """Get trending searches for a region."""
    if not RAPIDAPI_KEY:
        print(json.dumps({"error": "Missing RAPIDAPI_KEY environment variable."}))
        return

    url = f"https://{RAPIDAPI_HOST}/trendingSearches"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    params = {"geo": geo}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        result = {
            "geo": geo,
            "trending": data
        }
        print(json.dumps(result, indent=2))
    except requests.exceptions.RequestException as e:
        print(json.dumps({"error": f"Google Trends trending failed: {str(e)}"}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Trends CLI Wrapper (P0)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Interest Over Time
    interest_parser = subparsers.add_parser("interest", help="Check interest over time")
    interest_parser.add_argument("keywords", help="Comma-separated keywords")
    interest_parser.add_argument("--timeframe", default="today 3-m", help="Time range")
    interest_parser.add_argument("--geo", default="", help="Country code (e.g., US, FR)")

    # Related Queries
    related_parser = subparsers.add_parser("related", help="Get related queries")
    related_parser.add_argument("keyword", help="Keyword to find related queries for")
    related_parser.add_argument("--limit", type=int, default=10, help="Max results")

    # Trending Searches
    trending_parser = subparsers.add_parser("trending", help="Get trending searches")
    trending_parser.add_argument("--geo", default="US", help="Country code")

    args = parser.parse_args()

    if args.command == "interest":
        check_interest(args.keywords, args.timeframe, args.geo)
    elif args.command == "related":
        get_related(args.keyword, args.limit)
    elif args.command == "trending":
        get_trending(args.geo)
