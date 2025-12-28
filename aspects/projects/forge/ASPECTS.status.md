# Forge ASPECTS status (2025-10-27)

## Summary
- Discovery pass on 2025-10-27 reran the tracked `.rs/.yaml/.yml/.toml/.json/.sh` coverage check (`python3 - <<'PY'` with `git ls-files projects/forge`) and confirmed zero missing sources; section counts remain ≥8 entries and validation (`json.tool`/`audit.py`/`adi.py`) still reports ADIw 35.08 with Domain, Services, and Tool sections over threshold, so no new aspects, tag revisions, or structural updates were necessary this cycle.
- Discovery sweep on 2025-10-27 reran the tracked extension coverage script (`python3 - <<'PY'`) listing `git ls-files projects/forge` for `.rs/.yaml/.yml/.toml/.json/.sh`, received `No missing coverage for tracked extensions.` so no new or updated aspects were required this pass.
- Discovery verification on 2025-10-27 reran the tracked `.rs/.yaml/.yml/.toml/.json/.sh` coverage check via a `git ls-files`-backed Python script, confirming zero missing sources so no new aspects, tag updates, or structural changes are required this cycle.
- Discovery check on 2025-10-27 reran coverage scripts (`python3 - <<'PY'`) comparing tracked `.rs/.yaml/.yml/.toml/.json/.sh` sources against `ASPECTS.json` entries (outputs: `0 rs files missing coverage`, `0 .yaml files missing coverage`, `0 .yml files missing coverage`, `0 .toml files missing coverage`, `0 .json files missing coverage`, `0 .sh files missing coverage`), so no new or updated aspects were required during this detection pass.
- Discovery run on 2025-10-27 reran tracked extension coverage checks across `.rs/.yaml/.yml/.toml/.json/.sh` files and confirmed every source still maps to an aspect, so no new entries, tag updates, or structural changes were required this cycle.
- Verification on 2025-10-24 reran tracked extension coverage checks (`*.rs/*.yaml/*.yml/*.toml/*.json/*.sh`) and executed the validation trio (`python3 -m json.tool`, `audit.py`, `adi.py`), confirming zero missing sources, no isolates, and overall ADIw still at 35.08 so no new or updated aspects were added this pass.
- Discovery scan on 2025-10-24 reran coverage diff across `.rs`/`.yaml`/`.yml`/`.toml`/`.json`/`.sh` assets and confirmed every tracked code or configuration source already maps to an aspect (only `.github/contribution.md` remains intentionally excluded as marketing copy), so no new entries or updates required this pass.
- Split tool domain models into a dedicated `Tool Domain & Parsing` section by moving 12 entries from Tools/Provider Pipeline, retagged 38 remaining tool/service aspects with shared `services`, `runtime`, and `integration` coverage (50 aspects updated overall), relocated the Claude tool guidelines to Service Integrations, and refreshed provider pipeline tags. Validation now reports no isolates, but overall ADIw rose to 35.08 with Tool Domain 15.81 and Tools 13.79 still requiring connective work.
- Retagged 73 aspects across CLI, Orchestration, Infrastructure, Filesystem, Domain, App Runtime, Provider Pipeline, Quality, Planning, and Crate Metadata to cap each section at ≤10 unique tags, removed the unused `compaction` catalog entry, and reran sync-counts/audit checks (overall ADIw 31.92 with Services/Tools still the largest connectivity gaps).
- Discovery audit on 2025-10-22 confirmed all tracked file types already referenced; no new aspects or updates required this cycle.
- Updated 58 aspects across Tools, Domain Foundations, and Configuration to align shared tag vocabularies (capping section uniques at 10/10/9), restored connectivity for tool surfaces, and reran validation commands to confirm clean audit results.
- Re-tagged 54 aspects across Service Layer, Integration & Policy Services, Context & Reasoning, and Operations to shared vocabularies (`services`, `workflow`, `integration`, `conversation`, `provider`, `infrastructure`, `operations`, `transformers`, `validation`, `snapshots`) lowering unique tags to 10/7/7/5 respectively and clearing audit warnings for those sections.
- Retired 10 low-signal tags (`network`, `api`, `git`, `defaults`, `instructions`, `http`, `recovery`, `xml`, `reasoning`, `write`) across 50 aspects, replacing them with shared vocabulary (`infrastructure`, `operations`, `workflow`, `rendering`, `snapshots`, `validation`) and trimming section unique-tag counts (Services 29, Service Integrations 19, CLI 14, Domain 17) without introducing new isolates.
- Updated 55 aspects across Service Integrations, Operations, Tools, Terminal UI, and runtime surfaces to add catalog tags (`integration`, `registry`, `search`) plus shared `operations` coverage, rerunning validation to clear remaining isolates and ease ADIw from 38.04 to 36.57.
- Updated 53 aspects across Quality, Filesystem, Domain, Domain Foundations, and Services to add connective tags (`validation`, `infrastructure`, `context`, `analytics`, `snapshots`, `planning`), re-synced the tag catalog, and reran `audit.py`/`adi.py` to drop overall isolates from 13 to 0 while bringing ADIw down from 42.47 to 38.04 (still above threshold).
- Added 50 aspects covering crate manifests, module re-exports, provider catalogs, fixtures, plans, and operator docs while introducing the `Crate Metadata` section plus catalog tags (`manifest`, `operations`, `network`) and syncing counts after the expansion.
- Updated 52 aspects to add section-default tags (`runtime`, `context`, `workflow`), retire low-signal tags (`async`, `chat`, `plugin`, `installation`, etc.), and register `context`/`runtime` in the tag catalog.
- Updated 72 aspects across Services, Service Integrations, Developer Tooling, Automation, and Operations to add shared tags (`ci`, `persistence`, `validation`, `http`, `developer`) and align service surfaces with runtime touchpoints.
- Added 20 aspects across Planning, Automation, Infrastructure, Quality, Tools, and Operations to cover roadmap documents, CI module surfaces, and supporting configs like `insta.yaml`, `diesel.toml`, and the shell plugin README.
- Normalised section-default tags (services, infrastructure, configuration, workflow, domain) and replaced the stray `providers` tag with `provider`, updating 24 existing entries while resolving the duplicate Renovate slug under Developer Tooling.
- Re-synced the tag catalog to include `planning`, `tests`, and `performance`, then reformatted both JSON payloads to maintain canonical structure.

