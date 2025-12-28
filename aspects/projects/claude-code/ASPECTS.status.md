# Claude Code ASPECTS Status

## 2025-10-16

- Added 50 new aspects (hooks, command-guardrails, agent-runtime, agent-commands, plugins, documentation) with a focus on whitespace `editor`, `agent-runtime`, `command-guardrails` and new command descriptions `new-sdk-app`, `review-pr`, `dedupe` and infrastructure README. New section created `duplicate-commands`, into which the latest posts about the dedupe ritual have been moved to relieve the load `agent-commands` (now 24 entries).
- Audit: `python3 -m json.tool --no-ensure-ascii aspects/projects/claude-code/ASPECTS.json` | `python3 aspects/scripts/audit.py aspects/projects/claude-code/ASPECTS.json` -> warnings about >10 unique tags in `agent-commands`, `documentation`, `agent-runtime`, as well as about the new section `duplicate-commands` (3 entries). Plan: at the next revision cycle, combine tags through merging `documentation`/`agent-*` and, if necessary, expand the duplicate-commands section with additional linking entries.
- ADI: `python3 aspects/scripts/adi.py aspects/projects/claude-code/ASPECTS.json --per-section --weighted --ignore-tag-frac 0.15 --include-slug-links --include-source-links --adi-threshold 5.0 --show-isolates --isolate-limit 20 --tags-catalog aspects/projects/claude-code/ASPECTS.tags.json` -> total ADIw 11.73 >= 5.0 (no isolates). In the next updates, add bridges between `agent-runtime` ↔ `plugins` And `agent-commands` ↔ `documentation` (responsible: Claude Code platform team).
- Tags are synchronized: `python3 aspects/scripts/tags_manager.py --tags-path aspects/projects/claude-code/ASPECTS.tags.json --aspects-path aspects/projects/claude-code/ASPECTS.json sync-counts`.

## 2025-10-16

- Former section `agent-workflows` divided into three sections: `agent-workflows-feature-dev` (14 entries), `agent-workflows-pr-review` (15) and `agent-workflows-agent-sdk` (24) to remove the previous warning about excess volume and speed up navigation through command rituals.
- Updated entries `agent-commands-commit-bundle` And `plugin-commit-bundle`: sources translated into `.claude-plugin/marketplace.json`, `lastUpdated=2025-10-16`.
- Removed tag `editor` from document `devcontainer-extension-preinstall-doc`, and PR-review trigger playbooks do not have the tag `examples`, thanks to which `documentation` And `agent-playbooks` fit within the limit of unique tags.
- `python3 -m json.tool --no-ensure-ascii aspects/projects/claude-code/ASPECTS.json`
- `python3 aspects/scripts/audit.py aspects/projects/claude-code/ASPECTS.json` -> without warnings.
- `python3 aspects/scripts/adi.py aspects/projects/claude-code/ASPECTS.json --per-section --weighted --ignore-tag-frac 0.15 --include-slug-links --include-source-links --adi-threshold 5.0 --show-isolates --isolate-limit 20 --tags-catalog aspects/projects/claude-code/ASPECTS.tags.json` -> ADIw 11.18 >= 5.0, no isolates; `agent-playbooks` holds ADIw 5.14. We need bridge aspects between `agent-playbooks`, `agent-commands` And `plugins` (responsible: Claude Code platform team, due date: next update).
- `python3 aspects/scripts/tags_manager.py --tags-path aspects/projects/claude-code/ASPECTS.tags.json --aspects-path aspects/projects/claude-code/ASPECTS.json sync-counts`

## 2025-10-17

- Added 6 new aspects for `pr-review-toolkit` agents (code reviewer, comment analyzer, code simplifier, test analyzer, silent failure hunter, type design analyzer) with an emphasis on sample launch scenarios; chapter `agent-playbooks` now records when to proactively pull specialized agents.
- Updated 44 existing entries: sections `editor`, `documentation`, `automation`, `telemetry`, `command-guardrails`, `security` received an adjusted `importance`, new tags `vscode` And `claude-bot`, as well as a single `lastUpdated=2025-10-17`to enhance underfilled areas and find VS Code/Claude automation faster.
- Tags have been added to the dictionary `claude-bot` And `vscode`, counters recalculated (`tags_manager.py … sync-counts`).
- `python3 -m json.tool --no-ensure-ascii aspects/projects/claude-code/ASPECTS.json`
- `python3 aspects/scripts/audit.py aspects/projects/claude-code/ASPECTS.json` -> warnings: `section-agent-playbooks` And `section-documentation` use >10 unique tags; further unification of tags is required (responsible: Claude Code platform team, deadline: next tag revision cycle).
- `python3 aspects/scripts/adi.py aspects/projects/claude-code/ASPECTS.json --per-section --weighted --ignore-tag-frac 0.15 --include-slug-links --include-source-links --adi-threshold 5.0 --show-isolates --isolate-limit 20 --tags-catalog aspects/projects/claude-code/ASPECTS.tags.json` -> ADIw 11.39 >= 5.0, no isolates; additional bridges between `agent-playbooks`/`documentation` and other sections (responsible: Claude Code platform team, deadline: March update).
- `python3 aspects/scripts/tags_manager.py --tags-path aspects/projects/claude-code/ASPECTS.tags.json --aspects-path aspects/projects/claude-code/ASPECTS.json sync-counts`

