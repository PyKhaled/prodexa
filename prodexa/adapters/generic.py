import re
from bs4 import BeautifulSoup

from prodexa.adapters.base import BaseAdapter
from prodexa.fetchers.http import HTTPFetcher
from prodexa.parsers.json_ld import extract_product_json_ld
from prodexa.normalizers.price import normalize_price


class GenericAdapter(BaseAdapter):
    site = "*"

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/121.0 Safari/537.36"
        )
    }

    COMMON_PRICE_SELECTORS = [
        '[itemprop="price"]',
        '[class*="price"]',
        '[id*="price"]',
        '[data-price]',
    ]

    def __init__(self):
        self.fetcher = HTTPFetcher()


    def fetch(self, url: str) -> str:
        return self.fetcher.fetch(url)


    def extract(self, html: str) -> dict:
        soup = BeautifulSoup(html, "lxml")

        # 1️⃣ JSON-LD (best case)
        json_ld = extract_product_json_ld(soup)
        if json_ld:
            return json_ld

        # 2️⃣ Meta + heuristics
        data = {}

        og_title = soup.find("meta", property="og:title")
        meta_desc = soup.find("meta", attrs={"name": "description"})
        og_image = soup.find("meta", property="og:image")

        data["title"] = og_title["content"] if og_title else self._fallback_title(soup)
        data["description"] = meta_desc["content"] if meta_desc else None
        data["image"] = [og_image["content"]] if og_image else []

        price_text = self._find_price_text(soup)
        data["price"] = price_text

        return data

    def normalize(self, data: dict) -> dict:
        raw_price = (data.get("price") or data.get("offers", {}).get("price"))

        price, currency = normalize_price(raw_price)

        return {
            "title": data.get("name") or data.get("title"),
            "brand": self._extract_brand(data),
            "price": price,
            "currency": currency,
            "availability": self._extract_availability(data),
            "rating": self._extract_rating(data),
            "reviews_count": self._extract_reviews_count(data),
            "images": self._normalize_images(data),
            "description": data.get("description"),
            "features": [],
            "sku": data.get("sku"),
        }

    # -------------------------
    # Helpers
    # -------------------------

    def _fallback_title(self, soup):
        if soup.title:
            return soup.title.get_text(strip=True)
        return None

    def _find_price_text(self, soup):
        for selector in self.COMMON_PRICE_SELECTORS:
            el = soup.select_one(selector)
            if el:
                return el.get_text(strip=True)
        return None

    def _parse_price(self, price_raw):
        if not price_raw:
            return None, None

        match = re.search(r"([A-Z]{3}|[$€£]|EGP)?\s*([\d,.]+)", price_raw)
        if not match:
            return None, None

        currency_raw, amount = match.groups()
        price = float(amount.replace(",", ""))

        currency = self._normalize_currency(currency_raw)
        return price, currency

    def _normalize_currency(self, raw):
        if not raw:
            return None

        mapping = {
            "$": "USD",
            "€": "EUR",
            "£": "GBP",
            "EGP": "EGP",
        }
        return mapping.get(raw, raw)

    def _normalize_images(self, data):
        images = data.get("image") or data.get("images")
        if isinstance(images, str):
            return [images]
        return images or []

    def _extract_brand(self, data):
        brand = data.get("brand")
        if isinstance(brand, dict):
            return brand.get("name")
        return brand

    def _extract_rating(self, data):
        rating = data.get("aggregateRating", {}).get("ratingValue")
        if rating:
            return float(rating)
        return None

    def _extract_reviews_count(self, data):
        count = data.get("aggregateRating", {}).get("reviewCount")
        if count:
            return int(count)
        return None

    def _extract_availability(self, data):
        offers = data.get("offers", {})
        availability = offers.get("availability", "")
        if "InStock" in availability:
            return "in_stock"
        if "OutOfStock" in availability:
            return "out_of_stock"
        return None
