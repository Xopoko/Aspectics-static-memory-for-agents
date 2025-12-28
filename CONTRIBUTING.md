# Contributing

Thanks for your interest in improving Aspectics.

## Quick start

1. Read the policies in `AGENTS.aspects.md` and the workflow in `AGENTS.worker.md`.
2. Work on a branch and keep changes scoped and reviewable.
3. Run the checks listed below before opening a pull request.

## Working with aspects

- Each aspect entry must cite at least one source file as `{ path, sha256 }`.
- Use stable `id`, `slug`, and `sectionId` values.
- Keep `importance` in the `0.0-1.0` range and explain high-importance entries.
- Update `lastUpdated` whenever an entry changes.

## Required checks

```bash
python3 -m json.tool --no-ensure-ascii aspects/projects/<project>/ASPECTS.json
python3 aspects/scripts/audit.py aspects/projects/<project>/ASPECTS.json
python3 aspects/scripts/adi.py aspects/projects/<project>/ASPECTS.json \
  --per-section --weighted --ignore-tag-frac 0.15 \
  --include-slug-links --include-source-links \
  --adi-threshold 5.0 --show-isolates --isolate-limit 20 \
  --tags-catalog aspects/projects/<project>/ASPECTS.tags.json
```

## Pull request checklist

- [ ] The change follows the rules in `AGENTS.aspects.md`.
- [ ] All updated entries have valid `sources` and `lastUpdated`.
- [ ] `audit.py` and `adi.py` pass or warnings are documented in `ASPECTS.status.md`.
- [ ] The change is described clearly in the PR summary.
