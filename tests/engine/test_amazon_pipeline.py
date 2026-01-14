from pathlib import Path

from prodexa.engine.pipeline import extract_product


FIXTURE = Path(__file__).parent.parent / "fixtures" / "amazon_product.html"


def test_amazon_random_product_soft(monkeypatch):
    html = FIXTURE.read_text(encoding="utf-8")

    # Mock AmazonAdapter.fetch
    def fake_fetch(self, url):
        return html

    monkeypatch.setattr(
        "prodexa.adapters.amazon.AmazonAdapter.fetch",
        fake_fetch,
    )

    product = extract_product(
        "https://www.amazon.com/dp/B09B8V1LZ3",
        soft=True,
        cache=None,
    )

    assert product["url"].startswith("https://www.amazon.com")
    assert product.get("title") in (
        "Echo Dot (5th Gen)",
        "Amazon.com: Echo Dot (5th Gen)",
    )
    assert product.get("currency") == "USD"
    assert product.get("_meta") is not None
