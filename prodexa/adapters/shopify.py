import json
import re
from bs4 import BeautifulSoup

from prodexa.adapters.base import BaseAdapter
from prodexa.fetchers.http import HTTPFetcher
from prodexa.parsers.json_ld import extract_product_json_ld
from prodexa.normalizers.price import normalize_price


class ShopifyAdapter(BaseAdapter):
    site = ".myshopify.com"

    def __init__(self):
        self.fetcher = HTTPFetcher()

    # -------------------------
    # Fetch
    # -------------------------
    def fetch(self, url: str) -> str:
        return self.fetcher.fetch(url)

    # -------------------------
    # Extract
    # -------------------------
    def extract(self, html: str) -> dict:
        soup = BeautifulSoup(html, "lxml")

        # 1️⃣ Shopify Analytics object (most reliable)
        shopify_data = self._extract_shopify_meta(soup)
        if shopify_data:
            return shopify_data

        # 2️⃣ JSON-LD fallback
        json_ld = extract_product_json_ld(soup)
        if json_ld:
            return json_ld

        # 3️⃣ Last resort: HTML heuristics
        return self._extract_from_html(soup)

    # -------------------------
    # Normalize
    # -------------------------
    def normalize(self, data: dict) -> dict:
        raw_price = (
            data.get("price")
            or data.get("price_min")
            or data.get("offers", {}).get("price")
        )

        price, currency = normalize_price(str(raw_price))

        images = data.get("images") or []
        if isinstance(images, str):
            images = [images]

        return {
            "title": data.get("name") or data.get("title"),
            "brand": self._extract_brand(data),
            "price": price,
            "currency": currency,
            "availability": self._extract_availability(data),
            "rating": data.get("aggregateRating", {}).get("ratingValue"),
            "reviews_count": data.get("aggregateRating", {}).get("reviewCount"),
            "images": images,
            "description": data.get("description"),
            "features": [],
            "sku": self._extract_sku(data),
        }

    # ==================================================
    # Shopify-specific helpers
    # ==================================================

    def _extract_shopify_meta(self, soup):
        """
        Extracts:
        ShopifyAnalytics.meta.product
        """
        scripts = soup.find_all("script")
        for script in scripts:
            if not script.string:
                continue

            if "ShopifyAnalytics.meta.product" in script.string:
                try:
                    match = re.search(
                        r"ShopifyAnalytics\.meta\.product\s*=\s*(\{.*?\});",
                        script.string,
                        re.DOTALL,
                    )
                    if match:
                        return json.loads(match.group(1))
                except Exception:
                    continue
        return None

    def _extract_from_html(self, soup):
        title = soup.select_one("h1")
        price = soup.select_one('[class*="price"]')

        images = [
            img["src"]
            for img in soup.select("img")
            if img.get("src") and "cdn.shopify.com" in img.get("src")
        ]

        return {
            "title": title.get_text(strip=True) if title else None,
            "price": price.get_text(strip=True) if price else None,
            "images": images,
        }

    def _extract_brand(self, data):
        vendor = data.get("vendor")
        if vendor:
            return vendor
        brand = data.get("brand")
        if isinstance(brand, dict):
            return brand.get("name")
        return brand

    def _extract_availability(self, data):
        available = data.get("available")
        if available is True:
            return "in_stock"
        if available is False:
            return "out_of_stock"

        offers = data.get("offers", {})
        availability = offers.get("availability", "")
        if "InStock" in availability:
            return "in_stock"
        if "OutOfStock" in availability:
            return "out_of_stock"
        return None

    def _extract_sku(self, data):
        variants = data.get("variants")
        if isinstance(variants, list) and variants:
            return variants[0].get("sku")
        return data.get("sku")
