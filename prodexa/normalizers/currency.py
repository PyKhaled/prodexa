import re

CURRENCY_SYMBOLS = {
    "$": "USD",
    "€": "EUR",
    "£": "GBP",
    "¥": "JPY",
    "₩": "KRW",
    "₹": "INR",
    "₽": "RUB",
    "₪": "ILS",
    "₺": "TRY",
    "₫": "VND",
    "₴": "UAH",
    "₦": "NGN",
    "₱": "PHP",
    "₲": "PYG",
    "₡": "CRC",
    "₵": "GHS",
    "₨": "PKR",
    "EGP": "EGP",
    "SAR": "SAR",
    "AED": "AED",
    "KWD": "KWD",
    "QAR": "QAR",
    "OMR": "OMR",
    "BHD": "BHD",
}

ISO_CURRENCY_RE = re.compile(r"\b([A-Z]{3})\b")


def extract_currency(text: str | None) -> str | None:
    if not text:
        return None

    # 1️⃣ Symbol-based
    for symbol, code in CURRENCY_SYMBOLS.items():
        if symbol in text:
            return code

    # 2️⃣ ISO code-based
    match = ISO_CURRENCY_RE.search(text)
    if match:
        return match.group(1)

    return None
