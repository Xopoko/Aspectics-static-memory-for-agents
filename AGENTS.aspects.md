# AGENTS.aspects.md

## 1. Purpose

- Provide complete and verifiable knowledge about a project: architecture, infrastructure, business processes, UX, automation, metrics, tooling, and other aspects.
- Working artifact: `aspects/projects/<project_name>/ASPECTS.json`. Every statement must be supported by files in `projects/<project_name>/`.
- Each entry must reference at least one verifiable source as `{ path, sha256 }`.

## 2. Knowledge base structure

The files `aspects/sections_list_example.md` and `aspects/tags_list_example.md` contain examples of sections and tags. Use them as guidance during discovery.

### 2.1 Sections

Sections group aspects by meaning. Required fields:

- `id` - stable identifier (for example, `section-automation`).
- `slug` - short alias (`automation`).
- `title` - human-readable name.
- `entries` - list of aspects; sections must not be empty.

### 2.2 Entries (aspects)

Required entry fields:

- `id`, `sectionId`, `slug` - stable keys.
- `name` - short name.
- `description` - concrete explanation of value and details.
- `tags` - list of tags (lowercase, no spaces).
- `sources` - array of objects `{ path, sha256 }`.
- `lastUpdated` - date in `YYYY-MM-DD` format.
- `importance` - number from `0.0` to `1.0`.

### 2.3 Importance scale (`importance`)

- `importance` reflects how valuable the entry is for understanding the project.
- Recommended ranges:
  - `0.80-1.00` - critical foundation (read before any task; justify in description).
  - `0.60-0.79` - core domain knowledge.
  - `0.30-0.59` - useful context when relevant.
  - `0.00-0.29` - reference or historical context.

**Important:** `importance` is subjective, but it must reflect real value for a newcomer trying to understand the project quickly. Treat it as an attention signal.

### 2.4 Sources and relevance

- Prefer code, configs, and scripts as sources. `.md` files are acceptable only when the aspect is about documentation or a workflow that is actually used (prompts, runbooks, etc.). Do not cite documentation that is detached from the real project state.
- Recompute sha256 when a source changes: `shasum -a 256 <file>`.
- Do not allow duplicate paths in `sources`.

### 2.5 JSON schema

The full schema is provided in Appendix B and is used to validate structure.

## 3. Mandatory workflow

### 3.1 Before you start

1. Read critical aspects:
   ```bash
   python3 aspects/scripts/query.py aspects/projects/<project_name>/ASPECTS.json \
     --min-importance 0.8 --sort-by importance --limit 50
   ```

   > PowerShell does not support `python - <<'PY'`. Use `python -c "..."` or a temporary `.py` file instead (see Section 8).

2. Review the task and repository history.

### 3.2 Adding or updating entries

1. Look for duplicates (for example, `rg "<slug>" aspects/projects/<project_name>/ASPECTS.json`).
2. Pick a suitable section or create a new one with stable `id` and `slug`.
   - If an aspect does not help understand the project or process, skip it.
   - Do not create aspects from aggregated change lists (`CHANGELOG.md`, release notes, etc.). Use concrete files as sources instead.
3. Write a clear, specific `name` and `description`.
4. Select tags. For new tags, agree on them first and add them to the tag catalog (see Section 5).
5. Add `sources` and compute sha256.
6. Update `importance`, `lastUpdated`, and `sectionId`.
7. Check section integrity (non-empty list, unique `id`/`slug`).

### 3.3 After update

1. Run the checks from Section 4.4.
2. Verify that all touched entries have updated `lastUpdated`, `sources`, `importance`, tags, and `sectionId`.
3. Add new tags to `aspects/projects/<project_name>/ASPECTS.tags.json` and sync counts:
   ```bash
   python3 aspects/scripts/tags_manager.py \
     --tags-path aspects/projects/<project_name>/ASPECTS.tags.json sync-counts
   ```
4. Update `aspects/projects/<project_name>/ASPECTS.status.md` if the structure changed or a significant entry was added.
5. Check `git status` and delete temporary files (for example, `NUL`, `tmp/*.json`).
6. If a section exceeds 25 entries, prepare an aggregation plan and record it in `ASPECTS.status.md`.

## 4. Tools and checks

### 4.1 `aspects_manager.py`

