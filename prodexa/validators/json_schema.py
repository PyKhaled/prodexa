import json
from jsonschema import validate
from pathlib import Path

SCHEMA_PATH = Path(__file__).parents[1] / "schemas" / "product.v1.json"

with open(SCHEMA_PATH) as f:
    PRODUCT_SCHEMA = json.load(f)


def validate_product(product: dict):
    validate(instance=product, schema=PRODUCT_SCHEMA)