"""Append-only CSV tables partitioned by month, deduped on key columns. Git-friendly, survives restarts."""
from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd

DATA_ROOT = Path("data")


class Table:
    def __init__(self, strategy: str, name: str, columns: list[str], key: list[str], root: Path = DATA_ROOT,
                 partition: str = "month"):
        assert all(k in columns for k in key)
        assert partition in ("month", "year")
        assert columns[0].endswith("_time") or columns[0] in ("date",), "first column must be the UTC timestamp/date used for partitioning"
        self.dir = root / strategy / name
        self.columns = columns
        self.key = key
        self.partition = partition

    def _partition(self, ts: str) -> Path:
        return self.dir / f"{ts[:7] if self.partition == 'month' else ts[:4]}.csv"

    def _read_partition(self, p: Path) -> list[dict]:
        if not p.exists():
            return []
        with p.open(newline="") as f:
            return list(csv.DictReader(f))

    def append(self, rows: list[dict]) -> int:
        """Insert rows whose key is not already present. Returns number inserted."""
        inserted = 0
        by_part: dict[Path, list[dict]] = {}
        for r in rows:
            by_part.setdefault(self._partition(str(r[self.columns[0]])), []).append(r)
        for p, new_rows in by_part.items():
            raw = self._read_partition(p)
            existing, seen = [], set()
            for r in raw:  # union merges can leave duplicate keys; keep the first
                k = tuple(str(r[c]) for c in self.key)
                if k not in seen:
                    seen.add(k)
                    existing.append(r)
            out = []
            for r in new_rows:
                k = tuple(str(r[c]) for c in self.key)
                if k in seen:
                    continue
                seen.add(k)
                out.append({c: ("" if r.get(c) is None else r.get(c)) for c in self.columns})
            if not out and len(existing) == len(raw):
                continue
            p.parent.mkdir(parents=True, exist_ok=True)
            merged = sorted(existing + out, key=lambda r: tuple(str(r[k]) for k in self.key))
            with p.open("w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=self.columns)
                w.writeheader()
                w.writerows(merged)
            inserted += len(out)
        return inserted

    def replace(self, rows: list[dict]) -> int:
        """Rewrite the whole table from rows (for derived tables that are recomputed, not appended)."""
        if self.dir.exists():
            for p in self.dir.glob("*.csv"):
                p.unlink()
        return self.append(rows)

    def compact(self) -> int:
        """Rewrite every partition deduped and sorted (after a union merge). Returns rows dropped."""
        dropped = 0
        for p in (sorted(self.dir.glob("*.csv")) if self.dir.exists() else []):
            raw = self._read_partition(p)
            seen, keep = set(), []
            for r in raw:
                k = tuple(str(r[c]) for c in self.key)
                if k not in seen:
                    seen.add(k)
                    keep.append(r)
            if len(keep) != len(raw):
                keep.sort(key=lambda r: tuple(str(r[k]) for k in self.key))
                with p.open("w", newline="") as f:
                    w = csv.DictWriter(f, fieldnames=self.columns)
                    w.writeheader()
                    w.writerows(keep)
                dropped += len(raw) - len(keep)
        return dropped

    def read(self) -> pd.DataFrame:
        files = sorted(self.dir.glob("*.csv")) if self.dir.exists() else []
        if not files:
            return pd.DataFrame(columns=self.columns)
        df = pd.concat([pd.read_csv(f, dtype=str, keep_default_na=False) for f in files], ignore_index=True)
        return df.drop_duplicates(subset=self.key).sort_values(self.key).reset_index(drop=True)
