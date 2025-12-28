#!/usr/bin/env python3
"""Compute Aspect-Density Index (ADI) for an ASPECTS.json knowledge base.

ADI is defined as the ratio between the number of aspects (nodes) and the
average number of connections (degree) per aspect. This helper supports both
classic (unweighted) and inverse-frequency weighted degrees, filters
high-frequency “hub” tags, and can treat explicit slug mentions and shared
sources as additional connections.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path


@dataclass(frozen=True)
class Entry:
    slug: str
    slug_lower: str
    section_slug: str
    tags: frozenset[str]
    sources: frozenset[str]
    text: str


@dataclass(frozen=True)
class GraphStats:
    nodes: int
    edges: int
    average_degree: float
    adi: float
    isolated: int
    isolated_slugs: tuple[str, ...]
    weighted_edges: float | None = None
    weighted_average_degree: float | None = None
    weighted_adi: float | None = None


def load_entries(path: Path) -> list[Entry]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"ASPECTS file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc

    entries: list[Entry] = []
    slug_lower_index: dict[str, str] = {}
    slug_lower_values: list[str] = []
    id_values: list[str] = []
    for section in data.get("sections", []):
        section_slug = section.get("slug")
        if not section_slug:
            continue
        for entry in section.get("entries", []):
            slug = entry.get("slug")
            if not slug:
                continue
            slug_lower = slug.lower()
            slug_lower_index.setdefault(slug_lower, slug)
            slug_lower_values.append(slug_lower)
            entry_id = entry.get("id")
            if entry_id:
                id_values.append(entry_id)
            tags = frozenset(entry.get("tags", []))
            sources = frozenset(
                source["path"]
                for source in entry.get("sources", [])
                if isinstance(source, dict) and isinstance(source.get("path"), str)
            )
            text = (
                f"{entry.get('name', '')}\n{entry.get('description', '')}"
            ).lower()
            entries.append(
                Entry(
                    slug=slug,
                    slug_lower=slug_lower,
                    section_slug=section_slug,
                    tags=tags,
                    sources=sources,
                    text=text,
                )
            )

    duplicate_slugs = [
        slug_lower_index[slug_lower]
        for slug_lower, count in Counter(slug_lower_values).items()
        if count > 1
    ]
    if duplicate_slugs:
        sample = ", ".join(sorted(duplicate_slugs)[:5])
        more = ""
        if len(duplicate_slugs) > 5:
            more = f"... (+{len(duplicate_slugs) - 5} more)"
        raise SystemExit(
            f"Duplicate slugs detected (case-insensitive): {sample}{more}. "
            "Resolve duplicates before computing ADI."
        )

    duplicate_ids = [
        ident for ident, count in Counter(id_values).items() if count > 1
    ]
    if duplicate_ids:
        sample = ", ".join(sorted(duplicate_ids)[:5])
        more = ""
        if len(duplicate_ids) > 5:
            more = f"... (+{len(duplicate_ids) - 5} more)"
        raise SystemExit(
            f"Duplicate entry ids detected: {sample}{more}. "
            "Resolve duplicates before computing ADI."
        )

    return entries


def load_tag_reference_counts(path: Path | None) -> dict[str, int] | None:
    if path is None:
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Tags catalog not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in tags catalog {path}: {exc}") from exc

    tags = data.get("tags")
    if not isinstance(tags, list):
        raise SystemExit(f"Invalid tags catalog format: expected 'tags' array in {path}")

    counts: dict[str, int] = {}
    for item in tags:
        if not isinstance(item, dict):
            continue
        tag = item.get("tag")
        count = item.get("number_of_references")
        if isinstance(tag, str) and isinstance(count, int):
            counts[tag] = count
    return counts or None


def build_adjacency(
    entries: list[Entry],
    include_slug_links: bool,
    include_source_links: bool,
    ignore_tag_frac: float | None,
    weighted: bool,
    idf_gamma: float,
    tag_reference_counts: dict[str, int] | None,
) -> tuple[dict[str, set[str]], dict[str, dict[str, float]] | None]:
    adjacency: dict[str, set[str]] = {entry.slug: set() for entry in entries}
    weighted_adj: dict[str, dict[str, float]] | None = (
        {entry.slug: {} for entry in entries} if weighted else None
    )

    tag_counts_cache: dict[str, int] = {}
    missing_catalog_tags: set[str] = set()
    mismatch_catalog_tags: set[str] = set()

    def resolved_count(tag: str, slugs: list[str]) -> int:
        if tag in tag_counts_cache:
            return tag_counts_cache[tag]
        base = len(slugs)
        if tag_reference_counts is None:
            tag_counts_cache[tag] = base
            return base
        catalog_freq = tag_reference_counts.get(tag)
        if catalog_freq is None:
            if len(missing_catalog_tags) < 5 and tag not in missing_catalog_tags:
                print(
                    f"[adi] Warning: tag '{tag}' has no cached count in catalog; "
                    "run tags_manager.py sync-counts.",
                    file=sys.stderr,
                )
            missing_catalog_tags.add(tag)
            tag_counts_cache[tag] = base
            return base
        if catalog_freq != base and tag not in mismatch_catalog_tags:
            if len(mismatch_catalog_tags) < 5:
                print(
                    f"[adi] Warning: tag '{tag}' count mismatch "
                    f"(catalog={catalog_freq}, aspects={base}); "
                    "run tags_manager.py sync-counts.",
                    file=sys.stderr,
                )
            mismatch_catalog_tags.add(tag)
        value = max(base, catalog_freq)
        tag_counts_cache[tag] = value
        return value

    def add_edge(a: str, b: str, weight: float) -> None:
        adjacency[a].add(b)
        adjacency[b].add(a)
        if weighted_adj is not None:
            weighted_adj[a][b] = weighted_adj[a].get(b, 0.0) + weight
            weighted_adj[b][a] = weighted_adj[b].get(a, 0.0) + weight

    # Tag-based links -----------------------------------------------------
    tag_index: defaultdict[str, list[str]] = defaultdict(list)
    for entry in entries:
        for tag in entry.tags:
            tag_index[tag].append(entry.slug)

    total_entries = len(entries)
    ignored_tags: set[str] = set()
    if ignore_tag_frac is not None and total_entries > 0:
        ignored_tags = {
            tag
            for tag, slugs in tag_index.items()
            if resolved_count(tag, slugs) / total_entries >= ignore_tag_frac
        }

    for tag, slugs in tag_index.items():
        if tag in ignored_tags or len(slugs) < 2:
            continue
        references = resolved_count(tag, slugs)
        weight = 1.0
        if weighted:
            denom = math.log2(1 + references)
            if denom <= 0:
                continue
            weight = 1.0 / (denom**idf_gamma)
        for a, b in combinations(slugs, 2):
            add_edge(a, b, weight)

    # Source-based links --------------------------------------------------
    if include_source_links:
        source_index: defaultdict[str, list[str]] = defaultdict(list)
        for entry in entries:
            for source in entry.sources:
                source_index[source].append(entry.slug)
        for slugs in source_index.values():
            if len(slugs) < 2:
                continue
            for a, b in combinations(slugs, 2):
                add_edge(a, b, 1.0)

    # Explicit slug mentions ----------------------------------------------
    if include_slug_links:
        patterns = {
            entry.slug: re.compile(
                rf"(?<![a-z0-9_-]){re.escape(entry.slug_lower)}(?![a-z0-9_-])"
            )
            for entry in entries
        }
        for idx, entry in enumerate(entries):
            for other in entries[idx + 1 :]:
                if (
                    patterns[other.slug].search(entry.text)
                    or patterns[entry.slug].search(other.text)
                ):
                    add_edge(entry.slug, other.slug, 1.0)

    if tag_reference_counts is not None:
        if len(missing_catalog_tags) > 5:
            suppressed = len(missing_catalog_tags) - 5
            print(
                f"[adi] Warning: {suppressed} additional tags missing catalog counts (suppressed).",
                file=sys.stderr,
            )
        if len(mismatch_catalog_tags) > 5:
            suppressed = len(mismatch_catalog_tags) - 5
            print(
                f"[adi] Warning: {suppressed} additional catalog/tag count mismatches suppressed.",
                file=sys.stderr,
            )

    return adjacency, weighted_adj


def compute_stats(
    slugs: set[str],
    adjacency: dict[str, set[str]],
    weighted_adj: dict[str, dict[str, float]] | None,
) -> GraphStats:
    if not slugs:
        return GraphStats(0, 0, 0.0, math.inf, 0, tuple())

    total_degree = 0
    isolated = 0
    isolated_slugs: list[str] = []
    total_weighted_degree = 0.0
    for slug in slugs:
        neighbors = adjacency.get(slug, set()) & slugs
        degree = len(neighbors)
        total_degree += degree
        if degree == 0:
            isolated += 1
            isolated_slugs.append(slug)
        if weighted_adj is not None:
            weighted_neighbors = weighted_adj.get(slug, {})
            total_weighted_degree += sum(
                weight for neighbor, weight in weighted_neighbors.items() if neighbor in slugs
            )

    average_degree = total_degree / len(slugs)
    edges = int(total_degree / 2)
    adi = math.inf if average_degree == 0 else len(slugs) / average_degree
    weighted_average_degree: float | None = None
    weighted_edges: float | None = None
    weighted_adi: float | None = None
    if weighted_adj is not None:
        weighted_average_degree = total_weighted_degree / len(slugs)
        weighted_edges = total_weighted_degree / 2
        weighted_adi = (
            math.inf
            if weighted_average_degree == 0
            else len(slugs) / weighted_average_degree
        )

    return GraphStats(
        nodes=len(slugs),
        edges=edges,
        average_degree=average_degree,
        adi=adi,
        isolated=isolated,
        isolated_slugs=tuple(sorted(isolated_slugs)),
        weighted_edges=weighted_edges,
        weighted_average_degree=weighted_average_degree,
        weighted_adi=weighted_adi,
    )


def format_float(value: float) -> str:
    if math.isinf(value):
        return "inf"
    return f"{value:.2f}"


def print_stats(title: str, stats: GraphStats) -> None:
    message = (
        f"{title}: aspects={stats.nodes}, edges={stats.edges}, "
        f"avg_degree={format_float(stats.average_degree)}, "
        f"ADI={format_float(stats.adi)}, isolated={stats.isolated}"
    )
    if stats.weighted_average_degree is not None and stats.weighted_adi is not None:
        message += (
            f", weighted_avg_degree={format_float(stats.weighted_average_degree)}, "
            f"ADIw={format_float(stats.weighted_adi)}"
        )
    print(message)


def run(
    aspects_path: Path,
    per_section: bool,
    include_slug_links: bool,
    include_source_links: bool,
    ignore_tag_frac: float | None,
    weighted: bool,
    idf_gamma: float,
    adi_threshold: float,
    show_isolates: bool,
    isolate_limit: int | None,
    tag_reference_counts: dict[str, int] | None,
) -> None:
    entries = load_entries(aspects_path)
    if not entries:
        raise SystemExit("No entries found in the ASPECTS file.")

    adjacency, weighted_adj = build_adjacency(
        entries,
        include_slug_links=include_slug_links,
        include_source_links=include_source_links,
        ignore_tag_frac=ignore_tag_frac,
        weighted=weighted,
        idf_gamma=idf_gamma,
        tag_reference_counts=tag_reference_counts,
    )

    all_slugs = {entry.slug for entry in entries}
    overall = compute_stats(all_slugs, adjacency, weighted_adj)
    print_stats("Overall", overall)
    warning_triggered = False
    overall_metric = (
        overall.weighted_adi if weighted and overall.weighted_adi is not None else overall.adi
    )
    if overall_metric >= adi_threshold or math.isinf(overall_metric):
        warning_triggered = True
        label = "ADIw" if weighted and overall.weighted_adi is not None else "ADI"
        value = format_float(overall_metric)
        print(f"!! Overall {label} {value} >= threshold {adi_threshold:.2f}")
    if show_isolates and overall.isolated:
        print("  Isolated aspects:")
        isolates = overall.isolated_slugs
        if isolate_limit is not None:
            isolates = isolates[:isolate_limit]
        for slug in isolates:
            print(f"    - {slug}")
        if isolate_limit is not None and overall.isolated > isolate_limit:
            print(f"    ... ({overall.isolated - isolate_limit} more)")

    if per_section:
        print()
        print("Per section:")
        sections: defaultdict[str, set[str]] = defaultdict(set)
        for entry in entries:
            sections[entry.section_slug].add(entry.slug)

        high_sections: list[tuple[str, GraphStats]] = []
        for section_slug in sorted(sections):
            stats = compute_stats(sections[section_slug], adjacency, weighted_adj)
            print_stats(f"  {section_slug}", stats)
            metric = (
                stats.weighted_adi if weighted and stats.weighted_adi is not None else stats.adi
            )
            if metric >= adi_threshold or math.isinf(metric):
                high_sections.append((section_slug, stats))
            if show_isolates and stats.isolated:
                isolates = stats.isolated_slugs
                if isolate_limit is not None:
                    isolates = isolates[:isolate_limit]
                for slug in isolates:
                    print(f"    * isolated: {slug}")
                if isolate_limit is not None and stats.isolated > isolate_limit:
                    remaining = stats.isolated - isolate_limit
                    print(f"    * ... ({remaining} more)")

        if high_sections:
            warning_triggered = True
            print()
            print("Sections exceeding threshold:")
            for section_slug, stats in high_sections:
                metric = (
                    stats.weighted_adi
                    if weighted and stats.weighted_adi is not None
                    else stats.adi
                )
                label = "ADIw" if weighted and stats.weighted_adi is not None else "ADI"
                print(
                    f"  - {section_slug}: {label}={format_float(metric)}, "
                    f"avg_degree={format_float(stats.average_degree)}, "
                    f"isolated={stats.isolated}"
                )

    if not warning_triggered and not (show_isolates and overall.isolated):
        print()
        print("ADI within target thresholds; no high-risk sections detected.")


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate the Aspect-Density Index (ADI) for ASPECTS.json."
    )
    parser.add_argument(
        "aspects_path",
        type=Path,
        help="Path to the ASPECTS.json file.",
    )
    parser.add_argument(
        "--per-section",
        action="store_true",
        help="Calculate ADI for each section in addition to the global value.",
    )
    parser.add_argument(
        "--include-slug-links",
        action="store_true",
        help="Treat explicit slug mentions in names/descriptions as additional connections.",
    )
    parser.add_argument(
        "--include-source-links",
        action="store_true",
        help="Treat shared source file paths as links between aspects.",
    )
    parser.add_argument(
        "--tags-catalog",
        help="Optional path to ASPECTS.tags.json for cached tag reference counts.",
    )
    parser.add_argument(
        "--ignore-tag-frac",
        type=float,
        default=None,
        help=(
            "Ignore tags that appear in at least this fraction of entries when building tag links "
            "(e.g. 0.15 to drop very common tags)."
        ),
    )
    parser.add_argument(
        "--weighted",
        action="store_true",
        help="Calculate weighted ADI using inverse-frequency weights for tag-derived links.",
    )
    parser.add_argument(
        "--idf-gamma",
        type=float,
        default=1.0,
        help=(
            "Exponent applied to the tag weight denominator: weight(tag)=1/log2(1+freq)^gamma. "
            "Default: 1.0."
        ),
    )
    parser.add_argument(
        "--adi-threshold",
        type=float,
        default=4.0,
        help="Threshold that triggers a warning when ADI is greater or equal. Default: 4.0",
    )
    parser.add_argument(
        "--show-isolates",
        action="store_true",
        help="List isolated aspects (zero degree).",
    )
    parser.add_argument(
        "--isolate-limit",
        type=int,
        help="Maximum number of isolates to list per scope when --show-isolates is used.",
    )
    args = parser.parse_args(argv)
    if args.ignore_tag_frac is not None and not (0.0 <= args.ignore_tag_frac <= 1.0):
        parser.error("--ignore-tag-frac must be between 0.0 and 1.0")
    if args.idf_gamma <= 0:
        parser.error("--idf-gamma must be greater than 0")
    return args


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    tag_reference_counts = load_tag_reference_counts(
        Path(args.tags_catalog) if args.tags_catalog else None
    )
    run(
        aspects_path=args.aspects_path,
        per_section=args.per_section,
        include_slug_links=args.include_slug_links,
        include_source_links=args.include_source_links,
        ignore_tag_frac=args.ignore_tag_frac,
        weighted=args.weighted,
        idf_gamma=args.idf_gamma,
        adi_threshold=args.adi_threshold,
        show_isolates=args.show_isolates,
        isolate_limit=args.isolate_limit,
        tag_reference_counts=tag_reference_counts,
    )


if __name__ == "__main__":
    main()
