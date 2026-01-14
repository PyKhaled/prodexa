from prodexa.adapters.generic import GenericAdapter
from prodexa.adapters.shopify import ShopifyAdapter
from prodexa.adapters.amazon import AmazonAdapter
ADAPTERS = [
    ShopifyAdapter,
    AmazonAdapter,
]


def resolve_adapter(url: str):
    for adapter_cls in ADAPTERS:
        if adapter_cls.matches(url):
            return adapter_cls()
    return GenericAdapter()
