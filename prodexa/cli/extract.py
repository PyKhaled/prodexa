import sys
import json
import logging
from jsonschema import ValidationError
from prodexa.engine.pipeline import extract_product
from prodexa.errors import ExtractionError
from prodexa.cache.memory import MemoryCache
from prodexa.__version__ import __version__


DEFAULT_CACHE_TTL = 300  # seconds


def configure_logging(verbose: bool, quiet: bool) -> None:
    if quiet:
        level = logging.ERROR
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def main() -> None:
    args = sys.argv[1:]

    # ---------------- Version ----------------
    if "--version" in args:
        print(f"product-extractor {__version__}")
        sys.exit(0)

    if not args:
        print(
            "Usage:\n"
            "  product-extract <product_url> [options]\n\n"
            "Options:\n"
            "  --soft              Return partial product instead of failing\n"
            "  --cache             Enable cache (default)\n"
            "  --no-cache          Disable cache\n"
            "  --nocache           Disable cache (alias)\n"
            "  --ttl <seconds>     Cache TTL (default: 300)\n"
            "  --verbose           Debug logging\n"
            "  --quiet             Errors only\n"
            "  --version           Show version\n"
        )
        sys.exit(1)

    # ---------------- Flags ----------------
    soft = "--soft" in args
    verbose = "--verbose" in args
    quiet = "--quiet" in args

    configure_logging(verbose=verbose, quiet=quiet)

    # Cache flags
    nocache = "--no-cache" in args or "--nocache" in args
    cache_enabled = not nocache

    ttl = DEFAULT_CACHE_TTL
    if "--ttl" in args:
        try:
            ttl = int(args[args.index("--ttl") + 1])
        except Exception:
            print("❌ --ttl requires an integer value")
            sys.exit(1)

    cache = MemoryCache() if cache_enabled else None

    # ---------------- URL ----------------
    url = next((a for a in args if not a.startswith("-")), None)
    if not url:
        print("❌ Product URL is required")
        sys.exit(1)

    # ---------------- Execute ----------------
    try:
        product = extract_product(
            url,
            soft=soft,
            cache=cache,
            cache_ttl=ttl,
        )
        print(json.dumps(product, indent=2, ensure_ascii=False))
        sys.exit(0)

    except ValidationError as e:
        print("❌ Extraction failed: invalid product data\n")
        print("Reason:")
        print(f"  - {e.message}\n")

        if not soft:
            print("Hint:")
            print("  This page may not be a product page.")
            print("  Try running with --soft to get partial results:\n")
            print(f"    product-extract {url} --soft")

        sys.exit(2)

    except ExtractionError as e:
        print(f"❌ Extraction failed:\n  {e}")
        sys.exit(2)

    except Exception as e:
        print("❌ Unexpected error occurred")
        if verbose:
            raise
        print(str(e))
        sys.exit(3)