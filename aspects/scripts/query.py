#!/usr/bin/env python3
"""Query helper for ASPECTS.json.

Allows filtering entries by importance, tags and text search so agents can quickly
refresh critical knowledge before starting work.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable, Sequence
import io

if isinstance(sys.stdout, io.TextIOWrapper):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def load_aspects(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as handler:
            return json.load(handler)
    except FileNotFoundError as exc:
        raise SystemExit(f"ASPECTS file not found: {path}") from exc


def iter_entries(data: dict) -> Iterable[tuple[dict, dict]]:
    for section in data.get("sections", []):
        for entry in section.get("entries", []):
            yield section, entry


def format_entry(section: dict, entry: dict) -> str:
    importance = float(entry.get("importance", 0.0))
    title = section.get("title", section.get("id"))
    return (
        f"[{importance:.2f}] {entry['name']} "
        f"(section: {title}, slug: {entry['slug']})\n"
        f"    {entry['description']}"
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Filter ASPECTS entries by importance, tags and keywords."
    )
    parser.add_argument(
        "--min-importance",
        type=float,
        default=0.0,
        help="Lower bound for importance (inclusive). Default: 0.0",
    )
    parser.add_argument(
        "--max-importance",
        type=float,
        default=1.0,
        help="Upper bound for importance (inclusive). Default: 1.0",
    )
    parser.add_argument(
        "--tag",
        action="append",
        dest="tags",
        help="Filter by tag (can be repeated).",
    )
    parser.add_argument(
        "--contains",
        action="append",
        dest="contains",
        metavar="TEXT",
        help="Case-insensitive substring to require in name or description. Can be repeated; all values must match.",
    )
    parser.add_argument(
        "--any-tag",
        action="append",
        dest="any_tags",
        metavar="TAG",
        help="Require at least one of the provided tags. Can be repeated.",
    )
    parser.add_argument(
        "--section",
        help="Filter by section slug.",
    )
    parser.add_argument(
        "--sort-by",
        choices=("importance", "name", "section"),
        default="importance",
        help="Sort results by the given field. Default: importance.",
    )
    parser.add_argument(
        "--ascending",
        action="store_true",
        help="Sort ascending (default is descending for importance).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Return only the first N results after sorting.",
    )
    parser.add_argument(
        "--print-sources",
        action="store_true",
        help="Print sources for each matched entry in text mode.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON array.",
    )
    parser.add_argument(
        "aspects_path",
        type=Path,
        help="Path to the ASPECTS.json file to query.",
    )
    return parser.parse_args(argv)


def matches_filters(
    section: dict,
    entry: dict,
    *,
    min_importance: float,
    max_importance: float,
    tags: list[str] | None,
    any_tags: list[str] | None,
    contains: Sequence[str] | None,
    section_slug: str | None,
) -> bool:
    importance = entry.get("importance")
    if importance is None:
        return False
    try:
        importance_value = float(importance)
    except (TypeError, ValueError):
        return False

    if not (min_importance <= importance_value <= max_importance):
        return False

    if section_slug and section.get("slug") != section_slug:
        return False

    if tags:
        entry_tags = set(entry.get("tags", []))
        if not all(tag in entry_tags for tag in tags):
            return False
    if any_tags:
        entry_tags = set(entry.get("tags", []))
        if not any(tag in entry_tags for tag in any_tags):
            return False

    if contains:
        haystack = f"{entry.get('name', '')}\n{entry.get('description', '')}".lower()
        for needle in contains:
            lowered = needle.lower()
            if lowered not in haystack:
                return False

    return True


def sort_results(results: list[dict], sort_by: str, ascending: bool) -> None:
    def key(item: dict):
        entry = item["entry"]
        section = item["section"]
        if sort_by == "importance":
            return float(entry.get("importance", 0.0))
        if sort_by == "name":
            return entry.get("name", "").lower()
        return section.get("slug", "")

    reverse = not ascending if sort_by == "importance" else ascending is False
    results.sort(key=key, reverse=reverse)


def print_entry(item: dict, *, show_sources: bool) -> None:
    section = item["section"]
    entry = item["entry"]
    print(format_entry(section, entry))

    tags = entry.get("tags") or []
    if tags:
        print(f"    tags: {', '.join(tags)}")

    if show_sources:
        sources = entry.get("sources") or []
        if sources:
            print("    sources:")
            for source in sources:
                path = source.get("path", "<unknown>")
                sha = source.get("sha256", "<missing>")
                print(f"      - {path} ({sha})")
    print()


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    aspects_path = args.aspects_path
    if not aspects_path.is_absolute():
        aspects_path = aspects_path.resolve()
    data = load_aspects(aspects_path)

    results: list[dict] = []
    for section, entry in iter_entries(data):
        if matches_filters(
            section,
            entry,
            min_importance=args.min_importance,
            max_importance=args.max_importance,
            tags=args.tags,
            any_tags=args.any_tags,
            contains=args.contains or [],
            section_slug=args.section,
        ):
            results.append({"section": section, "entry": entry})

    sort_results(results, args.sort_by, args.ascending)

    if args.limit is not None and args.limit >= 0:
        results = results[: args.limit]

    if args.json:
        payload = [
            {
                "section": item["section"]["slug"],
                "importance": item["entry"].get("importance"),
                "id": item["entry"]["id"],
                "slug": item["entry"]["slug"],
                "name": item["entry"]["name"],
                "description": item["entry"]["description"],
                "tags": item["entry"].get("tags", []),
                "sources": item["entry"].get("sources", []),
            }
            for item in results
        ]
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        if not results:
            print("No entries found.")
        else:
            for item in results:
                print_entry(item, show_sources=args.print_sources)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