## 2025-10-16

- Added 25 new aspects (17 for issue intake templates, 8 for automation) to close the gap `issue-templates` (now 25 entries) and expand `automation` details about dispatch, lock and dedupe workflows.
- 31 existing entries were updated: tags were unified (removed `plugins` from `agent-commands`/`agent-runtime`/`command-guardrails`, `quality-safety`/`testing` from section `plugins`), marked everywhere `lastUpdated=2025-10-16`, which removed warnings about >10 unique tags.
- `python3 -m json.tool --no-ensure-ascii aspects/projects/claude-code/ASPECTS.json`
- `python3 aspects/scripts/audit.py aspects/projects/claude-code/ASPECTS.json` -> no errors, sections within limits.
- `python3 aspects/scripts/adi.py aspects/projects/claude-code/ASPECTS.json --per-section --weighted --ignore-tag-frac 0.15 --include-slug-links --include-source-links --adi-threshold 5.0 --show-isolates --isolate-limit 20 --tags-catalog aspects/projects/claude-code/ASPECTS.tags.json` -> general ADIw 10.87 >= 5.0, isolated `automation:claude-dedupe-manual-dispatch`; you need to link the record to other dedupe aspects (for example, through `duplicate-operations`) in the next cycle.
- `python3 aspects/scripts/tags_manager.py --tags-path aspects/projects/claude-code/ASPECTS.tags.json sync-counts`

## 2025-10-14

- A starting base has been created from 7 aspects (devcontainer, automation, security, plugins). There are no interconnections yet, so `python aspects/scripts/adi.py ...` showed ADIw 24.50 and marked the machines, security hook and marketplace as isolated.
- Action: after expanding the database, add connecting tags/links to the aspects (for example, link automation scripts with security-hook and devcontainer infrastructure) and recalculate ADI. Responsible: Claude Code platform team. Deadline: next sprint.
- Expansion of the database to 18 aspects (GitHub Actions, plugin docs). New run `python3 aspects/scripts/adi.py ...` gave ADIw 56.00, isolated 10 entries, especially the plugins section (no common tags/links). It is required to plan connecting aspects (common installation processes, shared tags) and/or cross-reference policy. Responsible: Claude Code platform team. Deadline: until the next database update.

## 2025-10-15

- Added 33 new aspects: sections `agent-commands`, `agent-playbooks`, `documentation`, issue templates and automation have been expanded. `python aspects/scripts/adi.py ... --adi-threshold 5.0` -> ADIw 22.39, isolated 4 records globally, and sections `agent-commands`, `agent-playbooks`, `plugins`, `hooks`, `editor` exceed the threshold due to lack of connections.
- Action: prepare a cross-link plan - add connecting tags and aspects (for example, procedural gates referencing commands/agents, and connections between plugins and their commands) and recalculate ADI in the next cycle. Responsible: Claude Code platform team. Deadline: next sprint.
- Added cross-workflow aspects to `agent-commands`, tags expanded (`duplicate-triage`, `pr-review`, `quality-safety`), sections `hooks` And `editor` received second entries. New run `python aspects/scripts/adi.py ...` showed ADIw 12.57: there are no isolated nodes, but `agent-commands` (ADIw 8.78), `agent-playbooks` (ADIw 11.77) and `plugins` (ADIw 9.66) is still above the threshold - additional cross-links (common tags/overview aspects) between commands and plugin packages are required.
- Moved security-guidance aspects to the section `security`, added `vscode-formatting-guardrails` And `devcontainer-net-capabilities`, descriptions of hooks and PowerShell launcher have been clarified. `python3 aspects/scripts/audit.py aspects/projects/claude-code/ASPECTS.json` warns about sections of <=6 entries and 11 unique tags for plugins - we keep this under control.
- Run `python3 aspects/scripts/adi.py ... --adi-threshold 5.0` gave ADIw 6.96 >= 5.0; isolated `environment:gitattributes` And `security:devcontainer-net-capabilities`. Plan: connect them with devcontainer firewall/automation aspects (responsible: Claude Code platform team, deadline: next update).
- Added eight new aspects (persisted devcontainer state, memory cap, npm prefix, firewall sudoers, zsh defaults, git delta, hook state persistence, PR review toolkit README) and moved `security-reminder-hook`/`security-guidance-hooks-config` to the section `hooks`to strengthen underpopulated sections. No new tags were introduced; existing dictionaries cover `devcontainer`, `security-hooks`, `pr-review`, `git-workflow`.
- `python3 aspects/scripts/audit.py aspects/projects/claude-code/ASPECTS.json` still marks sections `editor`, `documentation`, `hooks`, `issue-templates`, `security` with <=6 entries and 11 unique tags per `plugins`. `python3 aspects/scripts/adi.py ... --adi-threshold 5.0` showed ADIw 7.33 >= 5.0: isolated `environment:devcontainer-powershell-launcher`, `environment:gitattributes`, `security:devcontainer-net-capabilities`. It is required to connect these nodes with new devcontainer aspects or automation scripts in the next cycle (responsible: Claude Code platform team).
- Updated nine aspects of devcontainer/security (firewall, sudoers, state persistence, memory cap, etc.) and added `security-reminder-patterns`to fix the list of security hook rules. Teams `python3 -m json.tool --no-ensure-ascii`, `python3 aspects/scripts/audit.py`, `python3 aspects/scripts/adi.py ...`, `python3 aspects/scripts/tags_manager.py ... sync-counts` passed; ADIw 7.38 >= 5.0, insulated `environment:devcontainer-powershell-launcher`, `environment:gitattributes`, `security:devcontainer-net-capabilities`. Plan: link the launcher and gitattributes to the main devcontainer/automation aspects and add cross-links for `devcontainer-net-capabilities` in the next cycle (Claude Code platform team).