`aspects_manager.py` is the main CLI for manual and batch maintenance of `ASPECTS.json`.

| Command | Purpose and notes |
| --- | --- |
| `python3 aspects/scripts/aspects_manager.py list-sections` | Overview of sections: slug, title, entry count, unique tags. |
| `python3 aspects/scripts/aspects_manager.py list-entries [--section <slug|id>] [--tag <tag>] [--contains <substring>] [--output <path>]` | Filter and export entries. |
| `python3 aspects/scripts/aspects_manager.py show <slug>` | Show the full JSON for a specific aspect. |
| `python3 aspects/scripts/aspects_manager.py stats [--warn-count 25] [--warn-unique-tags 10]` | Section metrics with warning thresholds. |
| `python3 aspects/scripts/aspects_manager.py add` | Interactive entry creation. |
| `python3 aspects/scripts/aspects_manager.py update <slug>` | Interactive update for an entry. |
| `python3 aspects/scripts/aspects_manager.py delete <slug>` | Delete by slug (confirmation required). |
| `python3 aspects/scripts/aspects_manager.py import tmp/payload.json [--dry-run] [--replace] [--set-last-updated YYYY-MM-DD]` | Batch import; `--dry-run` previews changes. |

You can append `aspects/projects/<project_name>/ASPECTS.json` to any command (equivalent to `--aspects-path`) when working across multiple projects.

Usage patterns:

- Local revision: `list-sections` -> `stats` -> targeted `show`/`update`.
- Batch updates: export with `list-entries --output`, edit, run `import --dry-run`, then `import`.
- Cleanup: after `delete`, run checks from Section 4.4 to confirm no dangling references.

### 4.2 `query.py` (filtering and search)

```bash
python3 aspects/scripts/query.py aspects/projects/<project_name>/ASPECTS.json \
  [--min-importance FLOAT] [--max-importance FLOAT] [--sort-by FIELD] \
  [--limit N] [--tag TAG ...] [--any-tag TAG ...] [--contains SUBSTRING ...] \
  [--section <slug|id>] [--print-sources] [--json]
```

- `--min-importance`, `--max-importance` - inclusive range filter.
- `--sort-by` - `importance`, `lastUpdated`, `slug`, or other fields.
- `--limit` - maximum number of results.
- `--tag` / `--any-tag` - strict or loose tag matching.
- `--contains` - substring search (repeatable).
- `--section` - limit to a section by slug or `sectionId`.
- `--print-sources` - show paths and sha256.
- `--json` - machine output for post-processing.

Common scenarios:

- Critical aspects: `python3 aspects/scripts/query.py ... --min-importance 0.8 --sort-by importance --limit 20`.
- Duplicate search: `python3 aspects/scripts/query.py ... --tag automation --contains pipeline`.
- Freshness check: `python3 aspects/scripts/query.py ... --section infrastructure --sort-by lastUpdated --limit 5 --print-sources`.

### 4.3 `tags_manager.py` (tag catalog)

```bash
python3 aspects/scripts/tags_manager.py \
  --tags-path aspects/projects/<project_name>/ASPECTS.tags.json \
  [--aspects-path aspects/projects/<project_name>/ASPECTS.json] <command>
```

- `counts` - show tag frequencies in `ASPECTS.json`.
- `sync-counts` - recompute and update `number_of_references` (use `--dry-run` to preview).
- Without `--aspects-path`, the default is the sibling `ASPECTS.json`.

Add `--tags-catalog aspects/projects/<project_name>/ASPECTS.tags.json` to `adi.py` so it uses cached tag counts.

### 4.4 Mandatory checks

```bash
python3 -m json.tool --no-ensure-ascii aspects/projects/<project_name>/ASPECTS.json
python3 aspects/scripts/audit.py aspects/projects/<project_name>/ASPECTS.json
python3 aspects/scripts/adi.py aspects/projects/<project_name>/ASPECTS.json \
  --per-section --weighted --ignore-tag-frac 0.15 \
  --include-slug-links --include-source-links \
  --adi-threshold 5.0 --show-isolates --isolate-limit 20 \
  --tags-catalog aspects/projects/<project_name>/ASPECTS.tags.json
```

How to read results:

