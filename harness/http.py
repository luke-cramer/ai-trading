from __future__ import annotations

import time
import urllib.error
import urllib.request
from dataclasses import dataclass

USER_AGENT = "ai-trading-harness/0.1 (personal research logger)"


@dataclass
class Response:
    url: str
    status: int
    body: bytes
    elapsed_s: float

    def text(self) -> str:
        return self.body.decode("utf-8", errors="replace")


def get(url: str, timeout: int = 30, retries: int = 3, backoff_s: float = 2.0, headers: dict | None = None) -> Response:
    last_err: Exception | None = None
    for attempt in range(retries):
        t0 = time.monotonic()
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*", **(headers or {})})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return Response(url, r.status, r.read(), time.monotonic() - t0)
        except urllib.error.HTTPError as e:
            last_err = e
            if 400 <= e.code < 500 and e.code != 429:
                raise
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last_err = e
        time.sleep(backoff_s * (attempt + 1))
    raise RuntimeError(f"GET {url} failed after {retries} attempts: {last_err}")
