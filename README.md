# Aspectics - Static memory for agents

Aspectics is a structured knowledge base for software projects. Each project is captured as a set of curated "aspects" (architecture, UX, infrastructure, workflows, metrics, and more) stored as JSON with source references and hashes.

## Repository layout

```
Aspectics - Static memory for agents
├── AGENTS.aspects.md    - rules for authoring and maintaining aspects
├── AGENTS.worker.md     - required workflow for agents
├── README.md            - repository overview and quick start
└── aspects/
    ├── projects/        - per-project knowledge bases
    └── scripts/         - CLI utilities for querying and auditing aspects
```

## Quick start

1. Requirements
   - Python 3.11+
   - `rg`, `fd`, `jq`
2. Inspect tags for a project:
   ```bash
   cat aspects/projects/<project>/aspects-tags.md
   ```
3. Query high-importance aspects:
   ```bash
   python3 aspects/scripts/query.py aspects/projects/<project>/ASPECTS.json \
     --min-importance 0.8 --sort-by importance --limit 20 --print-sources
   ```

## Core files per project

```
aspects/projects/<project>/
├── ASPECTS.json       - aspect entries
├── ASPECTS.tags.json  - tag catalog with reference counts
└── ASPECTS.status.md  - audit notes and open issues
```

## Scripts

| Script | Purpose | Example |
| --- | --- | --- |
| `query.py` | Filter aspects by importance, tags, and text | `python3 aspects/scripts/query.py aspects/projects/<project>/ASPECTS.json --min-importance 0.8` |
| `audit.py` | Validate structure (`id`, `slug`, sources) | `python3 aspects/scripts/audit.py aspects/projects/<project>/ASPECTS.json` |
| `adi.py` | Connectivity analysis (ADI, isolates) | `python3 aspects/scripts/adi.py aspects/projects/<project>/ASPECTS.json --per-section` |
| `tags_manager.py` | Tag catalog management and counts | `python3 aspects/scripts/tags_manager.py --tags-path aspects/projects/<project>/ASPECTS.tags.json --sync-counts` |
| `hash_check.py` | Recompute sha256 for sources | `python3 aspects/scripts/hash_check.py --help` |
| `aspects_manager.py` | Interactive add/update/import tooling | `python3 aspects/scripts/aspects_manager.py --help` |

## Recommended workflow

1. Read critical aspects (importance >= 0.80) before any task.
2. Update entries with verified sources and sha256 hashes.
3. Run `audit.py` and `adi.py` after modifications.
4. Record warnings and follow-ups in `ASPECTS.status.md`.

## More details

- `AGENTS.aspects.md` - structure rules, validation requirements, and tagging policy.
- `AGENTS.worker.md` - mandatory workflow for agents.

## Contributing

See `CONTRIBUTING.md`.

## License

See `LICENSE`.