- `json.tool` validates JSON and canonicalizes formatting. If it fails, fix syntax first.
- `audit.py` checks structural consistency: unique `id`/`slug`, `sectionId` links, duplicate sources, and section/tag thresholds. Fix errors immediately; record warnings in `ASPECTS.status.md`.
- `adi.py` evaluates connectivity. Key fields: `nodes`, `edges`, `adi`, `isolated`. If thresholds are exceeded, record follow-ups in `ASPECTS.status.md`.

Before publishing changes, save the check output (stdout) or link to it in `ASPECTS.status.md` so others can reproduce the steps.

## 5. Tag taxonomy

1. The tag catalog lives in `aspects/projects/<project_name>/ASPECTS.tags.json` with structure `{ "tags": [...] }`. Each entry includes `tag`, `scope`, `comment`, and `number_of_references`. Use UTF-8 (no BOM), `indent=2`, `ensure_ascii=False`.
2. `number_of_references` is updated only via `tags_manager.py sync-counts`.
3. Keep `tags` sorted by `tag`. After edits, run:
   ```bash
   python3 -m json.tool --no-ensure-ascii aspects/projects/<project_name>/ASPECTS.tags.json
   python3 aspects/scripts/tags_manager.py \
     --tags-path aspects/projects/<project_name>/ASPECTS.tags.json sync-counts
   ```
4. Check for synonyms and duplicates before adding new tags. Resolve conflicts with the section owner.
5. Add new tags to the catalog before using them in aspects. Define clear boundaries in `scope` and practical meaning in `comment`.
6. Renaming, merging, or deleting tags must update the catalog, all affected aspects, and the rules.
7. For temporary tags, include a review deadline and owner in `comment`.

## 6. Regular audits

1. Audit sections daily or after every 15 new aspects. Record conclusions in `ASPECTS.status.md`.
2. Watch sections with <=6 or >25 entries; enrich or split them.
3. Monitor warning signals: >10 unique tags, repeated descriptions, growth of `slug`/`sources`.
4. `adi.py` checks from Section 4.4 are required; review ADI and isolates.
5. If thresholds are exceeded, assign an owner and plan corrective actions in the next sprint.

## 7. Mass edits

1. Prepare a JSON array or `{ "entries": [...] }` payload with valid fields.
2. Preview with `python3 aspects/scripts/aspects_manager.py import tmp/payload.json --dry-run`.
3. Apply with `python3 aspects/scripts/aspects_manager.py import tmp/payload.json [--replace] [--set-last-updated YYYY-MM-DD]`.
4. Run checks (Section 4.4).
5. Run `python3 aspects/scripts/aspects_manager.py stats` and record warnings in `ASPECTS.status.md`.

## 8. PowerShell notes (Windows)

- Set UTF-8 before running Python: `set PYTHONIOENCODING=utf-8` or `python -X utf8`.
- For one-off scripts, use `python -c "..."` or a temporary `.py` file; `python - <<'PY'` only works in bash.
- In `python -c` lines, escape double quotes with a backtick: `` `" ``.
- If `rg` struggles with special characters, switch to `rg --fixed-strings`/`--literal` or use `Select-String`.
- `Select-Object -Index` accepts only specific numbers; use a `for`/`foreach` loop for ranges.

## Appendix A. Example entry

```json
{
  "id": "aspect-responses-proxy-launcher",
  "sectionId": "section-cli",
  "slug": "responses-proxy-launcher",
  "name": "Responses proxy Node launcher",
  "description": "`codex-rs/responses-api-proxy/npm/bin/codex-responses-api-proxy.js` determines the target triple (`linux`, `darwin`, `win32` x `x64`/`arm64`), builds the path `vendor/<triple>/codex-responses-api-proxy(.exe)`, and launches the binary via `spawn` with inherited stdio. The `child.on(\"exit\")` handler mirrors the exit code or signal back to the Node process. This lets the npm responses-proxy package pick the correct artifact automatically without a shell wrapper.",
  "tags": [
    "cli",
    "node",
    "distribution"
  ],
  "sources": [
    {
      "path": "projects/Codex/codex-rs/responses-api-proxy/npm/bin/codex-responses-api-proxy.js",
      "sha256": "13d37206092330210088b1c1c329a1121a07203412b99c04f0275e81b75f17a2"
    }
  ],
  "lastUpdated": "2025-10-13",
  "importance": 0.52
}
```