## 2025-02-15

- Duplicate automation has been moved to a new section `duplicate-operations` (17 existing aspects moved from `automation`, added 10 new entries about logs, reaction checks and issue forms). `automation` now contains 10 records, the overloaded block has been unloaded.
- Updated 23 existing aspects (guardrails, issue templates, telemetry, backfill/auto-close pipelines), adding links to a new section and revealing user environments, `sed`-shielding, reaction skip, etc. Tag added `observability` (logging/diagnostics), `bug-report-template` got the tag `environment`.
- Expanded the section `command-guardrails` up to 10 entries: scripts recorded `clean_gone`, `commit-push-pr`, `dedupe`, `feature-dev` with an emphasis on the sequence of steps and approval gates; teams added a tag `plugins`to link guardrails with packages of the same name, and the basic commands `feature-dev` And `dedupe` got a tag `tool-guardrails`.
- Run `python3 -m json.tool --no-ensure-ascii aspects/projects/claude-code/ASPECTS.json` + `python3 aspects/scripts/audit.py …` + `python3 aspects/scripts/adi.py … --tags-catalog …` + `python3 aspects/scripts/tags_manager.py … sync-counts`.
- `audit.py`: warnings remain for sections `agent-commands`, `documentation`, `plugins`, `agent-runtime` (>10 unique tags each) and `command-guardrails` (10 records, but 12 unique tags) - either aggregation or unification of tags will be required.
- `adi.py`: total ADIw 10.71 >= 5.0 (no isolates). The highest ADIw `agent-commands` (4.20), `agent-playbooks` (4.15), `plugins` (4.04) and `environment` (2.43). It is necessary to plan additional bridges (for example, make connections between plugins  agent-* and additionally connect env/devcontainer aspects).

## 2025-02-14

- Added 50 new aspects: sections formed `agent-runtime` (11 entries) and `command-guardrails` (5 entries), the automation block was expanded (+16) and a section was created `telemetry` for Statsig monitoring. We covered the runtime profile of agents, the allowlist of tools for teams, the details of Bun scripts and the PowerShell launcher.
- Expanded taxonomy with tags `agent-runtime` And `tool-guardrails`; counters are synchronized via `python3 aspects/scripts/tags_manager.py --sync-counts`.
- `python3 aspects/scripts/audit.py` -> warnings: `documentation` And `plugins` use >10 unique tags, `automation` contains 26 records (>25), new sections `command-guardrails` And `telemetry` so far <=6 records; recorded in the backlog the need for further aggregation/disaggregation.
- `python3 aspects/scripts/adi.py ... --adi-threshold 5.0` -> overall ADIw 10.44 (>=5). The isolate remained with `environment:gitattributes`; we need to link it with devcontainer automation in the next update. The remaining new sections without isolated units.
- Additionally updated `environment:gitattributes`by adding connections via tags `devcontainer` And `network-security`, so the isolate disappeared; the overall ADIw remains 10.42 >= 5.0, we continue to plan end-to-end communications devcontainer  automation to reduce the indicator.
- Added cross-sectional aspects: `automation/bun-scripts-line-endings`, `telemetry/dedupe-telemetry-bridge`, `command-guardrails/dedupe-automation-alignment` connect git rules, guardrails and Statsig telemetry into a common duplicate policy.
- Repeated `python3 aspects/scripts/adi.py ...` -> ADIw 10.07 >= 5.0 (no isolates). Further linking of sections is required (for example, linking `agent-commands` And `plugins` through general reviews, reduce unique tags in `documentation`/`plugins` and aggregate `automation`, where there are already 27 entries).
