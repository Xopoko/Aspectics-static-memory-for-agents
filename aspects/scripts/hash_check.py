#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate ASPECTS.json source hashes and emit a report.",
    )
    parser.add_argument(
        "aspects_path",
        type=Path,
        help="Path to ASPECTS.json (or compatible) file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory to store the generated report (defaults to aspects/scripts/reports).",
    )
    parser.add_argument(
        "--report-prefix",
        default="hash_check",
        help="Filename prefix for the generated report (default: hash_check).",
    )
    return parser.parse_args()


def load_aspects(aspects_path: Path) -> Dict[str, Any]:
    try:
        content = aspects_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"error: ASPECTS file not found at {aspects_path}", file=sys.stderr)
        sys.exit(1)
    except OSError as exc:
        print(f"error: unable to read {aspects_path}: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON in {aspects_path}: {exc}", file=sys.stderr)
        sys.exit(1)


def compute_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(131072), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_report(data: Dict[str, Any], root_dir: Path) -> Dict[str, Any]:
    verified = 0
    missing: List[Dict[str, Any]] = []
    mismatches: List[Dict[str, Any]] = []

    for section in data.get("sections", []):
        for entry in section.get("entries", []):
            entry_id = entry.get("id")
            section_id = entry.get("sectionId")
            slug = entry.get("slug")

            for source in entry.get("sources", []):
                rel_path = Path(source.get("path", ""))
                expected = source.get("sha256")

                if not rel_path or not expected:
                    continue

                source_path = root_dir / rel_path
                if not source_path.exists():
                    missing.append(
                        {
                            "entryId": entry_id,
                            "sectionId": section_id,
                            "slug": slug,
                            "path": str(rel_path),
                        }
                    )
                    continue

                try:
                    actual = compute_hash(source_path)
                except OSError as exc:
                    missing.append(
                        {
                            "entryId": entry_id,
                            "sectionId": section_id,
                            "slug": slug,
                            "path": str(rel_path),
                            "error": str(exc),
                        }
                    )
                    continue

                if actual != expected:
                    mismatches.append(
                        {
                            "entryId": entry_id,
                            "sectionId": section_id,
                            "slug": slug,
                            "path": str(rel_path),
                            "expected": expected,
                            "actual": actual,
                        }
                    )
                else:
                    verified += 1

    total_sources = verified + len(missing) + len(mismatches)
    now = dt.datetime.now().astimezone()

    return {
        "generatedAt": now.isoformat(timespec="seconds"),
        "summary": {
            "totalSources": total_sources,
            "verified": verified,
            "missing": len(missing),
            "mismatches": len(mismatches),
        },
        "missingSources": missing,
        "hashMismatches": mismatches,
    }


def ensure_output_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def resolve_output_dir(args: argparse.Namespace) -> Path:
    if args.output_dir:
        return ensure_output_dir(args.output_dir)

    default_dir = Path(__file__).resolve().parent / "reports"
    return ensure_output_dir(default_dir)


def next_report_path(output_dir: Path, prefix: str) -> Path:
    date_part = dt.date.today().isoformat()
    candidate = output_dir / f"{prefix}_{date_part}.json"
    counter = 1

    while candidate.exists():
        candidate = output_dir / f"{prefix}_{date_part}_{counter:02}.json"
        counter += 1

    return candidate


def write_report(report: Dict[str, Any], path: Path) -> None:
    path.write_text(json.dumps(report, indent=2, ensure_ascii=True))


def main() -> None:
    args = parse_args()
    aspects_path = args.aspects_path.resolve()
    report_root = aspects_path.parent

    data = load_aspects(aspects_path)
    report = build_report(data, report_root)

    output_dir = resolve_output_dir(args)
    report_path = next_report_path(output_dir, args.report_prefix)

    write_report(report, report_path)

    summary = report["summary"]
    print(
        "Report written:",
        report_path,
        "\nSummary:",
        f"total={summary['totalSources']},",
        f"verified={summary['verified']},",
        f"missing={summary['missing']},",
        f"mismatches={summary['mismatches']}",
    )


if __name__ == "__main__":
    main()
