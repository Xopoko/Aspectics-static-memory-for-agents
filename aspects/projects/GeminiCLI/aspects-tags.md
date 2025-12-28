# Gemini-CLI tag taxonomy

| Tag | Destination | Responsible | Comment |
| --- | --- | --- | --- |
| agents | Related to ACP subagents and agent registry implementation. | Integrations team | Revision 2025-10-13; covers registration and interaction protocol. |
| auth | User and server authentication processes. | Security team | Revision 2025-10-13; includes OAuth, ADC and session verification. |
| automation | Scripts for automating builds, publications and auxiliary tasks. | Automation team | Revision 2025-10-13; includes CI and npm workflow scripts. |
| build | Low-level operations for assembling packages and artifacts. | Automation team | Revision 2025-10-13; We use it for assembly pipelines and bundles. |
| cli | Common user CLI and terminal interaction. | CLI command | Revision 2025-10-13; covers key gemini CLI scripts. |
| cli-command | Specific commands `gemini …` and their handlers. | CLI command | Revision 2025-10-13; We use it to quickly search for commands. |
| code-assist | Integration with Google Code Assist and related services. | Integrations team | Revision 2025-10-14; includes backend, client and UX confirmations. |
| config | Configuration structures, schemas and resolvers. | CLI command | Revision 2025-10-13; includes settings.json and CLI config. |
| core | GeminiCore core execution cycle and management services. | Core platform | Revision 2025-10-13; We use core for internal services. |
| editing | File editing tools, diff strategies and input validation. | Tools team | Revision 2025-10-13; covers EditTool, SmartEdit and proofreaders. |
| execution | Command execution orchestration and CLI process management. | Core platform | Revision 2025-10-13; includes launching tool pipelines and cycles. |
| extensions | Gemini CLI extensions: download, storage and updates. | Extensions command | Revision 2025-10-13; apply to all aspects of the extension ecosystem. |
| fallback | Fallback mechanics for model errors and network scenarios. | Core platform | Revision 2025-10-13; covers Flash fallback and backup paths. |
| filesystem | Working with the file system and accessing the working folder. | Tools team | Revision 2025-10-13; we use it for abstractions and FS tools. |
| ide | IDE integrations and related services. | Integrations team | Revision 2025-10-13; includes Zed, VSCode companion and ACP backend. |
| ink | Components and hooks of Ink rendering of terminal UI. | CLI command | Revision 2025-10-13; apply to aspects of React/Ink implementation. |
| integration-tests | Integration and end-to-end CLI tests. | QA team | Revision 2025-10-13; covers Vitest and test fixtures. |
| integrations | Connecting external services and protocols to the CLI. | Integrations team | Revision 2025-10-13; We use it for MCP, IDE and external APIs. |
| loop-detection | Mechanisms to protect against infinite loops. | Security team | Revision 2025-10-13; highlight LoopDetectionService and its rules. |
| mcp | Model Context Protocol and associated servers. | Integrations team | Revision 2025-10-13; includes configuration, authorization, and MCP clients. |
| memory | Working with session memory and history storage. | Core platform | Revision 2025-10-13; covers ChatRecording and memory loading. |
| metrics | OpenTelemetry counters and metrics. | Telemetry team | Revision 2025-10-13; We use it for quantitative metrics. |
| noninteractive | CLI modes without terminal UI. | CLI command | Revision 2025-10-13; covers non-interactive launch and tools. |
| observability | Observability mechanisms: logs, spans, UI debug. | Telemetry team | Revision 2025-10-13; we distinguish from metrics, the focus is on visualization. |
| policy | PolicyEngine, confirmation rules and access policy. | Security team | Revision 2025-10-13; includes configuration and MessageBus. |
| release | Release pipelines and package publications. | Automation team | Revision 2025-10-13; covers npm/GitHub release processes. |
| routing | Model routers and strategy selection classifiers. | Core platform | Revision 2025-10-14; includes routes, fallback and context signals. |
| sandbox | Sandbox environment, containers and team policies. | Security team | Revision 2025-10-13; We use it to build and run sandbox. |
| security | CLI security: checks, dialogs, confirmations. | Security team | Revision 2025-10-13; general coverage of security requirements. |
| settings | Settings, schema and migration layers settings.json. | CLI command | Revision 2025-10-13; includes MIGRATION_MAP and resolvers. |
| shell | Interaction of the CLI with shell commands and execution. | Tools team | Revision 2025-10-13; concerns ShellTool and confirmations. |
| slash-commands | Infrastructure of slash commands and their loaders. | CLI command | Revision 2025-10-14; We use it for the pipeline and secure command processing. |
| startup | Prepare, initialize and terminate the CLI process. | CLI command | Revision 2025-10-13; new tag for aspects of the starting sequence. |
| streaming | Streaming model responses and processing tokens. | Core platform | Revision 2025-10-13; includes TurnRunner and GeminiChat. |
| telemetry | Common telemetry mechanisms and SDK. | Telemetry team | Revision 2025-10-13; covers signal collection services. |
| terminal | Setting up the terminal, keybinding and TTY launch modes. | CLI command | Revision 2025-10-16; covers raw mode, Kitty protocol and window title control. |
| testing | Common test utilities and strategies. | QA team | Revision 2025-10-13; includes unit and integration scenarios. |
| tools | Tools (Tool API) and their infrastructure. | Tools team | Revision 2025-10-13; covers registry and individual tools. |
| trust | Trusted directories and trust levels. | Security team | Revision 2025-10-13; includes TrustedFolders and trust selection UI. |
| ui-dialogs | Dialog boxes, notifications and consent flow Ink UI. | CLI command | Revision 2025-10-16; We highlight modals, nudges and confirmations. |
| ui-diagnostics | Diagnostic panels, statistics and debug interfaces. | CLI command | Revision 2025-10-16; includes debug console, profiler and resource monitoring. |
| ui-hooks | Ink hooks and interface state contexts. | CLI command | Revision 2025-10-16; covers use groups and UI state providers. |
| ui-input | Input components, tooltips, and shell/TTY adapters. | CLI command | Revision 2025-10-16; includes composer, selection list and history. |
| ui-layout | Wireframe Ink components, layout and application framework. | CLI command | Revision 2025-10-16; covers containers, header, footer and general constants. |
| ui-messages | Rendering of messages of models and tools in the interface. | CLI command | Revision 2025-10-16; includes answer cards and a confirm capture tool. |
| ui | CLI user interface, components and UX. | CLI command | Revision 2025-10-13; apply to Ink UI and UX cases. |
| updates | Updates for extensions and the CLI itself. | CLI command | Revision 2025-10-13; new tag for pipelines and UX updates. |
| workspace | Workspace structure, contexts and associated operations. | CLI command | Revision 2025-10-13; covers WorkspaceContext and migrations. |

> 2025-10-14: Service tags removed `windows` And `packaging`; use combinations `automation`/`build`/`testing` for profile aspects.
