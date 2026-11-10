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
    def fixture(self, **changes):
        return {"timestamp": "2026-01-01T00:00:00Z", "model_id": "m", "test_region": "r", "network": "n",
                "status": 200, "elapsed_ms": 100, "request_feature": "text", **changes}

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

    def test_bad_values_rejected_with_line_number(self):
        values = [[], None, 42, self.fixture(status=True), self.fixture(status=0), self.fixture(elapsed_ms=True),
                  self.fixture(elapsed_ms=-1), self.fixture(elapsed_ms=float('inf')), self.fixture(elapsed_ms=float('nan')),
                  self.fixture(elapsed_ms=10**400), self.fixture(model_id=[]), self.fixture(network=' '),
                  self.fixture(timestamp='yesterday'), self.fixture(timestamp='2026-01-01T00:00:00')]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bad.jsonl'
            for index, row in enumerate(values):
                with self.subTest(index=index):
                    path.write_text(json.dumps(row), encoding='utf-8')
                    with self.assertRaisesRegex(ValueError, 'line 1'):
                        MODULE.load_jsonl(path)
                    with self.assertRaisesRegex(ValueError, 'line 1'):
                        MODULE.summarize([row])

    def test_json_exponent_overflow_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bad.jsonl'
            path.write_text(json.dumps(self.fixture()).replace('"elapsed_ms": 100', '"elapsed_ms": 1e309'), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'elapsed_ms'):
                MODULE.load_jsonl(path)

    def test_empty_sample_rejected(self):
        with self.assertRaises(ValueError):
            MODULE.summarize([])

    def test_time_window_uses_instants_not_lexical_offsets(self):
        rows = [self.fixture(timestamp='2026-01-01T08:00:00+08:00'), self.fixture(timestamp='2026-01-01T00:00:00.100Z')]
        result = MODULE.summarize(rows)
        self.assertEqual(result['first_timestamp'], '2026-01-01T00:00:00Z')
        self.assertEqual(result['last_timestamp'], '2026-01-01T00:00:00.100000Z')
        json.dumps(result, allow_nan=False)

    def test_valid_sample_and_large_finite_values_remain_strict_json(self):
        sample = MODULE.summarize(MODULE.load_jsonl(SCRIPT.parents[1] / 'examples/availability.sample.jsonl'))
        self.assertGreater(sample['sample_count'], 0)
        json.dumps(sample, allow_nan=False)
        json.dumps(MODULE.summarize([self.fixture(elapsed_ms=1e308), self.fixture(elapsed_ms=1.7e308)]), allow_nan=False)


if __name__ == "__main__":
    unittest.main()
