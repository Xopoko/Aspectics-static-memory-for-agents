# Status

# 2025-10-16

- Introduced regression-focused sections `tui-diff-tests` (20 entries) and `tui-list-tests` (24 entries) documenting the diff view matrix, width/height sweeps, offset loops, and the experimental list movement/viewport suites. Added 44 new aspects across those sections to surface individual scenarios (matrix behaviours, width caps, keymap mutations, append/prepend stability) so the golden-based coverage is easy to audit.
- Refreshed five `tui-experiments` entries to tag them with the new `tests` taxonomy key and cross-reference how their fixtures seed the regression sections. Updated `chat-message-toolcall-options` to capture the newer permission flags so automation coverage stays complete. The taxonomy now includes a `tests` tag in `ASPECTS.tags.json`.
- Total catalogue now at 32 sections / 444 entries.
- Validation commands executed:
  - `python3 -m json.tool --no-ensure-ascii aspects/projects/Crush/ASPECTS.json`
  - `python3 aspects/scripts/audit.py aspects/projects/Crush/ASPECTS.json`
  - `python3 aspects/scripts/adi.py aspects/projects/Crush/ASPECTS.json --per-section --weighted --ignore-tag-frac 0.15 --adi-threshold 5.0 --show-isolates --isolate-limit 20 --tags-catalog aspects/projects/Crush/ASPECTS.tags.json`
  - `python3 aspects/scripts/tags_manager.py --tags-path aspects/projects/Crush/ASPECTS.tags.json --aspects-path aspects/projects/Crush/ASPECTS.json sync-counts`
- Audit warnings unchanged for high unique-tag sections (`architecture`, `config`, `tui`, `llm`, `tools`, `cli`) and low-count `tui-experiments`/`chat-automation`; plan remains to backfill automation coverage in a future pass.
- ADI still reports isolates inside `messaging` (12 entries focused on metadata structs) plus `session-subsession` and `mcp-status-block`. Schedule a retag/cross-link effort to connect message schema aspects with the new regression entries so ADIw drops below threshold.

# 2025-10-21

- Added 26 regression-focused aspects covering internal tests for config merges/LSP defaults, csync maps and slices, filesystem glob/ignore/lookup helpers, home path coercion, prompt path expansion, OpenAI streaming retries, grep tool caching, shell cancellation/perf benchmarks, and experimental TUI widgets. The additions raise coverage in previously under-weighted sections (`concurrency`, `filesystem`, `llm-prompts`, `lsp`, `shell`, `observability`) and surface Taskfile automation for diffview goldens.
- Introduced new sections `Chat Input`, `Chat Output`, and `Chat Automation`, moving 24 entries out of `tui-chat` to reduce tag churn while keeping seven general chat aspects in place. Added `TUI Experiments` and relocated diffview/list experimental knowledge there so the main widgets/components sections stay focused on production surfaces.
- Synced tag catalog counts after the imports via `python3 aspects/scripts/tags_manager.py --tags-path aspects/projects/Crush/ASPECTS.tags.json --aspects-path aspects/projects/Crush/ASPECTS.json sync-counts`.
- Validation commands executed:
  - `python3 -m json.tool --no-ensure-ascii aspects/projects/Crush/ASPECTS.json`
  - `python3 aspects/scripts/audit.py aspects/projects/Crush/ASPECTS.json`
  - `python3 aspects/scripts/adi.py aspects/projects/Crush/ASPECTS.json --per-section --weighted --ignore-tag-frac 0.15 --adi-threshold 5.0 --show-isolates --isolate-limit 20 --tags-catalog aspects/projects/Crush/ASPECTS.tags.json` *(dropped the slug/source link flags because the enriched graph now times out with them)*
  - `python3 aspects/scripts/tags_manager.py --tags-path aspects/projects/Crush/ASPECTS.tags.json --aspects-path aspects/projects/Crush/ASPECTS.json sync-counts`
- Outstanding signals:
  - Audit flagged the freshly split `chat-automation` (6 entries) and `tui-experiments` (5 entries) as small; plan follow-up content once we document remaining permission automation flows and additional experimental widgets.
  - ADI still reports isolates clustered in `messaging` (12) and `sessions` (2) plus `tui`'s `mcp-status-block`; schedule retagging/cross-linking of message metadata aspects and session summaries to bring them back into the graph.
