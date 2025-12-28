# AGENTS.worker.md

Use aspects from `aspects/projects/<project_name>/ASPECTS.json` as the source of truth for the project. They are curated, verifiable, and designed to prevent guesswork. Read them early and often.

## Quick start

1. Review available tags:
   ```bash
   cat aspects/projects/<project_name>/aspects-tags.md
   ```
2. Load critical aspects:
   ```bash
   python3 aspects/scripts/query.py aspects/projects/<project_name>/ASPECTS.json \
     --min-importance 0.8 --sort-by importance --limit 20
   ```

## Importance scale

- `0.80-1.00` - critical foundation. Read before any task.
- `0.60-0.79` - core domain knowledge.
- `0.30-0.59` - useful context as needed.
- `0.00-0.29` - reference or historical notes.
- If you set `importance >= 0.8`, explain why in the description.

## Workflow

1. Load aspects with `importance >= 0.80` before starting work.
2. Review the tag catalog to understand available themes.
3. Analyze the task and the repository context.
4. Identify which aspects are relevant.
5. Plan the work based on those aspects (request more if needed).
6. Execute the task, re-checking aspects when in doubt.

## Quick queries (`query.py`)

- Filter by importance: `--min-importance 0.8 --sort-by importance`.
- Tag search: `--tag` requires all tags; `--any-tag` matches any (example: `--tag cli --any-tag automation`).
- Keyword search: repeat `--contains` for multiple substrings.
- Section filtering: `--section developer-utilities-and-automation --limit 5`.
- Include sources: `--print-sources`.
- JSON output: `--json` for automation and post-processing.
