import random
import time
import requests
from typing import List


class HTTPFetcher:
    DEFAULT_TIMEOUT = 15
    MAX_RETRIES = 3
    BACKOFF_FACTOR = 1.5

    USER_AGENTS: List[str] = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/121.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/119.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    ]

    def fetch(self, url: str) -> str:
        last_exception = None

        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                headers = {
                    "User-Agent": random.choice(self.USER_AGENTS),
                    "Accept-Language": "en-US,en;q=0.9",
                }

                response = requests.get(
                    url,
                    headers=headers,
                    timeout=self.DEFAULT_TIMEOUT,
                )

                response.raise_for_status()
                return response.text

            except Exception as exc:
                last_exception = exc
                if attempt < self.MAX_RETRIES:
                    sleep_time = self.BACKOFF_FACTOR ** attempt
                    time.sleep(sleep_time)
                else:
                    break

        raise RuntimeError(
            f"Failed to fetch URL after {self.MAX_RETRIES} attempts"
        ) from last_exception