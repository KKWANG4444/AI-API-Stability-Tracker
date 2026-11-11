import contextlib
import io
from pathlib import Path
import unittest
from unittest.mock import patch

from tools.verify_website_funnel import ALLOWED_ACTION_LINE, FILES, START_URL, check_documents, main


class WebsiteFunnelTests(unittest.TestCase):
    def documents(self):
        return {name: START_URL + "\n" for name in FILES}

    def test_valid_documents(self):
        self.assertEqual(check_documents(self.documents()), [])

    def test_intentional_readme_action_is_allowed(self):
        docs = self.documents()
        docs["README.md"] += ALLOWED_ACTION_LINE
        self.assertEqual(check_documents(docs), [])

    def test_missing_start_rejected_in_each_document(self):
        for name in FILES:
            with self.subTest(name=name):
                docs = self.documents()
                docs[name] = "no start link"
                self.assertTrue(check_documents(docs))

    def test_missing_file_rejected(self):
        for name in FILES:
            docs = self.documents()
            del docs[name]
            self.assertTrue(check_documents(docs))

    def test_action_not_allowed_in_geo_documents(self):
        for name in FILES[1:]:
            docs = self.documents()
            docs[name] += ALLOWED_ACTION_LINE
            self.assertTrue(check_documents(docs))

    def test_unapproved_readme_action_link_rejected(self):
        docs = self.documents()
        docs["README.md"] += ALLOWED_ACTION_LINE + "\n[Check model](https://github.com/KKWANG4444/openai-compatible-api-check)"
        self.assertTrue(check_documents(docs))

    def test_read_error_returns_nonzero(self):
        with patch.object(Path, "read_text", side_effect=OSError("unreadable")), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main([]), 1)

    def test_failed_rule_returns_nonzero(self):
        with patch.object(Path, "read_text", return_value="missing start"), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main([]), 1)