- Section/entry totals now at 30 sections / 400 entries.

## 2025-10-20

- Added 18 new `llm` aspects detailing coder-agent internals (title streaming, prompt queue handling, tool execution/cancellation, MCP refresh, provider event mapping, token accounting, panic guards) plus one `permissions` entry covering the concurrent request test suite. The `llm` section now holds 28 entries; permissions ticked up to 9.
- Refreshed 36 existing aspects across `config`, `tui`, `tui-chat`, `tui-styles`, and `devx`, adding resolver/loader test coverage, cross-references to agent and shell services, and extra tags (`shell`, `filesystem`, `agent`, `session`, `styles`, `pubsub`) to improve connectivity for previously sparse items such as `chat-queue-pill`, `mcp-status-block`, and theme/primitives.
- Synced tag catalog after imports via `python3 aspects/scripts/tags_manager.py --tags-path aspects/projects/Crush/ASPECTS.tags.json --aspects-path aspects/projects/Crush/ASPECTS.json sync-counts`.
- Validation commands executed after the edits:
  - `python3 -m json.tool --no-ensure-ascii aspects/projects/Crush/ASPECTS.json`
  - `python3 aspects/scripts/audit.py aspects/projects/Crush/ASPECTS.json`
  - `python3 aspects/scripts/adi.py aspects/projects/Crush/ASPECTS.json --per-section --weighted --ignore-tag-frac 0.15 --include-slug-links --include-source-links --adi-threshold 5.0 --show-isolates --isolate-limit 20 --tags-catalog aspects/projects/Crush/ASPECTS.tags.json`
- ADI highlights: overall ADIw = 20.59 (threshold 5.0) with isolates still in legacy `devx` entries (`crush-dev-guide`, `cspell-dictionary`, `readme-orientation`) and `tui/mcp-status-block`. Follow-up: fold those historical docs into richer sections or add cross-links so they stop skewing connectivity metrics.
- Audit warnings unchanged: high unique-tag counts in `architecture`, `config`, `tui`, `llm`, `tools`, `cli`; `tui-chat` now 33 entries (>25) and `llm` reached 28 (>25). Future cleanup should merge overlapping tags or break out subsections if the hot spots keep growing.

- Added 50 aspects focused on under-filled sections: 13 new `llm-providers` entries detailing Anthropic/OpenAI/Gemini/Azure/Bedrock/Vertex behaviours, 7 deeper dives into permission dialog rendering, 5 command palette updates for context-aware actions, 6 messaging helpers (roles, accessors, binary handling), 5 shell primitives (env/locking APIs), 4 pubsub concurrency notes, 3 session data aspects, and 7 diffview/filterable widget internals. Section counts now reinforce provider/TUI coverage without introducing new tags.
- Synced tag catalog counts after imports; no new taxonomy keys were introduced.
- Audit warnings persist for high tag counts (`architecture`, `config`, `tui`, `tools`, `cli`) and the large `tui-chat` section; overall ADIw remains above threshold with legacy isolates (`crush-dev-guide`, `cspell-dictionary`, `readme-orientation`, `mcp-status-block`) requiring future cross-linking.
- Validation commands:
  - `python3 -m json.tool --no-ensure-ascii aspects/projects/Crush/ASPECTS.json`
  - `python3 aspects/scripts/audit.py aspects/projects/Crush/ASPECTS.json`
  - `python3 aspects/scripts/adi.py aspects/projects/Crush/ASPECTS.json --per-section --weighted --ignore-tag-frac 0.15 --include-slug-links --include-source-links --adi-threshold 5.0 --show-isolates --isolate-limit 20 --tags-catalog aspects/projects/Crush/ASPECTS.tags.json`
  - `python3 aspects/scripts/tags_manager.py --tags-path aspects/projects/Crush/ASPECTS.tags.json --aspects-path aspects/projects/Crush/ASPECTS.json sync-counts`

## 2025-10-18

