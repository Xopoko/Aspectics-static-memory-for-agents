#!/usr/bin/env python3
"""Utilities for maintaining project tag catalogs (ASPECTS.tags.json)."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def compute_reference_counts(aspects_path: Path) -> Counter[str]:
    data = load_json(aspects_path)
    counter: Counter[str] = Counter()
    for section in data.get("sections", []):
        for entry in section.get("entries", []):
            counter.update(entry.get("tags", []))
    return counter


def ensure_sorted(tags_payload: dict[str, Any]) -> None:
    tags_payload["tags"] = sorted(
        tags_payload.get("tags", []), key=lambda item: item.get("tag", "")
    )


def sync_counts(
    tags_path: Path,
    aspects_path: Path,
    dry_run: bool,
    quiet: bool,
) -> int:
    counts = compute_reference_counts(aspects_path)
    tags_payload = load_json(tags_path)
    ensure_sorted(tags_payload)

    catalog_tags = {entry.get("tag") for entry in tags_payload.get("tags", [])}
    missing_in_catalog = sorted(set(counts) - catalog_tags)
    missing_in_aspects = sorted(tag for tag in catalog_tags if counts[tag] == 0)

    updated = 0
    for entry in tags_payload.get("tags", []):
        tag = entry.get("tag")
        if tag is None:
            continue
        value = counts.get(tag, 0)
        if entry.get("number_of_references") != value:
            entry["number_of_references"] = value
            updated += 1

    if updated and not dry_run:
        tags_path.write_text(dump_json(tags_payload), encoding="utf-8")
    elif updated and dry_run:
        sys.stdout.write(dump_json(tags_payload))
        sys.stdout.write("\n")

    if not quiet:
        print(
            f"Updated {updated} tag entries "
            f"(catalog: {tags_path}, aspects: {aspects_path})"
        )
        if missing_in_catalog:
            print(
                "Tags present in ASPECTS.json but missing in catalog:",
                ", ".join(missing_in_catalog),
                file=sys.stderr,
            )
        if missing_in_aspects:
            print(
                "Catalog tags not referenced in ASPECTS.json:",
                ", ".join(missing_in_aspects),
                file=sys.stderr,
            )

    return updated


def print_counts(counter: Counter[str], as_json: bool, limit: int | None) -> None:
    items: Iterable[tuple[str, int]] = sorted(counter.items())
    if limit is not None:
        items = list(items)[:limit]
    if as_json:
        print(
            dump_json(
                {tag: count for tag, count in items}
            )
        )
        return
    width = max((len(tag) for tag, _ in items), default=0)
    for tag, count in items:
        print(f"{tag.ljust(width)}  {count}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage tag catalogs (ASPECTS.tags.json)."
    )
    parser.add_argument(
        "--tags-path",
        help="Override path to ASPECTS.tags.json.",
    )
    parser.add_argument(
        "--aspects-path",
        help="Override path to ASPECTS.json.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    counts_parser = subparsers.add_parser(
        "counts",
        help="Print tag reference counts derived from ASPECTS.json.",
    )
    counts_parser.add_argument(
        "--json",
        action="store_true",
        help="Emit counts as JSON.",
    )
    counts_parser.add_argument(
        "--limit",
        type=int,
        help="Limit the number of tags displayed (alphabetical order).",
    )

    sync_parser = subparsers.add_parser(
        "sync-counts",
        help="Populate number_of_references in ASPECTS.tags.json.",
    )
    sync_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the updated payload instead of writing to disk.",
    )
    sync_parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress informational output.",
    )

    return parser


def resolve_paths(args: argparse.Namespace, parser: argparse.ArgumentParser) -> tuple[Path, Path]:
    if args.tags_path is None:
        parser.error("--tags-path is required")
    tags_path = Path(args.tags_path)

    if args.aspects_path is not None:
        aspects_path = Path(args.aspects_path)
    else:
        aspects_path = tags_path.with_name("ASPECTS.json")

    return tags_path, aspects_path


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "counts":
        if args.aspects_path is not None:
            aspects_path = Path(args.aspects_path)
        elif args.tags_path is not None:
            aspects_path = Path(args.tags_path).with_name("ASPECTS.json")
        else:
            parser.error("--aspects-path (or --tags-path to infer it) is required for counts")
        if not aspects_path.exists():
            parser.error(f"ASPECTS.json not found: {aspects_path}")
        counter = compute_reference_counts(aspects_path)
        print_counts(counter, as_json=args.json, limit=args.limit)
        return 0

    if args.command == "sync-counts":
        tags_path, aspects_path = resolve_paths(args, parser)
        if not tags_path.exists():
            parser.error(f"Tags catalog not found: {tags_path}")
        if not aspects_path.exists():
            parser.error(f"ASPECTS.json not found: {aspects_path}")
        sync_counts(
            tags_path=tags_path,
            aspects_path=aspects_path,
            dry_run=args.dry_run,
            quiet=args.quiet,
        )
        return 0

    parser.error(f"Unhandled command: {args.command}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
