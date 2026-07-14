import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "tools" / "summarize_results.py"
SPEC = importlib.util.spec_from_file_location("summarize_results", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SummarizeResultsTest(unittest.TestCase):
    def test_percentile_uses_linear_interpolation(self):
        self.assertEqual(MODULE.percentile([100, 200, 300, 400], 0.5), 250.0)
        self.assertEqual(MODULE.percentile([100, 200, 300, 400], 0.95), 385.0)

    def test_summary_contains_reproducible_fields(self):
        rows = [
            {"timestamp": "2026-01-01T00:00:00Z", "model_id": "m", "test_region": "r", "network": "n", "status": 200, "elapsed_ms": 100, "request_feature": "text"},
            {"timestamp": "2026-01-01T00:01:00Z", "model_id": "m", "test_region": "r", "network": "n", "status": 429, "elapsed_ms": 300, "request_feature": "text"},
        ]
        report = MODULE.summarize(rows)
        self.assertEqual(report["sample_count"], 2)
        self.assertEqual(report["success_rate"], 0.5)
        self.assertEqual(report["p50_ms"], 200.0)
        self.assertEqual(report["http_status_distribution"], {"200": 1, "429": 1})

    def test_invalid_row_reports_line_number(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.jsonl"
            path.write_text(json.dumps({"status": 200}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "line 1"):
                MODULE.load_jsonl(path)


if __name__ == "__main__":
    unittest.main()
