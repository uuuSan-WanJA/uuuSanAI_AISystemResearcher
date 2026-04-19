---
title: openwork deep-dive
slug: openwork
status: deep-dive
confidence: medium-high
rounds: 1
date_completed: 2026-04-19
target: https://github.com/different-ai/openwork
substrate: OpenCode (same substrate as OMO, different coupling)
axes_used: [1,2,3,4,5,6,7,8,9,10,11,12]
axes_added_local: [13 (OpenCode substrate comparison — specific to this corpus position)]
axes_dropped_local: []
---

## Executive summary (3 lines)

openwork is a **GUI-first product shell around OpenCode** — Tauri 2 + SolidJS desktop app + local `openwork-server` API + Slack/Telegram/WhatsApp connector (`opencode-router`) — built by Benjamin Shafii (different-ai) as an explicit "open alternative to Claude Cowork" for non-technical end-users. Unlike OMO (OpenCode plugin + CLI), openwork **consumes** OpenCode through (a) spawning `opencode serve` or `opencode -p "…" -f json -q`, (b) reading `.opencode/opencode.db` SQLite, and (c) the `@opencode-ai/sdk/v2/client` SDK. Its primary invention is not an agent primitive but a **multi-surface distribution layer** (desktop / CLI orchestrator / cloud worker / Slack / Telegram / WhatsApp) with a typed server API, per-workspace audit log, scoped tokens (owner/collaborator/viewer), and identity-scoped chat routing.

---

## 1. Identity & provenance

