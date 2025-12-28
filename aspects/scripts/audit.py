#!/usr/bin/env python3
"""Utility checks for ASPECTS.json consistency.

This script validates entry identifiers, slugs, section links, duplicated sources and
reports sections that look under-populated or overloaded so that the curator can
plan restructuring work ahead of time.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path


def load_aspects(aspects_path: Path) -> dict:
    try:
        with aspects_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as exc:
        raise SystemExit(f"ASPECTS file not found: {aspects_path}") from exc


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate structural consistency of an ASPECTS.json knowledge base.",
    )
    parser.add_argument(
        "aspects_path",
        type=Path,
        help="Path to the ASPECTS.json file to audit.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    aspects_path = args.aspects_path
    if not aspects_path.is_absolute():
        aspects_path = aspects_path.resolve()

    data = load_aspects(aspects_path)

    sections = data.get("sections", [])
    errors: list[str] = []
    warnings: list[str] = []

    entry_ids: dict[str, str] = {}
    entry_slugs: dict[str, str] = {}

    total_entries = 0
    for section in sections:
        section_id = section["id"]
        entries = section.get("entries", [])
        total_entries += len(entries)

        if len(entries) <= 6:
            warnings.append(
                f"section {section_id} has {len(entries)} entries (<=6)"
            )
        if len(entries) > 25:
            warnings.append(
                f"section {section_id} has {len(entries)} entries (>25)"
            )

        tags_counter: Counter[str] = Counter()

        for entry in entries:
            entry_id = entry["id"]
            if entry_id in entry_ids:
                errors.append(
                    f"duplicate entry id: {entry_id} ({section_id} vs {entry_ids[entry_id]})"
                )
            else:
                entry_ids[entry_id] = section_id

            entry_slug = entry["slug"]
            if entry_slug in entry_slugs:
                errors.append(
                    f"duplicate entry slug: {entry_slug} ({section_id} vs {entry_slugs[entry_slug]})"
                )
            else:
                entry_slugs[entry_slug] = section_id

            if entry.get("sectionId") != section_id:
                errors.append(
                    f"entry section mismatch: {entry_id} references {entry.get('sectionId')}"
                )

            tags = entry.get("tags", [])
            if len(tags) != len(set(tags)):
                errors.append(f"duplicate tags in entry: {entry_id}")
            tags_counter.update(tags)

            seen_sources: set[str] = set()
            for source in entry.get("sources", []):
                path = source.get("path")
                if not path:
                    errors.append(f"empty source path in entry: {entry_id}")
                    continue
                if path in seen_sources:
                    errors.append(
                        f"duplicate source path {path} in entry: {entry_id}"
                    )
                seen_sources.add(path)

            importance = entry.get("importance")
            if importance is None:
                errors.append(f"entry {entry_id} missing importance field")
            else:
                try:
                    importance_value = float(importance)
                except (TypeError, ValueError):
                    errors.append(
                        f"entry {entry_id} has non-numeric importance: {importance!r}"
                    )
                else:
                    if not 0.0 <= importance_value <= 1.0:
                        errors.append(
                            f"entry {entry_id} importance out of range [0,1]: {importance_value}"
                        )

        if len(tags_counter) > 10:
            warnings.append(
                f"section {section_id} uses {len(tags_counter)} unique tags (>10)"
            )

    print(f"Sections: {len(sections)} | Entries: {total_entries}")

    if errors:
        print("\nErrors:")
        for item in errors:
            print(f"  - {item}")

    if warnings:
        print("\nWarnings:")
        for item in warnings:
            print(f"  - {item}")

    if not errors and not warnings:
        print("No issues detected.")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