- Added 22 knowledge entries covering automation configs (Dependabot, labeler, CLA workflow, GoReleaser), developer docs (`CRUSH.md`, `README.md`, `cspell.json`), default configuration artifacts (`crush.json`, `schema.json`, `sqlc.yaml`), new TUI onboarding/styling widgets (theme manager, input/file picker/diff palettes, splash autosubmit, list caching), and provider-specific prompt guardrails for Anthropic and Gemini.
- Refreshed 18 existing tool/prompt aspects to link their markdown playbooks, extending descriptions for Bash, filesystem helpers (glob/grep/ls/view/write), Sourcegraph, diagnostics, and provider templates so the runtime instructions and the LLM guidance stay aligned; relocated `provider-client` under `llm-providers` and retagged config/style/devx entries to share `schema`, `cli`, and `styles` tags for better connectivity.
- `python3 -m json.tool --no-ensure-ascii aspects/projects/Crush/ASPECTS.json`, `python3 aspects/scripts/audit.py aspects/projects/Crush/ASPECTS.json`, `python3 aspects/scripts/adi.py aspects/projects/Crush/ASPECTS.json --per-section --weighted --ignore-tag-frac 0.15 --adi-threshold 5.0 --show-isolates --isolate-limit 20 --tags-catalog aspects/projects/Crush/ASPECTS.tags.json`, and `python3 aspects/scripts/tags_manager.py --tags-path aspects/projects/Crush/ASPECTS.tags.json --aspects-path aspects/projects/Crush/ASPECTS.json sync-counts` all ran after the edits (ADI executed without the optional source/link flags so it could complete within the time limit).
- Outstanding ADI isolates now concentrate in legacy sections (`config`, `devx`, `messaging`, `tui-commands`, some CLI/tooling entries); follow-up needed to retag or merge those historical aspects so they connect to broader knowledge (e.g., cross-link CLI utilities, messaging data models, and command palette docs).
- Section warnings remain for over-tagged/config/chat areas and low-count prompt/provider sections; consider adding provider-specific prompt summaries or merging redundant tags to reduce `>10` tag alerts.

## 2025-10-17

- Added six knowledge sections (`tui-dialogs`, `tui-components`, `tui-widgets`, `tui-styles`, `llm-prompts`, `llm-providers`) and 47 new aspects spanning TUI overlays, experimental widgets, styling primitives, prompt templates, provider adapters, and sqlc-generated database accessors.
- Introduced taxonomy tags (`components`, `dialogs`, `widgets`, `prompts`, `providers`, `styles`) and retagged existing isolates (`logo-gradient-renderer`, `status-help-bar`, `chat-queue-pill`, `message-attachments-struct`) to improve cross-linking and reduce ADI isolates from 30 → 6.
- Expanded tooling coverage with LLM file timestamp tracking, ripgrep discovery notes, safe command registry, and captured attachments across chat/file picker flows.
- Remaining isolates (`charmtone-theme`, `chroma-theme`, `markdown-renderer`, `style-icons`, `chat-queue-pill`, `config-json-merge`) need follow-up links to broader style/config knowledge before we tackle the lingering high ADIw.

### Validation log