## Follow-ups
1. Drive ADIw 35.08 below the 5.0 target by adding cross-links between Domain (11.35), Domain Foundations (15.64), Tools (13.79), Tool Domain (15.81), and Services (7.31); identify candidate tags/backlinks and shared sources to raise weighted degree.
2. Document usage guidance for the new `Tool Domain & Parsing` section and refreshed tags (`runtime`, `integration`, provider) so future tool-related entries land in the right section with consistent coverage.



## Validation log
```
python3 aspects/scripts/tags_manager.py --tags-path aspects/projects/forge/ASPECTS.tags.json --aspects-path aspects/projects/forge/ASPECTS.json sync-counts
python3 -m json.tool --no-ensure-ascii aspects/projects/forge/ASPECTS.json
python3 -m json.tool --no-ensure-ascii aspects/projects/forge/ASPECTS.tags.json
python3 aspects/scripts/audit.py aspects/projects/forge/ASPECTS.json
python3 aspects/scripts/adi.py aspects/projects/forge/ASPECTS.json --per-section --weighted --ignore-tag-frac 0.15 --include-slug-links --include-source-links --adi-threshold 5.0 --show-isolates --isolate-limit 20 --tags-catalog aspects/projects/forge/ASPECTS.tags.json
```
## 2025-10-22 Tag vocabulary cap pass
- Retagged 73 aspects across CLI, Orchestration, Infrastructure, Filesystem, Domain, App Runtime, Provider Pipeline, Quality, Planning, and Crate Metadata to keep each section at ≤10 unique tags.
- Removed the unused `compaction` catalog tag and re-synced counts via `tags_manager.py sync-counts`.
- Reran validation commands; `audit.py` is clean and `adi.py` reports ADIw 31.92 with Services 12.84, Tools 18.95, and Provider Pipeline 5.05 flagged for connectivity follow-up.

## 2025-10-22 Discovery audit pass
- Queried `ASPECTS.json` coverage for `.rs`, `.toml`, `.yaml`, `.json`, `.sh`, `.md`, and `.lock` files; only `.github/contribution.md` and `Cargo.lock` remain intentionally uncovered, leaving no immediate aspect candidates.
- Left sections already at the 25-entry cap untouched to avoid exceeding limits without a restructuring plan.
- Skipped tag/catalog changes; existing follow-ups (tag consolidation, ADIw reduction) remain the next actionable items.
## 2025-10-22 Section vocabulary alignment pass
- Replaced bespoke tags in Service Layer with the shared vocabulary (`services`, `workflow`, `conversation`, `provider`, `templates`, `tools`, `validation`, `infrastructure`, `integration`, `persistence`), cutting unique tags from 29 to 10 while keeping persistence heavy entries discoverable.
- Collapsed Integration & Policy Services tags to (`services`, `integration`, `workflow`, `provider`, `policy`, `persistence`, `infrastructure`), reducing unique tags from 19 to 7 and aligning MCP/policy surfaces with the integrations catalog.
- Normalised Context & Reasoning entries around (`context`, `workflow`, `conversation`, `provider`, `tools`, `transformers`, `validation`) so compaction and transformer coverage cluster under the context tree, dropping unique tags from 17 to 7.
- Updated Operations & Workflows entries to (`operations`, `workflow`, `automation`, `ci`), eliminating incidental tags (`developer`, `snapshots`, `tools`) and shrinking unique tags from 11 to 4.
- Reran `tags_manager.py`, `json.tool`, `audit.py`, and `adi.py`; service-related sections now clear audit tag warnings, ADIw ticked down from 36.24 to 33.96 but remains above threshold pending broader connectivity work highlighted below.
## 2025-10-22 Tag consolidation pass
- Replaced `network`, `api`, `git`, `defaults`, `instructions`, `http`, `recovery`, `xml`, `reasoning`, and `write` with shared tags (`infrastructure`, `operations`, `workflow`, `rendering`, `snapshots`, `validation`) across 50 aspects spanning Behavior Tests, Architecture, Configuration, Tools, Snapshots, and Service Integrations.
- Added `operations`/`snapshots` connectors to undo tooling and policy guidelines to keep the Tools section linked into shared vocabulary while aligning behavior net-fetch tests with infrastructure coverage.
- Pruned the retired tags from `ASPECTS.tags.json`, re-synced catalog counts, and reran `json.tool`, `audit.py`, and `adi.py`; ADIw slid from 36.57 to 36.24 (still above threshold, see follow-ups).
## 2025-10-22 Integration connectivity pass
- Added `integration`, `registry`, and `search` tags while updating 55 aspects across Service Integrations, Operations, Tools, Terminal UI, and runtime re-export modules; re-synced the tag catalog.
- All Operations entries now carry the `operations` tag, and `fs-search-service` picked up shared `search`/`read` tags, eliminating the remaining section isolates.
- Reran `tags_manager.py`, `json.tool`, `audit.py`, and `adi.py`; ADIw improved from 38.04 to 36.57 with zero isolates.


