"""One webhook for everything. Slack or Discord, detected by host. Unset -> stdout."""
from __future__ import annotations

import json
import os
import sys
import urllib.request

ENV = "ALERT_WEBHOOK_URL"
DISCORD_LIMIT = 1900  # Discord rejects content > 2000 chars


def _payload(url: str, text: str) -> dict:
    if "discord.com" in url or "discordapp.com" in url:
        return {"content": text[:DISCORD_LIMIT]}
    return {"text": text}


def send(text: str, level: str = "info") -> bool:
    url = os.environ.get(ENV, "").strip()
    prefix = {"info": "", "warn": ":warning: ", "error": ":rotating_light: "}[level]
    msg = prefix + text
    if not url:
        print(f"[alert:{level}] {text}", file=sys.stderr)
        return False
    body = json.dumps(_payload(url, msg)).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json", "User-Agent": "ai-trading-harness/0.1"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return 200 <= r.status < 300