```
$ python3 -m json.tool --no-ensure-ascii aspects/projects/Crush/ASPECTS.json
$ python3 aspects/scripts/audit.py aspects/projects/Crush/ASPECTS.json
Sections: 26 | Entries: 282

Warnings:
  - section section-architecture uses 14 unique tags (>10)
  - section section-config uses 11 unique tags (>10)
  - section section-tui uses 12 unique tags (>10)
  - section section-tui-chat has 33 entries (>25)
  - section section-tui-chat uses 14 unique tags (>10)
  - section section-tui-onboarding has 6 entries (<=6)
  - section section-tools uses 15 unique tags (>10)
  - section section-cli uses 11 unique tags (>10)
  - section section-tui-styles has 5 entries (<=6)
  - section section-llm-prompts has 6 entries (<=6)
  - section section-llm-providers has 6 entries (<=6)

$ python3 aspects/scripts/adi.py aspects/projects/Crush/ASPECTS.json --per-section --weighted --ignore-tag-frac 0.15 --include-slug-links --include-source-links --adi-threshold 5.0 --show-isolates --isolate-limit 20 --tags-catalog aspects/projects/Crush/ASPECTS.tags.json
[adi] Warning: tag 'tools' has no cached count in catalog; run tags_manager.py sync-counts.
Overall: aspects=282, edges=3644, avg_degree=25.84, ADI=10.91, isolated=6, weighted_avg_degree=10.39, ADIw=27.14
!! Overall ADIw 27.14 >= threshold 5.00
  Isolated aspects:
    - charmtone-theme
    - chat-queue-pill
    - chroma-theme
    - config-json-merge
    - markdown-renderer
    - style-icons

Per section:
  architecture: aspects=9, edges=36, avg_degree=8.00, ADI=1.12, isolated=0, weighted_avg_degree=8.70, ADIw=1.03
  automation: aspects=8, edges=28, avg_degree=7.00, ADI=1.14, isolated=0, weighted_avg_degree=2.11, ADIw=3.80
  cli: aspects=11, edges=35, avg_degree=6.36, ADI=1.73, isolated=0, weighted_avg_degree=3.63, ADIw=3.03
  concurrency: aspects=8, edges=28, avg_degree=7.00, ADI=1.14, isolated=0, weighted_avg_degree=2.46, ADIw=3.25
  config: aspects=14, edges=31, avg_degree=4.43, ADI=3.16, isolated=1, weighted_avg_degree=4.27, ADIw=3.28
    * isolated: config-json-merge
  database: aspects=19, edges=171, avg_degree=18.00, ADI=1.06, isolated=0, weighted_avg_degree=6.69, ADIw=2.84
  devx: aspects=9, edges=12, avg_degree=2.67, ADI=3.38, isolated=0, weighted_avg_degree=3.10, ADIw=2.90
  filesystem: aspects=10, edges=45, avg_degree=9.00, ADI=1.11, isolated=0, weighted_avg_degree=3.86, ADIw=2.59
  llm: aspects=11, edges=38, avg_degree=6.91, ADI=1.59, isolated=0, weighted_avg_degree=3.96, ADIw=2.78
  llm-prompts: aspects=6, edges=15, avg_degree=5.00, ADI=1.20, isolated=0, weighted_avg_degree=1.99, ADIw=3.02
  llm-providers: aspects=6, edges=15, avg_degree=5.00, ADI=1.20, isolated=0, weighted_avg_degree=1.78, ADIw=3.37
  lsp: aspects=10, edges=45, avg_degree=9.00, ADI=1.11, isolated=0, weighted_avg_degree=4.72, ADIw=2.12
  messaging: aspects=9, edges=23, avg_degree=5.11, ADI=1.76, isolated=0, weighted_avg_degree=4.93, ADIw=1.83
  observability: aspects=12, edges=66, avg_degree=11.00, ADI=1.09, isolated=0, weighted_avg_degree=6.65, ADIw=1.80
  permissions: aspects=8, edges=28, avg_degree=7.00, ADI=1.14, isolated=0, weighted_avg_degree=11.13, ADIw=0.72
  sessions: aspects=8, edges=16, avg_degree=4.00, ADI=2.00, isolated=0, weighted_avg_degree=3.74, ADIw=2.14
  shell: aspects=8, edges=28, avg_degree=7.00, ADI=1.14, isolated=0, weighted_avg_degree=7.42, ADIw=1.08
  tools: aspects=19, edges=142, avg_degree=14.95, ADI=1.27, isolated=0, weighted_avg_degree=5.99, ADIw=3.17
  tui: aspects=20, edges=41, avg_degree=4.10, ADI=4.88, isolated=1, weighted_avg_degree=3.72, ADIw=5.37
    * isolated: mcp-status-block
  tui-chat: aspects=33, edges=110, avg_degree=6.67, ADI=4.95, isolated=2, weighted_avg_degree=5.67, ADIw=5.82
    * isolated: chat-layout
    * isolated: chat-queue-pill
  tui-commands: aspects=8, edges=17, avg_degree=4.25, ADI=1.88, isolated=0, weighted_avg_degree=4.30, ADIw=1.86
  tui-components: aspects=10, edges=45, avg_degree=9.00, ADI=1.11, isolated=0, weighted_avg_degree=2.65, ADIw=3.77
  tui-dialogs: aspects=8, edges=28, avg_degree=7.00, ADI=1.14, isolated=0, weighted_avg_degree=2.21, ADIw=3.62
  tui-onboarding: aspects=6, edges=15, avg_degree=5.00, ADI=1.20, isolated=0, weighted_avg_degree=2.45, ADIw=2.45

$ python3 aspects/scripts/tags_manager.py --tags-path aspects/projects/Crush/ASPECTS.tags.json --aspects-path aspects/projects/Crush/ASPECTS.json sync-counts
Updated 5 tag entries (catalog: aspects/projects/Crush/ASPECTS.tags.json, aspects: aspects/projects/Crush/ASPECTS.json)
```

