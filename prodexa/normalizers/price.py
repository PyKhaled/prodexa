from prodexa.normalizers.currency import extract_currency
from prodexa.normalizers.locale import normalize_number


def normalize_price(raw_price: str | None) -> tuple[float | None, str | None]:
    """
    Returns: (price, currency)
    """
    if not raw_price:
        return None, None

    currency = extract_currency(raw_price)
    amount = normalize_number(raw_price)

    return amount, currency
