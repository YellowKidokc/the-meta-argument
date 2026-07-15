from __future__ import annotations
import argparse, json
from pathlib import Path
from .anti_gaming import run_anti_gaming
from .report import write_json_report, write_markdown_report
from .scoring import score_case

def main() -> None:
    p=argparse.ArgumentParser(description="Score a Meta-Argument case JSON file")
    p.add_argument("case_file", type=Path)
    p.add_argument("--output", type=Path)
    p.add_argument("--markdown", type=Path)
    p.add_argument("--anti-gaming", action="store_true")
    args=p.parse_args()
    try:
        case=json.loads(args.case_file.read_text(encoding="utf-8"))
        result=score_case(case)
        if args.anti_gaming and result.get("status")=="SCORED": result["anti_gaming"] = run_anti_gaming(case)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        p.error(str(exc)); return
    if args.output: write_json_report(result, args.output)
    else: print(json.dumps(result, indent=2, ensure_ascii=False))
    if args.markdown: write_markdown_report(case, result, args.markdown)
if __name__ == "__main__": main()
