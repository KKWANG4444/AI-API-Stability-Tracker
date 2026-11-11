"""Fail-closed checks for the website-first documentation entry points."""
import argparse
from pathlib import Path
import sys

FILES = ("README.md", "llms.txt", "llms-full.txt")
START_URL = "https://docs.aifast.hk/start/"
ACTION_TOKEN = "openai-compatible-api-check"
# This existing related-resource link is intentional, not a model-check CTA.
ALLOWED_ACTION_LINE = "- [OpenAI-compatible API 持续验收 Action](https://github.com/KKWANG4444/openai-compatible-api-check)"


def check_documents(documents):
    errors = []
    for name in FILES:
        if name not in documents:
            errors.append(f"{name}: missing required document")
            continue
        text = documents[name]
        if START_URL not in text:
            errors.append(f"{name}: missing website start entry")
        for number, line in enumerate(text.splitlines(), 1):
            if ACTION_TOKEN not in line:
                continue
            if name == "README.md" and line.strip() == ALLOWED_ACTION_LINE:
                continue
            errors.append(f"{name}:{number}: unexpected Action entry; keep model-check traffic on the website")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    try:
        documents = {name: (args.root / name).read_text(encoding="utf-8") for name in FILES}
    except (OSError, UnicodeError) as exc:
        print(f"Website funnel verification failed: {exc}", file=sys.stderr)
        return 1
    errors = check_documents(documents)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Website funnel verification passed; intentional README Action resource preserved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
