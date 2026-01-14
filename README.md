# Prodexa

A **production-grade, serverless-ready Python package** that extracts structured
product data from ecommerce product pages (Shopify, Amazon, and generic stores)
and returns a **validated JSON product model**.

Designed to work as:
- Python library
- CLI tool
- `python -m` executable
- Serverless function (Lambda, containers)
- Internal enrichment service

## ✨ Features

- ✅ Adapter-based architecture (Shopify, Amazon, Generic)
- ✅ Schema-validated product model (JSON Schema)
- ✅ Soft & strict extraction modes
- ✅ International price & currency normalization
- ✅ Retry, timeout & User-Agent rotation
- ✅ In-memory caching with TTL
- ✅ Friendly CLI (no stack traces)
- ✅ Logging control (`--verbose`, `--quiet`)
- ✅ Serverless & automation friendly

## 📦 Product Model

The extractor outputs a normalized product object:

```json
{
  "url": "https://example.com/product",
  "title": "Product Name",
  "brand": "Brand",
  "price": 1299.99,
  "currency": "USD",
  "availability": "in_stock",
  "rating": 4.6,
  "reviews_count": 231,
  "images": ["https://..."],
  "description": "...",
  "features": [],
  "sku": "SKU-123"
}
```

Schema location:

prodexa/schemas/product.v1.json


## 🧠 How It Works

URL
 → Adapter resolution
 → Fetch (retry + backoff + UA rotation)
 → Extract (JSON-LD / HTML)
 → Normalize (price, currency, locale)
 → Validate (JSON Schema)
 → Product JSON


## 🚀 Installation
```
Editable install (recommended for development)

pip install -e .

Regular install (from PyPI)

pip install product-extractor
```

## ▶️ Usage

1️⃣ CLI

```
product-extract <product_url> [options]
```

Common examples
```
# Strict mode (default)
product-extract https://shop.com/product

# Soft mode (best-effort)
product-extract https://example.com --soft

# Disable cache
product-extract <url> --nocache

# Custom cache TTL (seconds)
product-extract <url> --ttl 600

# Debug logging
product-extract <url> --soft --verbose

# Errors only
product-extract <url> --quiet

# Version
product-extract --version
```

2️⃣ python -m

```
python -m prodexa https://example.com --soft
```

3️⃣ As a Python Library
```
from prodexa import extract_product

product = extract_product(
    "https://shop.com/product",
    soft=True
)
```

With cache control:
```
from prodexa.cache.memory import MemoryCache

product = extract_product(
    url,
    soft=True,
    cache=MemoryCache(),
    cache_ttl=300
)
```

## 🧩 Soft vs Strict Mode

Strict mode (default)
	•	Enforces full schema
	•	Fails on missing required fields (e.g. price)
	•	Best for production pipelines

product-extract <url>

Soft mode
	•	Returns partial data
	•	Adds _meta.warnings
	•	Best for discovery & crawling

product-extract <url> --soft

Example soft output:
```
{
  "title": "Example Domain",
  "url": "https://example.com",
  "_meta": {
    "adapter": "GenericAdapter",
    "warnings": [
      "Schema validation failed: 'price' is a required property"
    ],
    "duration_ms": 184.22
  }
}
```

## 🗃 Caching
	•	✅ Enabled by default
	•	✅ In-memory cache with TTL
	•	✅ Cache key = URL + mode (soft/strict)

Cache options

Flag	Effect
(default)	Cache enabled
--cache	Explicit enable
--no-cache	Disable cache
--nocache	Disable cache (alias)
--ttl N	Cache TTL in seconds


📊 Logging Levels

Flag	Level
(default)	INFO
--verbose	DEBUG
--quiet	ERROR

Library logging is caller-controlled and safe for APIs & Lambda.

## 🧪 Exit Codes

Code	Meaning
0	Success
1	CLI usage error
2	Extraction / validation failure
3	Unexpected error


## ⚠️ Limitations (Intentional)
	•	❌ CAPTCHA solving
	•	❌ Login-required pages
	•	❌ Heavy JS rendering by default
	•	❌ Variant matrices (sizes/colors)

These belong to advanced / paid layers.

## 🛣 Roadmap
	•	Batch extraction (URLs file / list)
	•	Redis cache backend
	•	Rate limiting
	•	HTTP API wrapper
	•	TestPyPI / PyPI release

## 📜 License

MIT

### 👤 Maintainer

Built as a reusable extraction engine, not a one-off scraper.
Contributions welcome.
