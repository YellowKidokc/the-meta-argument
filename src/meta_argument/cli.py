from __future__ import annotations

import argparse
import json
from pathlib import Path

from .scoring import score_case


def main() -> None:
    parser = argparse.ArgumentParser(description="Score a Meta-Argument case JSON file")
    parser.add_argument("case_file", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        case = json.loads(args.case_file.read_text(encoding="utf-8"))
        result = score_case(case)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
        return

    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