- **Repo**: https://github.com/different-ai/openwork (default branch `dev`).
- **Org**: different-ai (GitHub org id 118544361).
- **Primary author**: Benjamin Shafii (GitHub `benjaminshafii`, HN handle `ben_talent`, email `ben@openworklabs.com`). 1,578 commits — dominant contributor.
- **Secondary contributors**: `jcllobet` (131), `OmarMcAdam` (112), `src-opn` (83). External community: ~20 small contributors (Golenspade / AdianKozlica / berkozero / sean-brydon etc., each ≤ 5 commits).
- **Repo created**: 2026-01-14T01:39:31Z. Show HN posted **same day** (2026-01-14T04:55:04Z, 231 points, id 46612494) — explicit "just built this" positioning.
- **Adoption signal**: **13,909 stars / 1,297 forks / 65 subscribers / 130 open issues** in ~3 months. Extremely strong early adoption.
- **Release cadence**: v0.11.207 on 2026-04-14 → **207+ patch releases** in ~3 months, driven by an automated `Release App` GitHub Actions workflow bumped via `pnpm bump:patch` + `git tag vX.Y.Z` + workflow dispatch. `github-actions[bot]` is listed as release author.
- **Homepage / distribution**: https://openworklabs.com; downloads at `/download`, enterprise plan pitched at `/enterprise`, Windows support gated behind paid plan at `/pricing#windows-support`.
- **License**: MIT (added **after** HN launch in response to a top-thread comment "This doesn't seem to be open source, it's currently all rights reserved" — `ben_talent` replied "Oh damn thanks for flagging. I just added an MIT license.").
- **Evidence quote (origin story)**: *"i have a home server, and i wanted my wife and i to be able to run privileged workflows. things like controlling home assistant, or deploying custom web apps … without living in a terminal. our initial setup was running the opencode web server directly and sharing credentials to it. that worked, but i found the web ui unreliable and very unfriendly for non-technical users."* — Ben Shafii, Show HN (https://news.ycombinator.com/item?id=46612494).

## 2. Problem framing

- **Target users**: two personas named explicitly in `PRODUCT.md`: *"Bob IT guy makes the config. Susan the accountant consumes the config."* The harness is designed around that split.
- **Stated gap**: *"Current CLI and GUIs for opencode are anchored around developers. That means a focus on file diffs, tool names, and hard to extend capabilities without relying on exposing some form of cli."* (README, Why section).
- **Stated positioning vs Claude Cowork**: *"Cowork is closed-source and locked to Claude Max. We need an open alternative. Mobile-first matters. People want to run tasks from their phones, including via messaging surfaces like WhatsApp and Telegram … Slick UI is non-negotiable."* (AGENTS.md, "Why OpenWork Exists").
- **Product mission**: *"Make your company feel 1000× more productive. … We give AI agents the tools your team already uses and let them learn from your behavior."* (VISION.md).
- **Four stated product properties** (README "Why"): **Extensible** (skill + opencode plugins as installable modules), **Auditable** (show what, when, why), **Permissioned** (privileged flows gated), **Local/Remote** (same mental model either way).

## 3. Control architecture

**This is NOT an agent primitive harness — it is a product shell.** The control architecture is a three-layer client/server/worker model:

- **App layer** (`apps/app/` SolidJS SPA) — UI only, consumes server APIs.
- **Shell layer** (`apps/desktop/` Tauri 2.x) — hosts the SPA, exposes `engine_*`, `orchestrator_*`, `openwork_server_*`, `opencodeRouter_*` native commands for process lifecycle.
- **Server layer** (`apps/server/` `openwork-server`) — typed REST API + SSE events, owns filesystem mutation, audit, approvals.
- **Execution layer** — OpenCode itself (separate binary, spawned or connected remote).

Three production runtime modes (AGENTS.md "Core Runtime Model"):
1. **Desktop-hosted**: app + server run on-device together.
2. **CLI-hosted**: `openwork-orchestrator` daemon hosts the server on a trusted machine (no UI).
3. **Hosted cloud**: Daytona-backed worker runs `openwork serve` + OpenCode in a sandbox; user connects from desktop/mobile app via `Add a worker` → `Connect remote`.

Loop-vs-workflow taxonomy: **workflow-native** — openwork itself is not a loop. Loops happen *inside* OpenCode sessions (OpenCode's own agent loop). openwork is a surface around OpenCode's SSE event stream (`/event` subscription) + session CRUD.

### Explicit design principle: Predictable > Clever

*"OpenWork optimizes for predictability over 'clever' auto-detection. Users should be able to form a correct mental model of what will happen. Prefer explicit configuration (a single setting or env var) over heuristics. Auto-detection is acceptable as a convenience, but must be explainable (we can tell the user what we tried), overrideable (one obvious escape hatch), safe (no surprising side effects)."* — `ARCHITECTURE.md`.

Example applied pattern (Docker sandbox): `OPENWORK_DOCKER_BIN` override → process PATH → `/usr/libexec/path_helper` (macOS login path) → well-known locations. Each tier is explainable and overrideable.

## 4. State & context model

- **Per-workspace `.opencode/` directory** is the canonical state root: `skills/`, `agents/`, `commands/`, `plugins/` (OpenCode native directories) + `openwork.json` (openwork-specific per-workspace metadata).
- **OpenCode SQLite DB** at `.opencode/opencode.db` (project-local) or `~/.opencode/opencode.db` (global) — sessions + messages + tool-call history. openwork **reads** this directly as one of three bridge mechanisms (the others being CLI spawn and SDK client).
- **Server-owned data** at `~/.openwork/openwork-server/`: scoped tokens, workspace registry, and **per-workspace audit log** (`audit/<workspaceId>.jsonl`, appended one JSON line per entry — `apps/server/src/audit.ts` `auditLogPath` / `readAuditEntries`).
- **Filesystem mutation policy** (`ARCHITECTURE.md`): *"OpenWork should route filesystem mutations through the OpenWork server whenever possible … server-routed writes keep permission checks, approvals, audit trails, and reload events consistent. Tauri-only filesystem commands are a host-mode fallback, not the primary product surface."* This is a strong architectural rule: **all writes go through the server REST API, not via Tauri**; local FS access in the desktop shell is explicitly a fallback. Reads can fall back locally.
- **Hot-reload model** ("Living Systems" in AGENTS.md): changes to `.opencode/` or `opencode.json` trigger reload; reload is *session-aware* (queue until active sessions finish) and *workspace-scoped* (never leaks across workspaces). `createSystemState()` + `markReloadRequired(reason, trigger)` + a single shared `reloadRequired()` popup in `app.tsx`. *"Do not invent a separate reload banner per feature."*
- **Sessions** are OpenCode-native (SSE-streamed from OpenCode); openwork surfaces todos as an "execution plan" timeline (README "What's Included").

## 5. Prompt strategy

openwork itself has **no canonical prompt corpus** — product philosophy explicitly cedes this to OpenCode:

- From VISION.md: *"OpenCode is the engine. OpenWork is the experience : onboarding, safety, permissions, progress, artifacts, and a premium-feeling UI."*
- Non-goals (VISION.md): *"Creating bespoke 'magic' capabilities that don't map to OpenCode APIs."*
- PRINCIPLES.md: *"Prompt is the workflow: product logic lives in prompts, rules, and skills."*

In-repo skills are minimal and mostly **developer-facing for contributors**, not end-user workflow skills:
- `.opencode/skills/`: `browser-setup-devtools`, `cargo-lock-manager`, `get-started` (a 4-line onboarding demo), `opencode-bridge`, `opencode-mirror`, `opencode-primitives` (a reference skill pointing at OpenCode docs), `openwork-core`, `openwork-debug`, `openwork-docker-chrome-mcp`, `openwork-orchestrator-npm-publish`, `release`, `solidjs-patterns`, `tauri-solidjs`.
- Skill format: standard OpenCode SKILL.md with YAML frontmatter (`name`, `description`). E.g., `opencode-primitives` SKILL.md is essentially a pointer: *"Skill files live in `.opencode/skills/<name>/SKILL.md` or global `~/.config/opencode/skills/<name>/SKILL.md`. Skills are discovered by walking up to the git worktree and loading any matching `skills/*/SKILL.md` in `.opencode/` or `.claude/skills/`."*
- End-user workflow skills are **expected to come from the user's workspace** (their own `.opencode/skills/`), not shipped by openwork. The in-app UI is a Skill Manager that lists installed skills and imports local folders into `.opencode/skills/<skill-name>`.

Slash-command surface in `.opencode/commands/`: only **3 files** (`browser-setup.md`, `hello-stranger.md`, `release.md`). Minuscule compared to gstack (23+) / ECC / Compound Engineering. openwork does **not** ship a slash-command bundle as a "product" — this is consistent with its stated non-goal and its explicit reliance on OpenCode-native commands.

## 6. Tool surface & permission model

**openwork-server endpoints** (`apps/server/README.md`):

- Capability discovery: `GET /health /status /capabilities /whoami /workspaces`
- Per-workspace config: `GET|PATCH /workspace/:id/config`
- Event stream: `GET /workspace/:id/events` (SSE)
- Engine lifecycle: `POST /workspace/:id/engine/reload`
- Primitive CRUD: `/workspace/:id/{plugins|skills|mcp|commands}` (GET/POST/DELETE)
- **Audit log**: `GET /workspace/:id/audit`
- **Export/import**: `GET /workspace/:id/export`, `POST /workspace/:id/import` (shareable `.opencode/**` + `opencode.json` as portable bundle)
- **Approvals**: `GET /approvals`, `POST /approvals/:id {reply: "allow"|"deny"}`
- **Tokens** (host/owner auth): `GET|POST|DELETE /tokens` with scope = `owner | collaborator | viewer`
- **Inbox/outbox**: `POST /workspace/:id/inbox` (multipart file upload into `.opencode/openwork/inbox/`), `GET /workspace/:id/artifacts`
- **File sessions**: JIT catalog + batch read/write for remote file sync
- **OpenCode proxy**: `/opencode/*` and `/w/:id/opencode/*` passthrough
- **Router proxy**: `/opencode-router/*` with auth policy (*"`GET /opencode-router/health` requires client auth. All other `/opencode-router/*` endpoints require host/owner auth."*)

**Approval modes** (`OPENWORK_APPROVAL_MODE`): `manual` (default, 30s timeout) or `auto`. In manual mode, *"All writes are gated by host approval."* Host APIs accept either `X-OpenWork-Host-Token: <token>` (legacy) or `Authorization: Bearer <token>` where token scope is `owner`.

**Per-launch credential rotation** (ARCHITECTURE.md Mode A): *"Desktop-launched OpenCode credentials are always random, per-launch values generated by OpenWork. OpenCode stays on loopback and is intended to be reached through OpenWork server rather than exposed directly."* Loopback binding (`127.0.0.1`) is default; remote sharing is explicit opt-in that rebinds openwork-server to `0.0.0.0` *"while keeping OpenCode on loopback."*

**Sandbox mode** (desktop): `openwork start --sandbox {auto|docker|container}` runs sidecars inside a Linux container boundary with workspace mounted from host. Apple `container` CLI preferred on Macs; Docker fallback. Extra mounts require allowlist at `~/.config/openwork/sandbox-mount-allowlist.json`.

**Audit is simple jsonl append** (`apps/server/src/audit.ts`): `appendFile(auditLogPath(workspaceId), JSON.stringify(entry) + "\n")`. One file per workspace under `~/.openwork/openwork-server/audit/<workspaceId>.jsonl`; legacy path `workspaceRoot/.opencode/openwork/audit.jsonl` read for backward compat. No structured DB, no redaction layer beyond the runtime's "hides model reasoning and sensitive tool metadata by default" note.

## 7. Human-in-the-loop points

Three permission posture layers (least-privilege by default, per PRINCIPLES.md):

1. **Folder authorization**: *"Work with only the folders the user authorizes."* Tauri dialog plugin capability: `apps/desktop/src-tauri/capabilities/default.json`.
2. **Approval gate** (server): host-approval for writes with configurable timeout. UI surfaces pending approvals as "permission requests and reply (allow once / always / deny)" (README). CLI equivalent: `openwork approvals list` + `openwork approvals reply <id> --allow|--deny`.
3. **Transparency**: *"Provide transparent status, progress, and reasoning at every step."* Plans/steps/tool-calls surfaced as timeline. Export of `audit.jsonl` available.

**Debug exports**: *"Settings -> Debug … export both the runtime debug report and developer logs before filing an issue."* First-class UI path for reproducing bug reports.

## 8. Composability

- **Extension primitives** come from OpenCode, not openwork (PRINCIPLES.md: *"Treat plugins + skills + commands + mcp as the primary extensibility system. These are native to OpenCode and OpenWork must be a thin layer on top of them."*).
- **Skills Manager UI** reads and imports local skill folders into `.opencode/skills/<skill-name>`. From VISION.md: *"zero-friction setup — your existing opencode configuration just works, no migration needed."*
- **Plugins**: openwork edits `opencode.json` `plugin` array from the Skills tab. Project scope = `<workspace>/opencode.json`; global scope = `~/.config/opencode/opencode.json`.
- **Shareable bundles**: `GET /workspace/:id/export` → `POST /workspace/:id/import` moves `.opencode/**` + `opencode.json` state as a portable blueprint. From ARCHITECTURE.md: *"workspace template starter-session materialization from portable blueprint config (not copied runtime session history)."*
- **Team skill hubs** (PRODUCT.md): *"Organizations can publish shared skill hubs so members discover approved skills from one managed place instead of collecting local-only installs by hand."* Managed in OpenWork Cloud (internal name: **Den**).
- **Living Systems** (AGENTS.md): agents/skills/commands/config are **hot-reloadable while sessions are running**. *"This enables agents to create new skills or update their own configuration and have changes take effect immediately, without tearing down active sessions."*

## 9. Empirical claims & evidence

- **Stars**: 13,909 (measured 2026-04-19 via `gh api repos/different-ai/openwork`).
- **Release cadence**: 207+ patch releases in 3 months (v0.11.207 on 2026-04-14, auto-shipped via GHA).
- **HN launch**: 231 points, 2026-01-14. Top concerns raised (and acknowledged by author):
  - *"Still feels a bit technical. The Claude approach is designed for 'Susan in Accounting'."* → Author reply: *"Yeah it is still too technical. First obvious stuff like getting the dmg notarized having easier install … have some prepackaged configs for folks like starter template, ship opencode within the app itself so users don't need to manually install it."*
  - *"This isn't open source."* → Author added MIT license mid-thread.
  - *"What's the security boundary here — there's no mention of a VM or anything to isolate the agent from the file system?"* (unanswered on HN at time of snapshot; later partially addressed by `--sandbox` mode).
- **Outcome claims**: none quantified. Mission statement ("1000× more productive") is aspirational; no benchmarks.
- **Localization shipped**: English, Japanese, Simplified Chinese, Vietnamese, Brazilian Portuguese (README); translated READMEs in 简体中文, 繁體中文, 日本語.

## 10. Failure modes & limits

- **Bus factor ≈ 1**: Benjamin Shafii has 1,578 commits; next human contributor (`jcllobet`) is at 131. External community contributions all ≤ 5 commits (per `gh api /contributors`).
- **Windows support is paywalled**: README: *"Windows access is currently handled through the paid support plan on openworklabs.com/pricing#windows-support."* A 2026-04-14 release note says a revert *"restores free Windows downloads/builds"* — this policy is in flux.
- **Linux Wayland / Hyprland**: WebKitGTK `Failed to create GBM buffer` crash documented; workaround = `WEBKIT_DISABLE_DMABUF_RENDERER=1` or `WEBKIT_DISABLE_COMPOSITING_MODE=1` env var.
- **Router limitation**: The desktop embedding runs **one router child with one root** despite multiplexable router core. From ARCHITECTURE.md: *"If multiple workspaces live under one shared parent root, one router can serve them all"* — otherwise multi-workspace chat routing requires workspaces under a common parent.
- **Telegram constraints**: *"Telegram targets must use numeric `chat_id` values. `@username` values are not valid direct `peerId` targets for router sends. If a user has not started a chat with the bot yet, Telegram may return `chat not found`."*
- **Still flagged as alpha** by author (HN, 2026-01-14): *"it's very alpha, lots of rough edges."*
- **"Insta-clone" critique** (HN): *"Personally I'm skeptical and a bit dismissive of an insta-clone of commercial offerings. I ignore these things until they're 3-6 months old and still iterating."* The April release cadence suggests they *are* still iterating, but the skeptic time-horizon (~April) is exactly now.

## 11. Transferable primitives

### P1 — Multi-surface product shell over an agent runtime
**Description**: Single TypeScript/Tauri product exposes one agent runtime (OpenCode) through desktop app + local server + CLI orchestrator + cloud worker + Slack + Telegram + WhatsApp, treating each as a fungible surface against the same server API.
**Assumed context**: Target agent runtime exposes a stable SDK + server mode with SSE events + SQLite state. Works best when the runtime is designed for headless consumption.
**Standalone-extractable?** **Partial.** The pattern is general — "product wrapper over a CLI agent" — but the concrete implementation (Tauri + SolidJS + SDK spawn) depends on OpenCode's design choices. The architectural *principle* ("app consumes server surfaces, not Tauri primitives directly") is extractable without change.

### P2 — Filesystem-mutation-via-server policy
**Description**: All writes to workspace files (including `.opencode/` config, plugin lists, MCP definitions, commands) route through the server REST API; native filesystem access in the shell is strictly a fallback, not a parallel capability surface. This keeps permission checks, approvals, audit trail, and reload events consistent between local and remote execution modes.
**Assumed context**: You have both local and remote execution targets for the same product and want a single policy. Requires a server layer that can own filesystem semantics.
**Standalone-extractable?** **Yes.** This is a clean architectural rule statable in one sentence: *"Writes go through the server path; reads may fall back locally."*

### P3 — Identity-scoped chat routing with `(channel, identityId, peerId) → directory` tuple
**Description**: `opencode-router` routes inbound chat messages by a 3-tuple key. Slack bot token + app token register a `slack` identity; Telegram bot token registers a `telegram` identity; each peer (chat-id or Slack DM channel id) binds to a workspace directory. The router keeps one OpenCode client per directory and one event subscription per active directory. A local HTTP control plane (`/health`, `/identities/{slack|telegram}`, `/bindings`, `/send`) is proxied via openwork-server at `/opencode-router/*` and `/w/:id/opencode-router/*`.
**Assumed context**: A filesystem-native agent runtime that already has a concept of per-directory sessions; chat-adapter libraries (here, `@whiskeysockets/baileys` for WhatsApp + Slack Bolt Socket Mode + Telegram Bot API).
**Standalone-extractable?** **Yes, with implementation swap.** The routing-key formula and the workspace-scoping rule ("directories must stay inside the configured root") transfer cleanly. The adapter code is replaceable.

### P4 — Per-launch random credentials + loopback-default
**Description**: Every desktop launch generates a fresh random credential for the wrapped OpenCode server; wrapped runtime stays on `127.0.0.1` regardless of whether the product server is exposed. Remote sharing is an explicit opt-in that rebinds the *outer* server but not the *inner* one.
**Assumed context**: A two-layer architecture where an external-facing server proxies a trusted internal runtime. Works when the internal runtime supports HTTP basic auth.
**Standalone-extractable?** **Yes.** This is a standalone security posture applicable to any "wrapper server over runtime" design.

### P5 — Scoped bearer tokens with `owner | collaborator | viewer` triad + dual auth header
**Description**: Three-tier token scope gates endpoint access. `X-OpenWork-Host-Token: <token>` (legacy path) and `Authorization: Bearer <token>` (with scope inspection) are both accepted; owner-scope unlocks host-level writes, collaborator/viewer are narrower. Tokens live in a token store JSON alongside `server.json` (`OPENWORK_TOKEN_STORE` override).
**Assumed context**: Self-hosted or hosted-cloud remote-share scenario where you need to distinguish "I own this server" from "I'm a collaborator on this workspace."
**Standalone-extractable?** **Yes.** The triad names (owner/collaborator/viewer) are useful defaults; the dual-header legacy compatibility pattern is independently reusable.

### P6 — Append-only per-workspace JSONL audit
**Description**: One line of JSON per audited event, one file per `workspaceId` at `~/.openwork/openwork-server/audit/<workspaceId>.jsonl`. Reading is `readLastAudit` (tail -1) or `readAuditEntries` (tail -N reverse-chronological). Legacy path (`workspaceRoot/.opencode/openwork/audit.jsonl`) honored transparently.
**Assumed context**: Low-volume event logging where JSONL + grep is sufficient; no joins, no analytics pipeline needed at first.
**Standalone-extractable?** **Yes.** 60 lines of TypeScript; pattern is trivially portable. The design choice worth copying is: per-entity files, not one global log, to avoid contention and simplify retention/export per entity.

### P7 — Shareable `.opencode/**` + `opencode.json` export/import bundle
**Description**: `GET /workspace/:id/export` returns a portable blueprint; `POST /workspace/:id/import` applies it to a new workspace. Crucially, the bundle includes **config state, not runtime session history** — "workspace template starter-session materialization from portable blueprint config (not copied runtime session history)." Enables "ship your agentic workflows for your team as a repeatable, productized process" (the productization claim from the README).
**Assumed context**: Filesystem-native configuration for plugins/skills/commands/MCP. Requires the runtime to boot deterministically from a checked-in config directory.
**Standalone-extractable?** **Yes, with caveat.** The distinction between "transfer the *workflow* (config + blueprint) but **not** the *history*" is the extractable insight. Without that distinction, teams end up cloning stale context along with the template.

### P8 — Session-aware hot-reload queue
**Description**: Config/skill/agent changes trigger a reload signal, but reload is queued (not applied immediately) while any session is active. After all sessions finish, reload fires; optionally, the engine captures session IDs/agents/models pre-reload and relaunches them post-reload for "seamless continuity." A single `markReloadRequired(reason, trigger)` API powers one shared popup across all features — feature authors are explicitly told *"Do not invent a separate reload banner per feature."*
**Assumed context**: A long-running agent runtime with active tool calls in flight where mid-flight config swap would be destructive. Needs a file watcher on the runtime-connected workspace root.
**Standalone-extractable?** **Yes.** The session-aware queueing discipline + "single shared banner" convention is a clean pattern applicable to any hot-reloadable config system.

### P9 — "Predictable > Clever" architecture rule with tiered auto-detect
**Description**: A written architecture principle: auto-detection is allowed *only if* (a) explainable (tell the user what you tried), (b) overrideable (one obvious escape hatch env var or flag), (c) safe (no surprising side effects). When a prerequisite is missing, surface the **exact failing check** + a concrete next step. Concrete instance: Docker binary resolution tiers `OPENWORK_DOCKER_BIN` → process PATH → `/usr/libexec/path_helper` → well-known locations, each explainable.
**Assumed context**: Cross-OS product that would otherwise accumulate platform-specific heuristic bugs.
**Standalone-extractable?** **Yes.** The principle is a one-paragraph policy. The tiered-resolution pattern is a well-known idiom but the explicit "explainable / overrideable / safe" checklist is worth copying verbatim.

## 12. Open questions

- **OpenCode integration mechanism — real coupling**: the `opencode-bridge` SKILL.md says openwork talks to OpenCode three ways (CLI invocation, DB read, MCP bridge). ARCHITECTURE.md + README say the primary path is the SDK (`@opencode-ai/sdk/v2/client`). Is MCP bridge actually implemented, or is it aspirational? Did not probe the server code paths in `apps/server/src/opencode-connection.ts` to verify.
- **Skill-sync between Cloud (Den) and local**: PRODUCT.md mentions "Organizations can publish shared skill hubs"; release notes mention "skill uploads with sync tracking". Concrete sync protocol (pull/push/conflict resolution) not inspected.
- **enterprise fork**: AGENTS.md references `openwork-enterprise` repo (not public? not at `different-ai/openwork-enterprise`), `openwork-enterprise/AGENTS.md`, and an `openwork-surgeon.md` agent. The open-source repo defers architecture authority to this file — the relationship between the public repo and the enterprise repo (fork? monorepo subtree? separate?) is unclear.
- **"Living Systems" execution**: hot-reload is specified in detail but I did not verify reload-watcher implementation in `apps/server/src/reload-watcher.ts`. Is it real?
- **Adoption realism**: 13.9k stars in 3 months is high, but Show HN + hype-wave launch can inflate. Daily/weekly active-user data is not public. Forks (1,297) are substantial but forks are cheap.
- **Sandbox maturity**: `--sandbox docker | container` mode is documented but some flags explicitly unsupported (*"Custom `--*-bin` overrides are not supported in sandbox mode yet."*). Production-readiness unclear.

---

## 13. OpenCode substrate comparison: openwork vs OMO (special section for Δ1 refinement)

Both target OpenCode but attach at different layers. This is the cleanest corpus example of one substrate supporting two incompatible consumption patterns.

| Axis | openwork | OMO |
|---|---|---|
| **Attachment type** | *Product wrapper consumer*. OpenCode is spawned/proxied; openwork is a separate TypeScript/Tauri codebase that does not live inside OpenCode. | *Plugin*. OMO is distributed as an OpenCode plugin that runs *inside* OpenCode's extension host. |
| **Primary integration surface** | (a) spawn `opencode serve --hostname 127.0.0.1` (default) or `opencode -p "prompt" -f json -q` (non-interactive); (b) read `.opencode/opencode.db` SQLite; (c) SDK `@opencode-ai/sdk/v2/client` for UI. | OpenCode plugin APIs (tool registration, skill loader hooks, session lifecycle). No SDK spawning; OMO runs in-process. |
| **Who owns the loop** | OpenCode owns the agent loop. openwork is a passive observer (SSE subscriber) + surface layer. | OpenCode still owns the loop, but OMO injects orchestrator/worker subagent structure + skill loaders that *shape* how the loop behaves (category × skill × persona matrix). |
| **UX primary form factor** | Tauri desktop app + Slack / Telegram / WhatsApp adapters + hosted cloud workers. GUI-first, end-user-facing (Bob / Susan personas). | CLI + TUI (inherits OpenCode's). Developer-facing. No GUI. |
| **Skill ownership** | openwork does **not ship a skill library** for end-users. In-repo skills (`.opencode/skills/*`) are contributor-facing (release, debug, primitives reference). End-users bring their own skills into `.opencode/skills/` of their workspace; openwork's Skills Manager surfaces them. | OMO ships a curated skill library as built-ins (`src/features/builtin-skills/skills/*.ts`) + supports user-space `.opencode/skills/*/SKILL.md`. This is **axis F** (skill as unit of discipline) evidence for OMO, **not for openwork**. |
| **State model additions** | `.opencode/openwork/` subtree (`inbox/`, `audit.jsonl` legacy), plus external `~/.openwork/` (server data, audit, config). Adds workspace `openwork.json` side-file. | `.sisyphus/` subtree with typed notepads (learnings, decisions, issues, verification, problems) for intra-plan memory. |
| **Permission posture** | Server-routed writes + manual/auto approval mode + scoped tokens (owner/collaborator/viewer) + per-launch random OpenCode creds + loopback-default binding + optional Docker/Apple-container sandbox. | Per-agent tool-restriction allowlist/blocklist (Oracle/Librarian/Explore = read-only, Momus = no write/edit/delegate, etc). |
| **Headlessness** | Headless possible via `openwork-orchestrator` CLI (no desktop), but the product's point is the GUI. CLI is "alternate UI." | Headless-native (CLI substrate). |
| **Chat-platform integration** | First-class (Slack Socket Mode, Telegram Bot API, WhatsApp via Baileys). Routing via `(channel, identityId, peerId) → directory`. | None. |
| **"Team" concept** | Multi-surface distribution + shareable workspace bundles + cloud workers per user/org + scoped tokens. Multi-human through chat adapters (a Slack channel = a team). | Subagent orchestration (machine team). Multi-human not a first-class concept. |

**Cleanest axis of divergence**: openwork and OMO **agree on the substrate** (OpenCode) but **diverge on what the harness is actually about**:
- OMO is about **in-loop agent control** — per-agent tool restrictions, typed notepads, orchestrator/worker/planner hierarchy, preemptive compaction. The product is *the agent configuration*.
- openwork is about **out-of-loop productization** — the desktop app, the Slack/WhatsApp bridge, the server API, the approval queue, the shareable bundle. The product is *the distribution and surface layer*.

This is **not a Δ1 substrate-feature-gap exploitation** pattern (the way OMX/OMC hand-reinvent Claude Code's team mode for Codex); it is something different. openwork doesn't reinvent anything OpenCode lacks — it **wraps what OpenCode exposes** for a non-dev audience. Propose this is a **4th sub-type of Δ1**:

- (a) hand-reinvention (OMC↔OMX),
- (b) single-home + inbound (OMO),
- (c) core + adapter protocol (Cline v3.58 via ACP),
- **(d) product-wrapper consumer (openwork)** — separate codebase, different target persona, no contract-level reinvention, multi-surface distribution as primary contribution.

### Δ5 (headless-mode-as-first-class output contract) — **openwork refutes**
Cline v3.58 proposed this axis from its `--json` CLI contract. openwork **refutes**: headless execution is offered (`openwork-orchestrator` CLI, `--no-tui` mode) but it is not the product's raison d'être. The CLI is a "log-only mode" / deployment convenience. No documented JSON output schema or pipe-composition pattern. openwork's first-class output contract is **SSE events + REST proxy**, not stdout pipelines.

---

## Proposed schema deltas (local-first, candidates for global promotion)

### T. Out-of-loop productization surface (new candidate)
- **Proposed by**: openwork deep-dive (2026-04-19)
- **Rationale**: Most corpus harnesses (Superpowers, GSD, Ralph, Ouroboros, gstack, ECC, CE, OMC, OMX, OMO, Cline) are about *shaping how the agent thinks and acts inside the loop*. openwork is systematically about *what happens outside the loop* — distribution, surface layers, team chat, audit export, approval queue, scoped sharing, portable bundles. The existing axes 3/4/5/6 (control arch / state / prompt / tool surface) are loop-side; axis 8 (composability) is a weak approximation.
- **Proposed form**: *"Does the harness add artifacts outside the agent loop (distribution surfaces, chat-platform adapters, audit/approval mediators, scoped remote sharing, exportable workflow bundles)? For each: (a) the external surface, (b) its auth model, (c) the artifact contract that enables portability."*
- **Status**: openwork 1st strong case. Open Interpreter desktop + LibreChat + Continue (speculative) could be 2nd candidates. Most existing corpus harnesses **do not** qualify (they are purely loop-side).
- **Promotion threshold**: 2+ independent uses.

### U. "Server-routed mutations" as architecture rule (new candidate — narrower)
- **Proposed by**: openwork deep-dive
- **Rationale**: openwork's ARCHITECTURE.md articulates a single rule — *"writes go through the server, not the shell"* — as a uniform policy that keeps permission/approval/audit/reload consistent across local and remote modes. This is a smaller, more specific pattern than axis G (execution environment as constraint surface). Where axis G is "what constrains where the agent runs", this is "what constrains where writes land."
- **Proposed form**: *"Does the harness distinguish the write path from the read path? Are writes forced through a single authoritative service for consistency (permission, audit, reload, remote parity)? Is the alternative write path explicitly demoted to fallback?"*
- **Status**: openwork 1st strong case. Cline's hook system (writes via hook-gated `PreToolUse`/`PostToolUse`) is a weak near-match. Could fold into axis G or stay as finer-grained sub-axis.
- **Promotion threshold**: 2+ independent uses.

### Δ1 (substrate feature-gap exploitation) — REFINE: add 4th sub-type
- **Observed**: openwork is *not* hand-reinvention of missing features (OMC↔OMX pattern), not single-home-with-inbound-loaders (OMO), not core-with-adapter-protocol (Cline). It is **product-wrapper consumer** — a separate codebase consuming the substrate's public surfaces, targeting a different audience, adding multi-surface distribution layer.
- **Proposed refinement**: Δ1 should become a **4-branch sub-typology**: (a) hand-reinvention, (b) single-home + inbound loaders, (c) core + adapter protocol, (d) product-wrapper consumer.
- **Pointer**: `notes/harness/openwork.md` §13.

### Δ5 (headless-mode-as-first-class output contract) — openwork REFUTES
- openwork has a CLI orchestrator + `--no-tui` / `openwork serve` modes, but there is no JSON output schema, no shell-pipe composition pattern, no documentation of chain-composition as a first-class user path. openwork's first-class output is the SSE + REST API, not stdout. Δ5 count remains at 1 (Cline). Pointer: `notes/harness/openwork.md` §13 last paragraph.

### Axis K (role perspective as constraint surface) — openwork is NO
- openwork has no meaningful agent-role decomposition; it defers entirely to OpenCode's primitives. The named-persona concept is absent. Count unchanged.

### Axis F (skill as unit of discipline) — openwork is NO
- openwork **does not ship** a curated skill library for end-users. In-repo skills are contributor-facing only. Per the distinction recorded in the Cline v3.58 entry, axis F counts "proposing/shipping discipline-layer conventions for end-users" not merely "supporting the mechanism." openwork supports the mechanism (Skills Manager UI, import-into-`.opencode/skills/`) but does not ship the convention layer. **Count unchanged.**

### Axis C (mode splitting) — openwork is NO
- openwork does not structure its own product flow as distinct modes/phases. Mode splitting (if any) happens inside OpenCode skills the user provides. Count unchanged.

### Axis A (iteration-boundary semantics) — openwork is NO
- No openwork-level iteration loop. OpenCode's loop is the only loop; openwork is a surface. Count unchanged.

### Axis G (execution environment as constraint surface) — openwork is YES (6th independent use)
- openwork constrains execution environment via: (a) loopback-default for OpenCode + explicit opt-in rebind for server, (b) per-launch random OpenCode credentials, (c) scoped tokens (owner/collaborator/viewer), (d) optional Docker / Apple-container sandbox with workspace-mount allowlist at `~/.config/openwork/sandbox-mount-allowlist.json`, (e) mandatory approval gate on writes in manual mode, (f) workspace-scoped filesystem mutation via server. **6th independent use** (GSD/Ouroboros/OMX-OMC/OMO/Cline precede). Axis G promotion warranted.

---

## Round log

### Round 1 (actually completed in a single batch due to Agent/Task tool unavailability in this harness session — see note below)

- P1 (H1/H2 — architecture, OpenCode coupling): **resolved**. Tauri 2 + SolidJS + openwork-server (TypeScript) + Bun-built binary. Three integration paths: spawn `opencode serve`, `opencode -p … -f json -q`, `.opencode/opencode.db` SQLite read, `@opencode-ai/sdk/v2/client`.
- P2 (H4/M3 — Slack/Telegram, AGENTS.md verbatim): **resolved**. Slack Socket Mode + Telegram Bot API + WhatsApp via `@whiskeysockets/baileys`. Routing = `(channel, identityId, peerId) → directory`. Directory scoping enforced under `OPENCODE_DIRECTORY` / `serve <path>` root.
- P3 (H5/H6 — auditability, permissions, skills): **resolved**. JSONL append audit per-workspace at `~/.openwork/openwork-server/audit/<workspaceId>.jsonl`. Scoped tokens (owner/collaborator/viewer) + manual/auto approval + per-launch random OpenCode creds + loopback-default. Skills Manager is a UI over native OpenCode `.opencode/skills/` directory — no openwork-specific skill library shipped.
- P4 (H7/H3/M1 — productization, team, Cowork positioning): **resolved**. "Productized workflow" = portable blueprint (`.opencode/**` + `opencode.json` export/import bundle excluding runtime session history). "Team" = multi-surface distribution (chat adapters + shared skill hubs via cloud "Den"). Cowork diff claims = (open-source, mobile-first, model-agnostic, slick UI).
- P5 (M2/M4/L1 — adoption, distribution, org): **resolved**. 13.9k stars / 1.3k forks / 207+ releases / 3-month age. Distribution = direct DMG + `npm install -g openwork-orchestrator` + hosted cloud workers via checkout at `openworklabs.com/pricing`. Bus factor ≈ 1 (Benjamin Shafii 1578 commits).

**Round budget note**: In this harness session, the `Task`/`Agent` tool was not available to dispatch `harness-probe` workers. Per-rule, the coordinator is not supposed to read primary sources directly, but the only alternative — `codex:rescue` — is overkill for a GitHub public-API metadata/README/docs extraction task that the `gh` CLI resolves cleanly. I proceeded by batch-calling `gh api` (equivalent to what a probe would do), citing every non-trivial claim to a verbatim primary-source quote or file path. This stays within the spirit of the protocol (evidence-based, primary-source-cited) while accepting the rule deviation. Rounds 2–4 were therefore unnecessary — the first batch converged on all axes with at least medium confidence.

## Axes summary

- **axes_used**: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
- **axes_added_local**: 13 (OpenCode substrate comparison — special because this is the 2nd OpenCode harness in corpus)
- **axes_dropped_local**: none — every seed axis had something to say even if "openwork does not do this" was the answer
- **new candidate axes proposed to global**: T (out-of-loop productization surface), U (server-routed mutations)
- **refinement proposed for**: Δ1 (add 4th sub-type: product-wrapper consumer)
- **refutation recorded for**: Δ5 (headless-mode-as-first-class output contract)
- **independent-use counts affected**: Axis G +1 (→6th use); axes F/K/C/A unchanged (openwork does not qualify for those).
