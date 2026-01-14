import re


def normalize_number(value: str) -> float | None:
    """
    Handles:
    - 1,299.99
    - 1.299,99
    - ١٬٢٩٩٫٩٩
    - 1299
    """
    if not value:
        return None

    # Arabic numerals → Latin
    arabic_map = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
    value = value.translate(arabic_map)

    # Remove currency words/symbols
    value = re.sub(r"[^\d,.\-]", "", value)

    # European format: 1.299,99
    if value.count(",") == 1 and value.count(".") >= 1:
        if value.rfind(",") > value.rfind("."):
            value = value.replace(".", "").replace(",", ".")

    # US format: 1,299.99
    else:
        value = value.replace(",", "")

    try:
        return float(value)
    except ValueError:
        return None
