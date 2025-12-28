# ASPECTS.json status

## Summary
- Added taxonomic tags `website`, `website-*`, `support`, `versioning`; 142 entries updated (all sections `website-*`, help, versioning and `maintenance-history-prompt`), which eliminated isolates within the web documentation and aligned coherence.
- Added 50 new aspects per section `website-llms`, `website-docs`, `website-blog`, `website-install`, `website-usage`, `website-recordings`, `website-leaderboards` And `website-examples`: new provider guides, include templates and blog posts are covered (July 2023 - May 2025), tag counters are recalculated after import.
- Added 35 new aspects (YAML leaderboards, audio metadata, fixtures and smoke tests) and updated 15 entries with unit test binding (`tests/basic/test_*.py`) to models, editblock and deprecated flags.
- Re-executed `python3 aspects/scripts/tags_manager.py --tags-path aspects/projects/Aider/ASPECTS.tags.json --aspects-path aspects/projects/Aider/ASPECTS.json sync-counts`to align the counters after expansion.
- Added 50 new aspects and 7 sections (`website-troubleshooting`, `website-usage`, `website-config`, `website-install`, `website-llms`, `website-leaderboards`, `website-recordings`) to cover individual pages of the site (troubleshooting, usage, configuration, installation, LLM providers, leaderboards and posts), each entry is linked to the corresponding `.md` file with the current `sha256`.
- Updated tags for new nodes (added intersecting `commands`, `cli`, `configuration`, `automation`, `tree-sitter` etc.) and the counters are synchronized: `python3 aspects/scripts/tags_manager.py --tags-path aspects/projects/Aider/ASPECTS.tags.json --aspects-path aspects/projects/Aider/ASPECTS.json sync-counts`.
- After the current batch, the database contains 638 records; new nodes are dated `2025-10-19`.

## Checks
- `python3 -m json.tool --no-ensure-ascii aspects/projects/Aider/ASPECTS.json`
- `python3 -m json.tool --no-ensure-ascii aspects/projects/Aider/ASPECTS.tags.json`
- `python3 aspects/scripts/tags_manager.py --tags-path aspects/projects/Aider/ASPECTS.tags.json --aspects-path aspects/projects/Aider/ASPECTS.json sync-counts` (2025-10-19)
- `python3 aspects/scripts/audit.py aspects/projects/Aider/ASPECTS.json`
  - warnings: unique tags >10 (`cli`, `chat`, `commands`, `test-coverage`, `website-docs`, `website-blog`, `website-usage-guides`); sections `tree-sitter`, `benchmarks` And `website-blog` exceed 25 records.
- `python3 aspects/scripts/adi.py aspects/projects/Aider/ASPECTS.json --per-section --weighted --ignore-tag-frac 0.15 --include-slug-links --include-source-links --adi-threshold 5.0 --show-isolates --isolate-limit 20 --tags-catalog aspects/projects/Aider/ASPECTS.tags.json`
  - general metrics (2025-10-19): ADI 8.20, ADIw 28.18 (above threshold 5.0); no isolates; critical sections according to ADIw >=5.0 -- `ci` (5.21), `edit-formats` (5.09), `maintenance` (5.10), `test-coverage` (6.34). All `website-*` sections below threshold (avg_degree >=6.0).

## Observations and next steps
1. **High ADIw outside of web documentation.** `ci`, `edit-formats`, `maintenance`, `test-coverage` still above the threshold - work with tags/structure or crushing is needed.
2. **Tag coverage of website-* has been stabilized.** New tag layer (`website`, `website-*`) removed isolates; Make sure that new entries in these sections also automatically receive the appropriate tag.
3. **Benchmarks / Tree-sitter.** Sections remain >25 entries; an aggregation or division plan is required.
