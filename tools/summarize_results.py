#!/usr/bin/env python3
"""Summarize reproducible AI API observations from JSONL without dependencies."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REQUIRED = {"timestamp", "model_id", "test_region", "network", "status", "elapsed_ms", "request_feature"}


def validate_row(row: Any, line_number: int) -> dict[str, Any]:
    prefix = f"line {line_number}: "
    if not isinstance(row, dict):
        raise ValueError(prefix + "每条记录必须是 JSON 对象")
    missing = REQUIRED - row.keys()
    if missing:
        raise ValueError(prefix + f"missing {', '.join(sorted(missing))}")
    if type(row["status"]) is not int or not 100 <= row["status"] <= 599:
        raise ValueError(prefix + "status must be an HTTP status integer")
    elapsed = row["elapsed_ms"]
    try:
        valid_elapsed = type(elapsed) in (int, float) and math.isfinite(elapsed) and elapsed >= 0
    except OverflowError:
        valid_elapsed = False
    if not valid_elapsed:
        raise ValueError(prefix + "elapsed_ms 必须是有限、非负、非布尔数值")
    for name in ("timestamp", "model_id", "test_region", "network", "request_feature"):
        value = row[name]
        if not isinstance(value, str) or not value.strip() or any(ord(char) < 32 for char in value):
            raise ValueError(prefix + f"{name} 必须是非空文本且不含控制字符")
    try:
        stamp = datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00"))
        if "T" not in row["timestamp"] or stamp.utcoffset() is None:
            raise ValueError
        normalized = stamp.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    except (ValueError, OverflowError):
        raise ValueError(prefix + "timestamp 必须是带时区的 ISO 8601 时间") from None
    return {**row, "timestamp": normalized}


def reject_constant(value: str):
    raise ValueError("JSON 不允许 NaN 或 Infinity")


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
            row = json.loads(line, parse_constant=reject_constant)
        except ValueError as exc:
            raise ValueError(f"line {line_number}: invalid JSON ({exc})") from exc
        rows.append(validate_row(row, line_number))
    if not rows:
        raise ValueError("input contains no observations")
    return rows


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        raise ValueError("input contains no observations")
    rows = [validate_row(row, number) for number, row in enumerate(rows, 1)]
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
        "first_timestamp": min(rows, key=lambda row: datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00")))["timestamp"],
        "last_timestamp": max(rows, key=lambda row: datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00")))["timestamp"],
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
        rendered = json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
