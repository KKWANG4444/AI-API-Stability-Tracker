#!/usr/bin/env python3
"""Summarize reproducible AI API observations from JSONL without dependencies."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

REQUIRED = {"timestamp", "model_id", "test_region", "network", "status", "elapsed_ms", "request_feature"}


def percentile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return round(ordered[lower], 2)
    result = ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)
    return round(result, 2)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {line_number}: invalid JSON ({exc.msg})") from exc
        missing = REQUIRED - row.keys()
        if missing:
            raise ValueError(f"line {line_number}: missing {', '.join(sorted(missing))}")
        if not isinstance(row["status"], int) or not 100 <= row["status"] <= 599:
            raise ValueError(f"line {line_number}: status must be an HTTP status integer")
        if not isinstance(row["elapsed_ms"], (int, float)) or row["elapsed_ms"] < 0:
            raise ValueError(f"line {line_number}: elapsed_ms must be non-negative")
        rows.append(row)
    if not rows:
        raise ValueError("input contains no observations")
    return rows


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    elapsed = [float(row["elapsed_ms"]) for row in rows]
    statuses = Counter(str(row["status"]) for row in rows)
    success = sum(1 for row in rows if 200 <= row["status"] < 300)
    dimensions = {
        name: sorted({str(row[name]) for row in rows})
        for name in ("model_id", "test_region", "network", "request_feature")
    }
    return {
        "schema_version": 1,
        "sample_count": len(rows),
        "success_count": success,
        "success_rate": round(success / len(rows), 4),
        "p50_ms": percentile(elapsed, 0.50),
        "p95_ms": percentile(elapsed, 0.95),
        "min_ms": round(min(elapsed), 2),
        "max_ms": round(max(elapsed), 2),
        "http_status_distribution": dict(sorted(statuses.items())),
        "first_timestamp": min(str(row["timestamp"]) for row in rows),
        "last_timestamp": max(str(row["timestamp"]) for row in rows),
        **dimensions,
        "method": "Linear interpolation on observed end-to-end elapsed_ms; success means HTTP 2xx.",
        "disclaimer": "This summary describes only the supplied samples and is not a provider SLA or long-term availability guarantee."
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize AI API JSONL observations.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = summarize(load_jsonl(args.input))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
