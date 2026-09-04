from __future__ import annotations

from datetime import datetime, timezone

UTC = timezone.utc


def now() -> datetime:
    return datetime.now(UTC)


def iso(dt: datetime) -> str:
    """Canonical UTC timestamp: 2026-09-04T09:00:00Z."""
    return dt.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


def hour_bucket(dt: datetime) -> str:
    return iso(dt.replace(minute=0, second=0, microsecond=0))


def stamp(dt: datetime) -> str:
    """Filesystem-safe timestamp for raw log filenames."""
    return dt.astimezone(UTC).strftime("%Y%m%dT%H%M%SZ")
