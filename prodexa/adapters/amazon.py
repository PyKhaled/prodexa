import json
import re
import requests
from bs4 import BeautifulSoup

from prodexa.adapters.base import BaseAdapter
from prodexa.fetchers.http import HTTPFetcher
from prodexa.parsers.json_ld import extract_product_json_ld


class AmazonAdapter(BaseAdapter):
    site = "amazon."

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/121.0 Safari/537.36"
        )
    }

    def __init__(self):
        self.fetcher = HTTPFetcher()

    def fetch(self, url: str) -> str:
        return self.fetcher.fetch(url)

    def extract(self, html: str) -> dict:
        soup = BeautifulSoup(html, "lxml")

        json_ld = extract_product_json_ld(soup)
        if json_ld:
            return json_ld

        title = soup.select_one("#productTitle")
        price = soup.select_one(".a-price .a-offscreen")

        return {
            "title": title.get_text(strip=True) if title else None,
            "price": price.get_text(strip=True) if price else None,
        }

    def normalize(self, data: dict) -> dict:
        price, currency = None, None

        if isinstance(data.get("price"), str):
            match = re.search(r"([\d,.]+)", data["price"])
            if match:
                price = float(match.group(1).replace(",", ""))
                currency = "USD"

        return {
            "title": data.get("name") or data.get("title"),
            "brand": data.get("brand", {}).get("name")
            if isinstance(data.get("brand"), dict)
            else data.get("brand"),
            "price": price or data.get("offers", {}).get("price"),
            "currency": currency or data.get("offers", {}).get("priceCurrency"),
            "rating": data.get("aggregateRating", {}).get("ratingValue"),
            "reviews_count": data.get("aggregateRating", {}).get("reviewCount"),
            "images": data.get("image", []),
            "description": data.get("description"),
            "features": [],
            "availability": "in_stock"
            if "In Stock" in json.dumps(data)
            else None,
            "sku": data.get("sku")
        }
