from prodexa.engine.pipeline import extract_product


def test_pipeline_smoke(monkeypatch):
    def fake_fetch(self, url):
        return "<html><title>Test</title></html>"

    monkeypatch.setattr(
        "prodexa.adapters.generic.GenericAdapter.fetch",
        fake_fetch,
    )

    product = extract_product(
        "https://example.com/product",
        soft=True,          # 👈 important
        cache=None,         # 👈 isolate test from cache
    )

    assert "url" in product
