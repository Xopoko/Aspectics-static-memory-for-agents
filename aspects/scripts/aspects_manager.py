#!/usr/bin/env python3
"""
Comprehensive CLI for inspecting and modifying ASPECTS.json archives.

Features:
- list sections and entries
- show a specific aspect
- interactively add, update, or delete entries
- import batches from a JSON payload (superset of merge_aspects_entries.py)

All commands operate on the specified ASPECTS.json (defaults to Claude Code).
"""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


DEFAULT_ASPECTS = Path("aspects/projects/claude-code/ASPECTS.json")


def configure_utf8_io() -> None:
    """Ensure stdout/stderr can emit UTF-8 even on Windows legacy consoles."""
    for name in ("stdout", "stderr"):
        stream = getattr(sys, name, None)
        if not stream:
            continue
        try:
            stream.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
            continue
        except (AttributeError, ValueError):
            pass
        try:
            buffer = stream.buffer  # type: ignore[attr-defined]
        except AttributeError:
            continue
        try:
            wrapper = io.TextIOWrapper(buffer, encoding="utf-8", errors="replace")
            setattr(sys, name, wrapper)
        except (AttributeError, OSError):
            pass


def load_json(path: Path) -> Dict[str, Any]:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def save_json(path: Path, payload: Dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def prompt(message: str, default: Optional[str] = None, *, required: bool = False) -> str:
    suffix = f" [{default}]" if default is not None else ""
    while True:
        value = input(f"{message}{suffix}: ").strip()
        if value:
            return value
        if default is not None and not value:
            return default
        if not required:
            return ""
        print("  Value required.")


def prompt_yes_no(message: str, default: bool = False) -> bool:
    default_str = "Y/n" if default else "y/N"
    while True:
        answer = input(f"{message} ({default_str}): ").strip().lower()
        if not answer:
            return default
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("  Please answer y or n.")


def prompt_multiline(message: str, default: Optional[str] = None, *, required: bool = False) -> str:
    print(message)
    if default:
        print("--- current ---")
        print(default)
        print("---------------")
    print("Enter lines; finish with single '.' on its own line.")
    lines: List[str] = []
    while True:
        line = input()
        if line == ".":
            break
        lines.append(line.rstrip())
    text = "\n".join(lines).strip()
    if not text:
        if default:
            return default
        if required:
            print("  Description required.")
            return prompt_multiline(message, default, required=required)
    return text


def index_sections(data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    idx: Dict[str, Dict[str, Any]] = {}
    for section in data["sections"]:
        idx[section["id"]] = section
        idx[section["slug"]] = section
    return idx


def list_sections(data: Dict[str, Any]) -> None:
    print("Sections:")
    for section in data["sections"]:
        print(
            f"- {section['id']} | {section['title']} ({section['slug']}) "
            f"- entries: {len(section['entries'])}"
        )


def build_entry_index(data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    slug_index: Dict[str, Dict[str, Any]] = {}
    for section in data["sections"]:
        for entry in section["entries"]:
            slug_index[entry["slug"]] = entry
    return slug_index


def choose_section(data: Dict[str, Any], current_section: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    sections = data["sections"]
    for idx, section in enumerate(sections, start=1):
        marker = " (current)" if current_section and section["id"] == current_section["id"] else ""
        print(f"{idx:2d}. {section['title']} ({section['slug']}){marker}")
    while True:
        value = prompt("Select section number", required=True)
        try:
            index = int(value)
            if 1 <= index <= len(sections):
                return sections[index - 1]
        except ValueError:
            pass
        print("  Invalid selection.")


def repo_root(aspects_path: Path) -> Path:
    # aspects/projects/<project>/ASPECTS.json -> repo root (two parents + aspects/)
    return aspects_path.parent.parent.parent.parent


def compute_sha256(file_path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with file_path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def gather_tags(default: Optional[List[str]] = None) -> List[str]:
    default_view = ", ".join(default or [])
    raw = prompt(
        "Tags (comma separated, lowercase, no spaces)",
        default=default_view if default else None,
        required=True,
    )
    tags = [tag.strip().lower() for tag in raw.split(",") if tag.strip()]
    unique: List[str] = []
    for tag in tags:
        if tag not in unique:
            unique.append(tag)
    if not unique:
        print("  At least one tag required.")
        return gather_tags(default)
    return unique


def gather_importance(default: Optional[float]) -> float:
    default_str = f"{default:.2f}" if default is not None else "0.50"
    while True:
        raw = prompt("Importance (0.0-1.0)", default_str, required=True)
        try:
            value = float(raw)
        except ValueError:
            print("  Importance must be numeric.")
            continue
        if 0.0 <= value <= 1.0:
            return round(value, 2)
        print("  Importance must be between 0.0 and 1.0.")


def gather_sources(base_path: Path, defaults: Optional[List[Dict[str, str]]] = None) -> List[Dict[str, str]]:
    sources: List[Dict[str, str]] = []
    existing = {(src["path"], src["sha256"]) for src in defaults or []}
    if defaults:
        print("Existing sources:")
        for src in defaults:
            print(f"  - {src['path']} ({src['sha256'][:8]}…)")
        if prompt_yes_no("Keep existing sources by default?", default=True):
            sources.extend(defaults)
    idx = 0
    while True:
        idx += 1
        raw_path = prompt(f"Source #{idx} (relative path, Enter to finish)", required=False)
        if not raw_path:
            break
        relative = raw_path.replace("\\", "/")
        candidate = (base_path / relative).resolve() if not Path(relative).is_absolute() else Path(relative)
        if not candidate.exists():
            print("  File not found.")
            idx -= 1
            continue
        sha = compute_sha256(candidate)
        if (relative, sha) in existing or any(src["path"] == relative for src in sources):
            print("  Duplicate source skipped.")
            idx -= 1
            continue
        sources.append({"path": relative, "sha256": sha})
    if not sources:
        print("  Entry requires >=1 source.")
        return gather_sources(base_path, defaults or [])
    return sources


def ensure_unique(entry: Dict[str, Any], index: Dict[str, Dict[str, Any]], *, allow_same_slug: bool) -> None:
    for slug, existing in index.items():
        if existing["id"] == entry["id"] and slug != entry["slug"]:
            raise ValueError(f"ID '{entry['id']}' already used by slug '{slug}'.")
        if not allow_same_slug and slug == entry["slug"]:
            raise ValueError(f"Slug '{entry['slug']}' already exists.")


def interactive_entry(
    data: Dict[str, Any],
    aspects_path: Path,
    *,
    existing: Optional[Dict[str, Any]] = None,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    base_path = repo_root(aspects_path)
    sections_by_id = {section["id"]: section for section in data["sections"]}
    if existing:
        section = sections_by_id[existing["sectionId"]]
        print(f"Editing '{existing['slug']}' in section '{section['title']}'.")
        if prompt_yes_no("Change section?", default=False):
            section = choose_section(data, current_section=section)
    else:
        section = choose_section(data)

    entry = dict(existing) if existing else {
        "id": "",
        "sectionId": section["id"],
        "slug": "",
        "name": "",
        "description": "",
        "tags": [],
        "sources": [],
        "lastUpdated": date.today().isoformat(),
        "importance": 0.5,
    }
    entry["sectionId"] = section["id"]

    slug_default = entry.get("slug") or None
    entry["slug"] = prompt("Slug (lowercase, hyphenated)", slug_default, required=True)

    if not existing or prompt_yes_no("Update entry id?", default=False):
        entry["id"] = prompt(
            "ID (stable identifier)",
            default=entry.get("id") or f"aspect-{entry['slug']}",
            required=True,
        )

    entry["name"] = prompt("Name", entry.get("name") or None, required=True)
    entry["description"] = prompt_multiline(
        "Description",
        entry.get("description"),
        required=True,
    )
    entry["tags"] = gather_tags(entry.get("tags"))

    entry["importance"] = gather_importance(entry.get("importance"))
    entry["lastUpdated"] = prompt(
        "Last updated (YYYY-MM-DD)",
        entry.get("lastUpdated") or date.today().isoformat(),
        required=True,
    )
    entry["sources"] = gather_sources(base_path, entry.get("sources"))
    return entry, section


def add_entry(args: argparse.Namespace) -> None:
    data = load_json(args.aspects_path)
    entries_by_slug = build_entry_index(data)
    entry, section = interactive_entry(data, args.aspects_path)
    ensure_unique(entry, entries_by_slug, allow_same_slug=False)
    section.setdefault("entries", []).append(entry)
    save_json(args.aspects_path, data)
    print(f"Added entry '{entry['slug']}' to section '{section['title']}'.")


def update_entry(args: argparse.Namespace) -> None:
    data = load_json(args.aspects_path)
    entries_by_slug = build_entry_index(data)
    if args.slug not in entries_by_slug:
        raise SystemExit(f"Entry with slug '{args.slug}' not found.")
    current = entries_by_slug[args.slug]
    # locate section to replace entry later
    section_map = {section["id"]: section for section in data["sections"]}
    current_section = section_map[current["sectionId"]]
    entry, new_section = interactive_entry(data, args.aspects_path, existing=current)
    ensure_unique(entry, {slug: val for slug, val in entries_by_slug.items() if slug != args.slug}, allow_same_slug=True)
    # remove old entry
    current_section["entries"] = [e for e in current_section["entries"] if e["slug"] != args.slug]
    new_section.setdefault("entries", []).append(entry)
    save_json(args.aspects_path, data)
    print(f"Updated entry '{entry['slug']}'.")


def delete_entry(args: argparse.Namespace) -> None:
    data = load_json(args.aspects_path)
    entries_by_slug = build_entry_index(data)
    if args.slug not in entries_by_slug:
        raise SystemExit(f"Entry with slug '{args.slug}' not found.")
    entry = entries_by_slug[args.slug]
    section_map = {section["id"]: section for section in data["sections"]}
    section = section_map[entry["sectionId"]]
    section["entries"] = [e for e in section["entries"] if e["slug"] != args.slug]
    save_json(args.aspects_path, data)
    print(f"Deleted entry '{args.slug}'.")


def list_entries(args: argparse.Namespace) -> None:
    data = load_json(args.aspects_path)
    count = 0
    output_lines = []
    for section in data["sections"]:
        if args.section and section["slug"] != args.section and section["id"] != args.section:
            continue
        for entry in section["entries"]:
            if args.tag and args.tag not in entry.get("tags", []):
                continue
            if args.contains and args.contains.lower() not in entry["name"].lower() and args.contains.lower() not in entry["description"].lower():
                continue
            line = f"{section['slug']}/{entry['slug']} | importance={entry['importance']:.2f} | tags={','.join(entry.get('tags', []))}"
            output_lines.append(line)
            count += 1
    if getattr(args, "output", None):
        if str(args.output) == "-":
            target_stream = sys.stdout
            print("\n".join(output_lines), file=target_stream)
        else:
            Path(args.output).write_text("\n".join(output_lines) + "\n", encoding="utf-8")
            print(f"Wrote {count} entries to {args.output}")
    else:
        for line in output_lines:
            print(line)
        print(f"Total entries matched: {count}")


def show_entry(args: argparse.Namespace) -> None:
    data = load_json(args.aspects_path)
    entries = build_entry_index(data)
    entry = entries.get(args.slug)
    if not entry:
        raise SystemExit(f"Entry '{args.slug}' not found.")
    print(json.dumps(entry, indent=2, ensure_ascii=False))


def stats(args: argparse.Namespace) -> None:
    data = load_json(args.aspects_path)
    warn_count = args.warn_count
    warn_tags = args.warn_unique_tags

    print(f"Sections summary (warn if entries>{warn_count} or unique tags>{warn_tags}):")
    print("slug,title,entries,unique_tags,status")
    for section in data["sections"]:
        entries = section.get("entries", [])
        tags = {tag for entry in entries for tag in entry.get("tags", [])}
        status = []
        if len(entries) > warn_count:
            status.append(f">entries({len(entries)})")
        if len(tags) > warn_tags:
            status.append(f">tags({len(tags)})")
        marker = ";".join(status) if status else "-"
        print(f"{section['slug']},{section['title']},{len(entries)},{len(tags)},{marker}")


def import_entries(args: argparse.Namespace) -> None:
    payload_path = Path(args.payload)
    data = load_json(args.aspects_path)
    payload = load_json(payload_path)

    if isinstance(payload, dict) and "entries" in payload:
        new_entries = payload["entries"]
    elif isinstance(payload, list):
        new_entries = payload
    else:
        raise SystemExit("Payload must be a list of entries or an object with an 'entries' array.")
    section_index = index_sections(data)
    existing_by_slug = build_entry_index(data)

    default_last_updated = args.set_last_updated or date.today().isoformat()
    staged: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    seen_ids: set[str] = set()
    seen_slugs: set[str] = set()

    for entry in new_entries:
        if not isinstance(entry, dict):
            raise SystemExit("Each entry in payload must be an object.")
        section_id = entry.get("sectionId")
        section_slug = entry.get("sectionSlug")
        target = None
        if section_id:
            target = section_index.get(section_id)
        if not target and section_slug:
            target = section_index.get(section_slug)
        if not target:
            raise SystemExit(f"Cannot resolve section for entry '{entry.get('slug')}'. Provide sectionId or sectionSlug.")
        entry["sectionId"] = target["id"]
        entry.pop("sectionSlug", None)
        entry.setdefault("lastUpdated", default_last_updated)

        if entry["id"] in seen_ids or entry["slug"] in seen_slugs:
            raise SystemExit(f"Duplicate id or slug in payload: {entry['id']} / {entry['slug']}")
        seen_ids.add(entry["id"])
        seen_slugs.add(entry["slug"])

        if not args.replace and entry["slug"] in existing_by_slug:
            raise SystemExit(f"Entry with slug '{entry['slug']}' already exists. Use --replace to overwrite.")
        staged[target["id"]].append(entry)

    logs: List[str] = []
    if args.dry_run:
        print("Dry run:")
    for section in data["sections"]:
        entries = staged.get(section["id"])
        if not entries:
            continue
        if args.replace:
            incoming_slugs = {entry["slug"] for entry in entries}
            original_len = len(section["entries"])
            section["entries"] = [entry for entry in section["entries"] if entry["slug"] not in incoming_slugs]
            replaced = original_len - len(section["entries"])
            if replaced:
                logs.append(f"{section['slug']}: replaced {replaced} entries.")
        section["entries"].extend(entries)
        logs.append(f"{section['slug']}: appended {len(entries)} entries.")

    if args.dry_run:
        for log in logs:
            print("  -", log)
        print("No changes written.")
    else:
        save_json(args.aspects_path, data)
        for log in logs:
            print("  -", log)
        print("Entries merged.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage ASPECTS.json knowledge base.",
        allow_abbrev=False,
    )
    parser.add_argument(
        "--aspects-path",
        type=Path,
        default=DEFAULT_ASPECTS,
        help=f"Path to ASPECTS.json (default: {DEFAULT_ASPECTS}).",
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True  # type: ignore[attr-defined]

    subparsers.add_parser("list-sections", help="Print available sections.")

    list_entries_parser = subparsers.add_parser("list-entries", help="List entries with optional filters.")
    list_entries_parser.add_argument("--section", help="Filter by section slug or id.")
    list_entries_parser.add_argument("--tag", help="Filter by tag.")
    list_entries_parser.add_argument("--contains", help="Filter by case-insensitive substring in name/description.")
    list_entries_parser.add_argument("--output", type=Path, help="Write the result to a file (use '-' for stdout).")

    show_parser = subparsers.add_parser("show", help="Show full JSON for an entry by slug.")
    show_parser.add_argument("slug")

    stats_parser = subparsers.add_parser("stats", help="Show per-section counts and unique tag statistics.")
    stats_parser.add_argument("--warn-count", type=int, default=25, help="Warn if entries in section exceed this number (default: 25).")
    stats_parser.add_argument("--warn-unique-tags", type=int, default=10, help="Warn if unique tags in section exceed this number (default: 10).")

    subparsers.add_parser("add", help="Interactively add a new entry.")

    update_parser = subparsers.add_parser("update", help="Interactively update an existing entry.")
    update_parser.add_argument("slug")

    delete_parser = subparsers.add_parser("delete", help="Delete an entry by slug.")
    delete_parser.add_argument("slug")

    import_parser = subparsers.add_parser("import", help="Import entries from a JSON payload.")
    import_parser.add_argument("payload", help="Path to JSON payload (array or {\"entries\": [...]})")
    import_parser.add_argument("--replace", action="store_true", help="Overwrite entries with matching slug/id.")
    import_parser.add_argument("--dry-run", action="store_true", help="Print actions without writing to disk.")
    import_parser.add_argument("--set-last-updated", type=str, help="Override lastUpdated for entries missing the field.")

    return parser


def main() -> None:
    configure_utf8_io()
    parser = build_parser()
    args, remainder = parser.parse_known_args()
    if remainder:
        if len(remainder) == 1:
            args.aspects_path = Path(remainder[0])
        else:
            parser.error(f"Unexpected extra arguments: {' '.join(remainder)}")

    if not args.aspects_path.exists():
        raise SystemExit(f"ASPECTS file not found: {args.aspects_path}")

    command = args.command
    if command == "list-sections":
        list_sections(load_json(args.aspects_path))
    elif command == "list-entries":
        list_entries(args)
    elif command == "show":
        show_entry(args)
    elif command == "stats":
        stats(args)
    elif command == "add":
        add_entry(args)
    elif command == "update":
        update_entry(args)
    elif command == "delete":
        delete_entry(args)
    elif command == "import":
        import_entries(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