### Follow-ups

- Add cross-links for the remaining isolates (palette-focused `styles` entries, `chat-queue-pill`, `config-json-merge`) or fold them into richer sections so ADIw declines toward the 5.0 target.
- Address the lingering “tag >10” warnings by consolidating overlapping TUI/config labels once the new sections settle.
- Investigate the `tools` tag cache warning in ADI (despite sync) and update scripts if the cache key logic needs an adjustment.

## 2025-10-16

- Split the TUI knowledge base into `tui`, `tui-chat`, `tui-commands`, and the new `tui-onboarding` section, relocating 24 chat/command entries earlier in the day and adding 40 more aspects covering chat runtime behaviour, onboarding flows, reusable list widgets, LLM telemetry, and messaging attachments.
- Expanded chat coverage with mouse selection/copy UX, assistant/tool refresh pipelines, prompt queue sizing, and header diagnostics, while onboarding now documents splash keymaps, API key verification UI, and provider model pickers used during first-run setup.
- Broadened the general TUI section with tool preview renderers, MCP status tiles, the status/help bar, and filterable list internals; added matching config and LLM knowledge (`config.Merge`, agent telemetry/error sentinels, MCP tool registry) plus the messaging attachment struct.
- Introduced the `chat` taxonomy tag, retagged 20 chat entries, and re-synced catalogue counts; new isolates appeared (`logo-gradient-renderer`, `status-help-bar`, `message-attachments-struct`, `chat-queue-pill`) that need linking.

### Validation log

