import logging
import time
from typing import Dict, Any

from prodexa.registry import resolve_adapter
from prodexa.validators.json_schema import validate_product
from prodexa.errors import ExtractionError
from prodexa.cache.base import CacheBackend
from prodexa.cache.memory import MemoryCache
from prodexa.utils import make_cache_key

logger = logging.getLogger(__name__)

DEFAULT_CACHE_TTL = 300
_cache = MemoryCache()


def _extract_without_cache(url: str, soft: bool) -> Dict[str, Any]:
    """
    Core extraction logic without caching.
    """

    if not url or not isinstance(url, str):
        raise ExtractionError("A valid product URL is required")

    logger.info("Starting extraction for URL: %s", url)
    adapter = resolve_adapter(url)
    logger.debug("Resolved adapter: %s", adapter.__class__.__name__)

    start_time = time.perf_counter()

    # ---------------- Fetch ----------------
    try:
        html = adapter.fetch(url)
    except Exception as exc:
        logger.exception("Fetch failed for URL: %s", url)
        raise ExtractionError(f"Failed to fetch URL: {url}") from exc

    # ---------------- Extract ----------------
    try:
        raw_data = adapter.extract(html)
    except Exception as exc:
        logger.exception("Extraction failed")
        if not soft:
            raise ExtractionError("Extraction failed") from exc
        raw_data = {}

    # ---------------- Normalize ----------------
    try:
        product = adapter.normalize(raw_data)
    except Exception as exc:
        logger.exception("Normalization failed")
        if not soft:
            raise ExtractionError("Normalization failed") from exc
        product = {}

    product["url"] = url

    # ---------------- Validate ----------------
    warnings: list[str] = []

    try:
        validate_product(product)
    except Exception as exc:
        if not soft:
            logger.exception("Schema validation failed")
            raise
        warning = f"Schema validation failed: {exc}"
        logger.warning(warning)
        warnings.append(warning)

    if soft:
        product["_meta"] = {
            "adapter": adapter.__class__.__name__,
            "warnings": warnings,
            "duration_ms": round(
                (time.perf_counter() - start_time) * 1000, 2
            ),
        }

    logger.info(
        "Extraction completed (soft=%s)", soft
    )

    return product


def extract_product(
    url: str,
    *,
    soft: bool = False,
    cache: CacheBackend | None = _cache,
    cache_ttl: int = DEFAULT_CACHE_TTL,
) -> Dict[str, Any]:
    """
    Extract a product with optional caching.
    """

    cache_key = make_cache_key(url, soft)

    # ---------------- Cache HIT ----------------
    if cache:
        cached = cache.get(cache_key)
        if cached:
            logger.info("Cache hit for URL: %s", url)
            return cached

    logger.info("Cache miss for URL: %s", url)

    # ---------------- Extract ----------------
    product = _extract_without_cache(url, soft)

    # ---------------- Cache SET ----------------
    if cache:
        cache.set(cache_key, product, ttl=cache_ttl)

    return product