## 2025-10-20 Connectivity refinement pass
- Introduced catalog tags `ci`, `persistence`, `validation`, `http`, and `developer`, then synced counts (31/9/6/5/9 references respectively) to describe CI automation, persistence layers, validation utilities, HTTP adapters, and developer workflows.
- Refreshed 72 existing aspects across Services, Service Integrations, Developer Tooling, Automation, and Operations to add connective tags and update `lastUpdated` metadata.
- CI workflow entries now share the `ci` tag, while persistence-oriented services use `persistence` to bridge configuration, repository, and cache coverage.
- `adi.py` improved from ADIw 38.15 to 33.08 with global isolates cleared, though Services, Configuration, and Operations still harbour section-level isolates listed in follow-ups.


## 2025-10-20 Tag alignment pass
- Added cross-cutting tags (`workflow`, `conversation`, `configuration`, `infrastructure`, `read`, `write`, `discovery`, `errors`, `telemetry`, `rendering`, etc.) to 50 aspects so Services adapters, tool implementations, and foundational domain types cluster with their runtime touchpoints.
- Confirmed `tags_manager.py sync-counts` updated 14 catalog entries, reflecting the new tag assignments.
- Reran `adi.py`; domain-foundation isolates reduced to four but Services/Tools still exceed ADIw thresholds, indicating further refactors (tag consolidation or sectional restructuring) are required.

## 2025-10-20 Planning expansion pass
- Captured 12 roadmap documents for compaction, system-context rendering, retry migration, tool context, model selection, large file ranges, agent loader, dump auto-open, history storage, and AppConfig repository work so strategic decisions are traceable to source plans.
- Added supporting knowledge for CI module exports, tool authoring guidelines, snapshot defaults, Diesel schema configuration, and shell plugin operations to backfill previously uncovered files.
- Normalised section-default tags (services/infrastructure/configuration/workflow/domain) and replaced the `providers` tag with `provider` to tighten section connectivity before rerunning `audit.py`/`adi.py`.

## 2025-10-20 Section-default tag normalization pass
- Added missing section-default tags (`runtime`, `context`, `workflow`, `ui`) to 29 aspects and attached `workflow` to orchestrator surfaces to improve intra-section connectivity.
- Replaced niche tags (`async`, `chat`, `customization`, `installation`, `sandbox`, `auth`, `cache`, `events`, `json`, `logging`, `performance`, `plugin`) across 23 aspects with shared vocabulary (`conversation`, `environment`, `policy`, `analytics`, `persistence`, `release`, `validation`).
- Extended XML coverage to streaming and template aspects, added `context`/`runtime` entries to the tag catalog, and re-synced counts after pruning the retired tags.
- `audit.py` still flags >10 unique tags in Services (30), Service Integrations (20), Configuration (17), CLI (14), etc.; `adi.py` (ADIw 31.98) highlights remaining isolates noted above.

## 2025-10-22 Crate metadata and fixtures coverage pass
- Added 50 aspects spanning module re-exports, provider catalogs, quality fixtures, plan iterations, README/AGENTS operator docs, and the new `Crate Metadata` section that documents every `Cargo.toml`.
- Registered catalog tags `manifest`, `operations`, and `network`, then re-synced counts to account for the new section and fixtures.
- `audit.py` remains warning-only while `adi.py` (ADIw 42.47) now lists additional isolates (`python-valid-fixture`, `python-invalid-fixture`, `service-utils-module`, `tool-call-fixture`, etc.), earmarked in follow-ups for connectivity work.