```
$ python3 -m json.tool --no-ensure-ascii aspects/projects/Crush/ASPECTS.json
$ python3 aspects/scripts/audit.py aspects/projects/Crush/ASPECTS.json
Sections: 20 | Entries: 234

Warnings:
  - section section-architecture uses 14 unique tags (>10)
  - section section-config uses 11 unique tags (>10)
  - section section-tui uses 11 unique tags (>10)
  - section section-tui-chat has 33 entries (>25)
  - section section-tui-chat uses 14 unique tags (>10)
  - section section-tui-onboarding has 6 entries (<=6)
  - section section-tools uses 14 unique tags (>10)
  - section section-cli uses 11 unique tags (>10)

$ python3 aspects/scripts/adi.py aspects/projects/Crush/ASPECTS.json --per-section --weighted --ignore-tag-frac 0.15 --include-slug-links --include-source-links --adi-threshold 5.0 --show-isolates --isolate-limit 20 --tags-catalog aspects/projects/Crush/ASPECTS.tags.json
Overall: aspects=234, edges=2431, avg_degree=20.78, ADI=11.26, isolated=4, weighted_avg_degree=10.20, ADIw=22.95
!! Overall ADIw 22.95 >= threshold 5.00
  Isolated aspects:
    - chat-queue-pill
    - logo-gradient-renderer
    - message-attachments-struct
    - status-help-bar

Per section:
  architecture: aspects=9, edges=36, avg_degree=8.00, ADI=1.12, isolated=0, weighted_avg_degree=8.81, ADIw=1.02
  automation: aspects=8, edges=28, avg_degree=7.00, ADI=1.14, isolated=0, weighted_avg_degree=2.11, ADIw=3.80
  cli: aspects=11, edges=39, avg_degree=7.09, ADI=1.55, isolated=0, weighted_avg_degree=4.12, ADIw=2.67
  concurrency: aspects=8, edges=28, avg_degree=7.00, ADI=1.14, isolated=0, weighted_avg_degree=2.46, ADIw=3.25
  config: aspects=14, edges=91, avg_degree=13.00, ADI=1.08, isolated=0, weighted_avg_degree=6.78, ADIw=2.06
  database: aspects=16, edges=120, avg_degree=15.00, ADI=1.07, isolated=0, weighted_avg_degree=6.67, ADIw=2.40
  devx: aspects=9, edges=12, avg_degree=2.67, ADI=3.38, isolated=0, weighted_avg_degree=2.89, ADIw=3.12
  filesystem: aspects=10, edges=21, avg_degree=4.20, ADI=2.38, isolated=0, weighted_avg_degree=2.33, ADIw=4.30
  llm: aspects=11, edges=40, avg_degree=7.27, ADI=1.51, isolated=0, weighted_avg_degree=4.10, ADIw=2.68
  lsp: aspects=10, edges=45, avg_degree=9.00, ADI=1.11, isolated=0, weighted_avg_degree=4.61, ADIw=2.17
  messaging: aspects=9, edges=22, avg_degree=4.89, ADI=1.84, isolated=1, weighted_avg_degree=4.89, ADIw=1.84
    * isolated: message-attachments-struct
  observability: aspects=12, edges=66, avg_degree=11.00, ADI=1.09, isolated=0, weighted_avg_degree=6.65, ADIw=1.80
  permissions: aspects=8, edges=28, avg_degree=7.00, ADI=1.14, isolated=0, weighted_avg_degree=9.76, ADIw=0.82
  sessions: aspects=8, edges=16, avg_degree=4.00, ADI=2.00, isolated=0, weighted_avg_degree=3.74, ADIw=2.14
  shell: aspects=8, edges=28, avg_degree=7.00, ADI=1.14, isolated=0, weighted_avg_degree=7.27, ADIw=1.10
  tools: aspects=16, edges=70, avg_degree=8.75, ADI=1.83, isolated=0, weighted_avg_degree=3.76, ADIw=4.26
  tui: aspects=20, edges=38, avg_degree=3.80, ADI=5.26, isolated=3, weighted_avg_degree=3.62, ADIw=5.52
    * isolated: logo-gradient-renderer
    * isolated: mcp-status-block
    * isolated: status-help-bar
  tui-chat: aspects=33, edges=101, avg_degree=6.12, ADI=5.39, isolated=2, weighted_avg_degree=5.55, ADIw=5.94
    * isolated: chat-layout
    * isolated: chat-queue-pill
  tui-commands: aspects=8, edges=17, avg_degree=4.25, ADI=1.88, isolated=0, weighted_avg_degree=4.25, ADIw=1.88
  tui-onboarding: aspects=6, edges=15, avg_degree=5.00, ADI=1.20, isolated=0, weighted_avg_degree=2.57, ADIw=2.33

Sections exceeding threshold:
  - tui: ADIw=5.52, avg_degree=3.80, isolated=3
  - tui-chat: ADIw=5.94, avg_degree=6.12, isolated=2

$ python3 aspects/scripts/tags_manager.py --tags-path aspects/projects/Crush/ASPECTS.tags.json --aspects-path aspects/projects/Crush/ASPECTS.json sync-counts
Updated 16 tag entries (catalog: aspects/projects/Crush/ASPECTS.tags.json, aspects: aspects/projects/Crush/ASPECTS.json)
```

### Follow-ups

- Overall ADIw climbed to 22.95; add cross-links for the new isolates (queue pill, status/help bar, logo renderer, message attachments) and tighten the TUI graph to bring the weighted score down.
- Address high-tag warnings (architecture, config, tools, cli, tui, tui-chat) in the next taxonomy sweep by consolidating overlapping labels.
- Plan dedicated work to connect `logo-gradient-renderer`, `status-help-bar`, and `message-attachments-struct` with related observability/UI knowledge, and reassess splitting `tui-chat` if the section continues to grow.

## 2025-10-15

