# ASPECTS.json status - 2025-10-14

## Summary
- Coverage: 32 sections, 640 aspects.
- Largest sections: CLI wrappers (36), Sessions and history (33), TUI Rendering (30), Observability (29), Repository (28).
- Areas of attention: `cli` And `configuration` after subindexes they dropped to ADIw 4.82 and 4.18; closest candidates for revision - `tools`, `testing`, `repository` (rich set of tags, but still <5).
- Latest checks: `python -m json.tool --no-ensure-ascii aspects/projects/Codex/ASPECTS.json`, `python aspects/scripts/audit.py aspects/projects/Codex/ASPECTS.json`, `PYTHONIOENCODING=utf-8 python aspects/scripts/adi.py aspects/projects/Codex/ASPECTS.json --per-section --weighted --ignore-tag-frac 0.15 --include-slug-links --include-source-links --adi-threshold 5.0 --show-isolates --isolate-limit 20`.

| Section | Aspects | Unique tags | Notes |
| --- | ---: | ---: | --- |
| Architecture | 21 | 17 | It is necessary to reduce the zoo of tags and raise critical conventions to >=0.8. |
| Interface and app server | 15 | 15 | The JSON-RPC loop is described; integration tests need to be updated. |
| TUI core UX | 15 | 12 | We monitor UX tags and add general utilities to the index. |
| TUI Bottom Pane | 18 | 8 | We support compact summaries and control duplicates with core. |
| TUI Cloud Tasks | 18 | 14 | We control the growth of tags and prepare separate subsections. |
| TUI onboarding | 16 | 8 | Update trust/login scripts for new policies. |
| TUI Rendering | 30 | 12 | Status nodes are united, vt100/ANSI are associated with dev rules. |
| Configuration | 23 | 13 | ADIw 4.18 -- `configuration-index` reinforced and highlights key `config-core` files. |
| Security | 13 | 10 | We keep the same hardening rules, and improve the key rotation. |
| Authentication and tokens | 14 | 6 | All login branches are covered; priority - revision of importance. |
| Secrets and storage | 7 | 6 | New section about auth.json and `read_auth_header_from_stdin`, support tag `secrets`. |
| Sandboxes and hardening | 19 | 10 | We control Linux/macOS policies and apply_patch consistency. |
| Responses API Integration | 12 | 10 | Support common tags and synchronization with retry/Azure workaround. |
| Sessions and history | 33 | 14 | Candidate for division (history vs resume/fork) to reduce congestion. |
| Tools | 27 | 18 | Distinguish between runtime utilities and auxiliary scripts. |
| Executing commands | 27 | 13 | Maintain synchronization with sandbox and execpolicy. |
| Integrations | 13 | 16 | Critical index updated; monitor the balance of Ollama/Cloud Tasks tags. |
| MCP Integrations | 23 | 13 | Added critical review, key runtimes are marked `integrations`. |
| SDK and integrations | 25 | 12 | We save the build pipelines, consider selecting submodules. |
| Track Changes | 22 | 10 | We monitor intersections with apply_patch and history. |
| Apply Patch pipeline | 20 | 13 | There is a high spread of tags, we are preparing to split them into stages. |
| Repository | 28 | 13 | Service processes; we avoid intersections with CLI/Tools. |
| CLI wrappers | 36 | 16 | Added subindexes (exec/app-server/mcp), tags aligned around CLI/exec/mcp. |
| CLI Distribution | 12 | 7 | Covering BinaryComponent and staging; We keep synchronization with security. |
| Observability | 29 | 15 | Increase the share of >=0.8 aspects and link with telemetry-core. |
| Developer Environment | 11 | 14 | VS Code/Justfile merged, added `repo-maintenance` And `vt100`. |
| Data Contracts | 19 | 18 | A dictionary of contracts and owners is needed; reduce tag diversity. |
| Security Testing | 12 | 11 | Support coverage login/regression and approval scripts. |
| Testing core operations | 24 | 24 | Requires partitioning by exec/responses/cloud. |
| Testing: Tools & CLI | 24 | 20 | Received configuration tests; bring the set of tags to <=10. |
| Testing: MCP | 20 | 12 | MCP harness is synchronized with integrations, we maintain a single scheme. |
| Testing: Change Tracking & Rollouts | 14 | 8 | Synchronize with rollout processes and history. |

## Overview of sections
- **CLI wrappers (36 / 16 tags)**: added overview entries `cli-exec-index`, `cli-app-server-index`, `cli-mcp-index`; exec tests and utilities now use the same tags (`cli`, `exec`, `mcp`), which reduced the spread and lowered ADIw.
- **Configuration (23 / 13 tags)**: `configuration-index` expanded `core/src/config.rs`, key entries (layers, overrides, sandbox) received the tag `config-core`; test scripts are finally submitted to `testing-tools`.
- **Integrations (13 / 16 tags)**: the section is compressed due to the merger of Ollama subsections; `integrations-index` remains critical when updating Responses/Cloud Tasks/Ollama gateways.
- **MCP Integrations (23 / 13 tags)**: new `mcp-integrations-overview` and marking runtimes `integrations` tied the MCP CLI and server components to the overall picture.
- **Developer Environment (11 / 14 tags)**: VS Code and Justfile collected under `repo-maintenance`, `clippy-color-guard` marked `vt100`, duplicate launch/extensions have been removed.
- **TUI Rendering (30 / 12 tags)**: the status subsystem is combined into `tui-status-card`, ANSI/palette-utilities and shimmer are marked `vt100`, which synchronizes rendering with the rules of the dev environment.

## Key actions
1. For `cli` subindexes for exec/app-server/MCP were added, tags were cleaned up (exec instead of execution, cli-core instead of interface/schema), thanks to which ADIw dropped to 4.82.
2. B `configuration` reinforced `configuration-index` links to `core/src/config.rs`, key entries are marked `config-core`, and the servicing tests are finally submitted to `testing-tools`.
3. Dev/TUI nodes supported: VS Code/Justfile merged under `repo-maintenance`,ANSI/vt100 labels are extended to TUI rendering while maintaining coherence with terminal constraints.

## ADI revision - 2025-10-14
- Team: `PYTHONIOENCODING=utf-8 python aspects/scripts/adi.py aspects/projects/Codex/ASPECTS.json --per-section --weighted --ignore-tag-frac 0.15 --include-slug-links --include-source-links --adi-threshold 5.0 --show-isolates --isolate-limit 20`
- Result: ADIw 33.98 >= 5.00, no isolated aspects (640 records, 24613 edges).
- There are no sections with ADIw >= 5; nearest values - `cli` (4.82) and `configuration` (4.18) after the segmentation.
- Actions taken:
  * Added subindexes `cli-exec-index`, `cli-app-server-index`, `cli-mcp-index`, and exec tests and utilities have been transferred to single tags (`exec`, `cli-core`, `integrations`).
  * IN `configuration` expanded `configuration-index`, and key entries (layers, overrides, sandbox) received the tag `config-core`; servicing tests are included in `testing-tools`.
  * VS Code/Justfile and TUI rendering are synchronized via `repo-maintenance` And `vt100`, which reduced local fragmentation.
- Next steps:
  1. Comb `tools`/`testing` (high dispersion of tags) and prepare thematic indexes for the most verbose subsections.
  2. For `repository` And `observability` reduce unique tags by highlighting auxiliary indexes (maintenance, telemetry-core).
  3. Continue aligning tags `vt100`, `repo-maintenance`, `responses-api` between adjacent sections to keep ADIw < 5.0.
