# ASPECTS.json status - 2026-01-16

## Summary
- Coverage: 32 sections, 665 aspects.
- Largest sections: CLI wrappers (36), Sessions and history (35), TUI Rendering (30), Observability/Tools (29), Repository/Execution (28).
- Areas of attention: overall ADIw 33.00 >= 5.00; high tag spread remains in `architecture`, `interface`, `tui`, `tui-rendering`, `tui-cloud-tasks`, `configuration`, `sessions`, `tools`, `execution`, `integrations`, `integrations-mcp`, `responses-api`, `sdk`, `apply-patch`, `repository`, `cli`, `observability`, `data-contracts`, and testing sections.
- Hash verification: report `aspects/scripts/reports/hash_check_2026-01-16_03_2026-01-16.json` (total 898, verified 898, missing 0, mismatches 0; repo-root).
- Latest checks: `python3 -m json.tool --no-ensure-ascii aspects/projects/Codex/ASPECTS.json`, `python3 aspects/scripts/audit.py aspects/projects/Codex/ASPECTS.json`, `python3 aspects/scripts/adi.py aspects/projects/Codex/ASPECTS.json --per-section --weighted --ignore-tag-frac 0.15 --include-slug-links --include-source-links --adi-threshold 5.0 --show-isolates --isolate-limit 20 --tags-catalog aspects/projects/Codex/ASPECTS.tags.json`.
- Check outputs stored: `aspects/scripts/reports/audit_2026-01-16_04.txt`, `aspects/scripts/reports/adi_2026-01-16_04.txt`.

| Section | Aspects | Unique tags | Notes |
| --- | ---: | ---: | --- |
| Architecture | 23 | 17 | Added agent control plane; tag spread still high. |
| Interface and app server | 18 | 11 | Added config API + model list; tag spread above threshold. |
| TUI core UX | 17 | 14 | Collab events + notification fallback now covered for TUI2. |
| TUI Bottom Pane | 18 | 8 | TUI2 bottom-pane widgets are now aligned. |
| TUI Cloud Tasks | 18 | 14 | Composer input now includes TUI2 public widgets. |
| TUI onboarding | 16 | 8 | TUI2 onboarding/welcome/auth steps aligned. |
| TUI Rendering | 30 | 12 | TUI2 rendering sources now aligned; vt100/ANSI remain linked. |
| Configuration | 27 | 15 | Added web-search mode config; tag spread remains high. |
| Security | 13 | 10 | We keep the same hardening rules, and improve the key rotation. |
| Authentication and tokens | 14 | 6 | All login branches are covered; priority - revision of importance. |
| Secrets and storage | 7 | 6 | New section about auth.json and `read_auth_header_from_stdin`, support tag `secrets`. |
| Sandboxes and hardening | 19 | 10 | We control Linux/macOS policies and apply_patch consistency. |
| Responses API Integration | 13 | 11 | Added codex-api client; keep tags aligned with backend-client. |
| Sessions and history | 35 | 14 | Added rollout truncation/init errors; candidate for split (history vs resume/fork). |
| Tools | 29 | 19 | Added collab tools; tag spread remains high. |
| Executing commands | 28 | 13 | Added execpolicy-legacy context; keep sandbox alignment. |
| Integrations | 15 | 17 | Added LM Studio OSS bootstrap and codex-client transport. |
| MCP Integrations | 25 | 16 | Added exec-server shell tool and shell-tool-mcp launcher. |
| SDK and integrations | 25 | 12 | We save the build pipelines, consider selecting submodules. |
| Track Changes | 22 | 10 | We monitor intersections with apply_patch and history. |
| Apply Patch pipeline | 20 | 13 | There is a high spread of tags, we are preparing to split them into stages. |
| Repository | 28 | 13 | Service processes; we avoid intersections with CLI/Tools. |
| CLI wrappers | 36 | 16 | Added subindexes (exec/app-server/mcp), tags aligned around CLI/exec/mcp. |
| CLI Distribution | 12 | 7 | Covering BinaryComponent and staging; We keep synchronization with security. |
| Observability | 29 | 15 | TUI2 session log and OTEL layer now tracked. |
| Developer Environment | 12 | 8 | Added Bazel build/RBE setup documentation. |
| Data Contracts | 22 | 20 | Added app-server v2 thread APIs; tag diversity still high. |
| Security Testing | 12 | 11 | Chatwidget approval tests now include TUI2. |
| Testing core operations | 24 | 24 | Requires partitioning by exec/responses/cloud. |
| Testing: Tools & CLI | 24 | 20 | Received configuration tests; bring the set of tags to <=10. |
| Testing: MCP | 20 | 12 | MCP harness is synchronized with integrations, we maintain a single scheme. |
| Testing: Change Tracking & Rollouts | 14 | 8 | Synchronize with rollout processes and history. |

## Overview of sections
- **Architecture (23 / 17 tags)**: added agent control plane for multi-agent lifecycle; tag spread still high.
- **Interface and app server (18 / 11 tags)**: config API and model list now documented; tag spread above threshold.
- **TUI core/bottom/onboarding (17/18/16 entries)**: TUI2 sources aligned across chatwidget, bottom pane, and onboarding steps.
- **Observability (29 / 15 tags)**: TUI2 session log and OTEL layer coverage added.
- **Developer Environment (12 / 8 tags)**: Bazel build/RBE setup documented alongside justfile workflows.
- **Data Contracts (22 / 20 tags)**: app-server v2 thread APIs and thread history builder captured.

## Key actions
1. Added WebSearchMode configuration coverage and updated tool registration behavior.
2. Documented app-server v2 thread lifecycle APIs and metadata payloads.
3. Captured Bazel build + remote execution setup in dev environment.
4. Updated Linux sandbox coverage with read-only bind-mount helper notes.
5. Refreshed audit/ADI/hash reports after updates.

## ADI revision - 2026-01-16
- Team: `python3 aspects/scripts/adi.py aspects/projects/Codex/ASPECTS.json --per-section --weighted --ignore-tag-frac 0.15 --include-slug-links --include-source-links --adi-threshold 5.0 --show-isolates --isolate-limit 20 --tags-catalog aspects/projects/Codex/ASPECTS.tags.json`
- Result: ADIw 33.00 >= 5.00, no isolated aspects (665 records, 27182 edges).
- Sections with ADIw >= 5: none. Near-threshold sections: `cli` (4.84), `tui` (4.65), `architecture` (4.57), `integrations` (4.51), `tui-rendering` (4.44), `repository` (4.43), `integrations-mcp` (4.36), `tui-bottom-pane` (4.36), `testing` (4.17), `dev-environment` (4.17), `configuration` (3.97).
- Next steps:
  1. Consolidate tags in `tools`, `integrations`, `integrations-mcp`, and `interface` (high tag dispersion, counts >10).
  2. Reduce tag diversity in `architecture`, `configuration`, `tui`, `responses-api`, and `data-contracts` by tightening tag usage.
  3. Consider splitting `sessions` and `tui-rendering`, and revisit testing tag overload once new indexes stabilize.
