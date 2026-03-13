"""
MeaningCloud Sentiment Analysis CLI Wrapper (CCP L1: Perception — Intelligence Radar)
Pattern: firecrawl_wrapper.py
CCP Integration: Used by vibe-comments, tribe-soul-extraction
TODO: Output in Tshala SentimentReport format for CBCS integration

Usage:
  python sentiment_wrapper.py analyze "text to analyze" --lang en
  python sentiment_wrapper.py analyze-url "https://example.com/article" --lang en

Requires: MEANINGCLOUD_API_KEY environment variable
API: MeaningCloud Sentiment Analysis 2.1
"""

import os
import argparse
import requests
import json
import sys

MEANINGCLOUD_API_KEY = os.environ.get("MEANINGCLOUD_API_KEY")
MEANINGCLOUD_API_URL = "https://api.meaningcloud.com/sentiment-2.1"


def analyze_text(text: str, lang: str = "en"):
    """Analyze sentiment of a text string."""
    if not MEANINGCLOUD_API_KEY:
        print(json.dumps({"error": "Missing MEANINGCLOUD_API_KEY environment variable."}))
        return

    payload = {
        "key": MEANINGCLOUD_API_KEY,
        "txt": text,
        "lang": lang
    }

    try:
        response = requests.post(MEANINGCLOUD_API_URL, data=payload)
        response.raise_for_status()
        data = response.json()

        # Simplify for agent consumption
        result = {
            "input_text": text[:200] + "..." if len(text) > 200 else text,
            "language": lang,
            "status": data.get("status", {}),
            "score_tag": data.get("score_tag"),
            "agreement": data.get("agreement"),
            "subjectivity": data.get("subjectivity"),
            "confidence": data.get("confidence"),
            "irony": data.get("irony"),
            "sentence_list": [
                {
                    "text": s.get("text", "")[:100],
                    "score_tag": s.get("score_tag"),
                    "confidence": s.get("confidence")
                }
                for s in data.get("sentence_list", [])[:5]
            ]
        }
        print(json.dumps(result, indent=2))
    except requests.exceptions.RequestException as e:
        print(json.dumps({"error": f"Sentiment analysis failed: {str(e)}"}))


def analyze_url(url: str, lang: str = "en"):
    """Analyze sentiment of content at a URL."""
    if not MEANINGCLOUD_API_KEY:
        print(json.dumps({"error": "Missing MEANINGCLOUD_API_KEY environment variable."}))
        return

    payload = {
        "key": MEANINGCLOUD_API_KEY,
        "url": url,
        "lang": lang
    }

    try:
        response = requests.post(MEANINGCLOUD_API_URL, data=payload)
        response.raise_for_status()
        data = response.json()

        result = {
            "input_url": url,
            "language": lang,
            "status": data.get("status", {}),
            "score_tag": data.get("score_tag"),
            "agreement": data.get("agreement"),
            "subjectivity": data.get("subjectivity"),
            "confidence": data.get("confidence"),
            "irony": data.get("irony")
        }
        print(json.dumps(result, indent=2))
    except requests.exceptions.RequestException as e:
        print(json.dumps({"error": f"URL sentiment analysis failed: {str(e)}"}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MeaningCloud Sentiment Analysis CLI Wrapper (P0)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Analyze Text
    text_parser = subparsers.add_parser("analyze", help="Analyze sentiment of text")
    text_parser.add_argument("text", help="Text to analyze")
    text_parser.add_argument("--lang", default="en", help="Language (en, fr, es, etc.)")

    # Analyze URL
    url_parser = subparsers.add_parser("analyze-url", help="Analyze sentiment of URL content")
    url_parser.add_argument("url", help="URL to analyze")
    url_parser.add_argument("--lang", default="en", help="Language")

    args = parser.parse_args()

    if args.command == "analyze":
        analyze_text(args.text, args.lang)
    elif args.command == "analyze-url":
        analyze_url(args.url, args.lang)