- Expanded the Crush knowledge base to 12 sections and 65 entries, introducing Language Servers and Concurrency Utilities alongside deeper coverage for automation, permissions, and observability.
- Documented LSP lifecycle management, csync primitives, eight additional agent tools, six CI/CD workflows, session helpers, provider streaming, and CLI permission modes to close prior gaps.

### Validation log

```
$ python3 -m json.tool --no-ensure-ascii aspects/projects/Crush/ASPECTS.json
$ python3 aspects/scripts/audit.py aspects/projects/Crush/ASPECTS.json
Sections: 12 | Entries: 65

Warnings:
  - section section-architecture has 3 entries (<=6)
  - section section-config has 5 entries (<=6)
  - section section-sessions has 6 entries (<=6)
  - section section-tui has 4 entries (<=6)
  - section section-llm has 5 entries (<=6)
  - section section-permissions has 3 entries (<=6)
  - section section-cli has 4 entries (<=6)
  - section section-observability has 3 entries (<=6)
  - section section-lsp has 6 entries (<=6)
  - section section-concurrency has 3 entries (<=6)

$ python3 aspects/scripts/adi.py aspects/projects/Crush/ASPECTS.json --per-section --weighted --ignore-tag-frac 0.15 --include-slug-links --include-source-links --adi-threshold 5.0 --show-isolates --isolate-limit 20 --tags-catalog aspects/projects/Crush/ASPECTS.tags.json
Overall: aspects=65, edges=262, avg_degree=8.06, ADI=8.06, isolated=0, weighted_avg_degree=4.82, ADIw=13.50
!! Overall ADIw 13.50 >= threshold 5.00

Per section:
  architecture: aspects=3, edges=3, avg_degree=2.00, ADI=1.50, isolated=0, weighted_avg_degree=1.38, ADIw=2.18
  automation: aspects=8, edges=28, avg_degree=7.00, ADI=1.14, isolated=0, weighted_avg_degree=2.11, ADIw=3.80
  cli: aspects=4, edges=6, avg_degree=3.00, ADI=1.33, isolated=0, weighted_avg_degree=0.95, ADIw=4.23
  concurrency: aspects=3, edges=3, avg_degree=2.00, ADI=1.50, isolated=0, weighted_avg_degree=0.86, ADIw=3.48
  config: aspects=5, edges=10, avg_degree=4.00, ADI=1.25, isolated=0, weighted_avg_degree=2.00, ADIw=2.49
  llm: aspects=5, edges=7, avg_degree=2.80, ADI=1.79, isolated=0, weighted_avg_degree=2.18, ADIw=2.29
  lsp: aspects=6, edges=15, avg_degree=5.00, ADI=1.20, isolated=0, weighted_avg_degree=2.58, ADIw=2.33
  observability: aspects=3, edges=3, avg_degree=2.00, ADI=1.50, isolated=0, weighted_avg_degree=0.71, ADIw=4.21
  permissions: aspects=3, edges=3, avg_degree=2.00, ADI=1.50, isolated=0, weighted_avg_degree=2.21, ADIw=1.36
  sessions: aspects=6, edges=7, avg_degree=2.33, ADI=2.57, isolated=0, weighted_avg_degree=2.19, ADIw=2.74
  tools: aspects=15, edges=17, avg_degree=2.27, ADI=6.62, isolated=0, weighted_avg_degree=2.00, ADIw=7.50
  tui: aspects=4, edges=3, avg_degree=1.50, ADI=2.67, isolated=0, weighted_avg_degree=1.50, ADIw=2.67

Sections exceeding threshold:
  - tools: ADIw=7.50, avg_degree=2.27, isolated=0

$ python3 aspects/scripts/tags_manager.py --tags-path aspects/projects/Crush/ASPECTS.tags.json --aspects-path aspects/projects/Crush/ASPECTS.json sync-counts
Updated 2 tag entries (catalog: aspects/projects/Crush/ASPECTS.tags.json, aspects: aspects/projects/Crush/ASPECTS.json)
```

### Follow-ups

- Reduce tools-section ADIw (7.50) by adding further bridge aspects or references that relate file-permission utilities with task-automation tools.
- Continue adding cross-links that connect TUI overlays with session or tool flows to push the overall ADIw (13.50) below threshold.
