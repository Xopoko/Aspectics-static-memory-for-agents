# Aspect database status - 2025-10-20

## Updates
- Added 50 new aspects (now 649) for the interactive UI: fixed AsciiArt logos, RawMarkdownIndicator, TodoListDisplay, EnumSelector, unicode-aware `useTextBuffer` And `handleVimAction`, as well as hooks for loading indicator, phrase cycler, theme/settings/model/memory commands.
- We expanded the base of utilities and configurations: comment-json sync-by-omission, customDeepMerge, resolvePath, package-json loader, updateEventEmitter/appEvents, assume/checkExhaustive, semantic-colors and color-utils are described.
- Documented operational automation: lint runner, full patch release chain and ripgrep downloader; section created `section-ide-companion` with aspects of IDE Companion (activation, DiffManager, IDEServer, OpenFilesManager, release tooling, esbuild).
- Updated tag counters `ASPECTS.tags.json` through `tags_manager.py sync-counts`.

## Validation
- `python3 -m json.tool --no-ensure-ascii aspects/projects/GeminiCLI/ASPECTS.json`
- `python3 -m json.tool --no-ensure-ascii aspects/projects/GeminiCLI/ASPECTS.tags.json`
- `python3 aspects/scripts/audit.py aspects/projects/GeminiCLI/ASPECTS.json`
- `python3 aspects/scripts/adi.py aspects/projects/GeminiCLI/ASPECTS.json --per-section --weighted --ignore-tag-frac 0.15 --include-slug-links --include-source-links --adi-threshold 5.0 --show-isolates --isolate-limit 20 --tags-catalog aspects/projects/GeminiCLI/ASPECTS.tags.json`

## ADI Metrics
- Overall ADIw = 45.87 (threshold 5.0); global isolates: `app-events-emitter`, `assume-exhaustive`, `lerp-utility`, `lru-cache`, `raw-markdown-indicator`, `safe-literal-replace`, `slash-command-parser`, `terminal-serializer`, `ui-text-constants`.
- Critical sections according to ADIw: `ui-contexts` (84.90), `ui-utils` (27.21), `core-data-utils` (40.25), `core-utils` (37.07), `core` (16.15; isolated `core-index-export`, `core-logger`, `core-package-exports`, `fallback-types`), `core-noninteractive` (6.92), `cli-ui` (7.14), `cli-commands` (5.75), `cli-integration-commands` (6.30), `ui-hooks-completion` (5.09), `core-fs-utils` (5.39), `tools` (5.02).
- Audit: `section-ui` increased to 27 records (>25), `section-ide-companion` uses 11 unique tags (>10); previous deviations remain in `section-tools` (31 entries, 14 tags) and `section-security` (26/13), as well as in sections with rich taxonomy (`startup`, `ui-*`, `agents`, `integrations`, `telemetry`, `a2a-server`). Remain compact `config-versions`, `ui-hooks-observability`, `core-noninteractive`.

## Next steps
1. Link new insulators (`raw-markdown-indicator`, `ui-text-constants`, `mcp-status-view`, `app-events-emitter`, `assume-exhaustive`, `lerp-utility`, `core-package-exports`) with consuming components or neighboring aspects.
2. Continue working with historical isolates (`core-data-utils`, `core-utils`, `core`), add links to use cases or redistribute entries into application sections.
3. Prepare a partition plan `section-ui` (27 entries) and clarify taxonomy `section-ide-companion` (11 unique tags): Group banners/components and highlight companion blocks to reduce ADIw.
4. Keep crushing in plans `section-tools` And `section-security`, as well as revision of tags in sections with >10 unique tags (`tools`, `security`, `telemetry`, `integrations`, `agents`, `startup`, `ui-*`, `a2a-server`).
