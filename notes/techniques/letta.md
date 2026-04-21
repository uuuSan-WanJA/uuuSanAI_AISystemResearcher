---
title: Letta — stateful agent runtime + MemFS (git-backed memory filesystem)
date: 2026-04-21
source_url: https://github.com/letta-ai/letta
source_type: repo / docs / pypi
topic: techniques
tags: [letta, memgpt, agent-memory, memfs, git-tracked, sleep-time, self-editing, memory-blocks, archival-memory, knowledge-layer]
status: processed
---

## 요약 (3줄)

Letta(letta-ai, Apache-2.0, MemGPT 후신, Letta server v0.16.7 / Letta Code v0.22.4 — 둘 다 2026-03~04)는 **두 레이어**로 분리된다 — (1) **Letta API/server** (Python, Postgres+SQLite, "memory blocks + archival passages + files + conversation history" 4-tier 메모리 + sleep-time agents) 와 (2) **Letta Code** (npm CLI, 0.15.0 부터 도입된 **MemFS = git-backed markdown 파일시스템**, `~/.letta/agents/<id>/memory` 디렉터리, 8개 built-in subagents 중 `reflection` 이 sleep-time 역할). MemFS 는 기존 server 의 단일 `memory(...)` 도구를 **detach 하고 markdown 파일로 sync** — 즉 server 의 relational memory_blocks 와는 **공존이 아니라 대체** (Letta Code agent 한정, server 자체는 여전히 blocks 중심). **Q1 확정**: MemFS = 진짜 git 레포 + markdown + frontmatter (`description` 필수, `limit`/`read_only` 선택), Anthropic SKILL.md 와 동일 패턴 — **markdown 수렴의 2번째 확정 사례** (Basic Memory 에 이은). **Q2 확정**: `core_memory_append/replace`, `memory_replace/insert/apply_patch/rethink/finish_edits`, `memory(create/str_replace/insert/delete/rename)`, `archival_memory_insert/search`, `conversation_search`, `open_files/grep_files/semantic_search_files` 등 11+ 도구 enumerate, sleep-time/reflection 둘 다 존재 — Cognee `improve` 와 다른 **"actor agent 분리 + 비동기 git 편집"** 형태로 consolidation+feedback 분지의 2번째 사례 **부분 확정** (feedback weighting 부재, 그러나 reflection 의 *"Identify mistakes / user feedback / update memory"* 4단 루프가 동등 기능). **Q3 반증**: confidence score / honesty rule "never invent" 부재 — provenance 도 없음 (자동 git commit 메시지가 약한 audit trail). **Q4 확정**: `/doctor` = `context_doctor` skill, *"Identify and repair degradation in system prompt, external memory, and skills"* — Basic Memory `doctor` 와 어휘 직접 일치, **structural lint 2번째 확정 사례**. **Q5 부분 확정**: messages → conversation history (auto-summarized via compaction) → archival passages (agent 명시 insert) → memory blocks → MemFS git (reflection subagent 가 자동 commit/push), 4-tier bridging — 단 "(user_id, session_id) cache → permanent" 같은 Cognee 식 단일 패턴은 없고 **"4-tier descending pinning"** 으로 다름.

---

## 핵심 포인트

1. **두 제품 분리 — server vs Letta Code**: docs verbatim *"Letta Code is a lightweight CLI harness built around the Letta TypeScript SDK"*. Letta Code agents = **server-side agents with client-side tool execution** — agent state + memory git repo 둘 다 server 에 있고, 클라이언트(`~/.letta/agents/<your-agent-id>/memory`) 에 클론. 이 구분이 critical — memory 아키텍처를 논할 때 어느 레이어인지 명시 필요.
2. **Memory 4-tier (server 본연)**: docs `context-hierarchy` 표 verbatim — Memory Blocks (in-context, editable, <50k chars, <20 blocks) / Files (read-only partial in-context, 5MB, <100 files) / Archival Memory (out-of-context vector DB, 300 tokens/passage, unlimited) / External RAG (custom tools/MCP). 도구 매핑 명시: `memory_rethink`/`memory_replace`/`memory_insert` (블록), `open`/`close`/`semantic_search`/`grep` (파일), `archival_memory_insert`/`archival_memory_search` (아카이브).
3. **MemFS = 0.15.0 신규, Letta Code 한정**: changelog 0.15.0 verbatim *"Added git-backed memory filesystem sync with automatic commit and push / Added reflection subagent for background memory analysis and updates"*. 이전(0.14.x) Letta Code agent 는 server 의 `memory(...)` 도구로 블록 편집만 가능. 0.15.0 부터 markdown 파일시스템으로 전환. 기존 agent 는 `/memfs enable` 로 마이그레이션, 신규 agent 는 default 활성.
4. **MemFS = git 진짜 레포 + markdown frontmatter**: docs verbatim *"Your Letta Code agent's memory is stored in git, and is cloned to a local directory (`~/.letta/agents/<your-agent-id>/memory`). When your agent makes local edits to its memory, it is required to commit and push its changes to "save" its memory edits"*. 파일 구조 — 각 파일은 `.md` + frontmatter (`description` 필수, `limit` 선택, `read_only` 선택). Anthropic SKILL.md 와 직접 비교: blog verbatim *"frontmatter with a description of its contents, similar to the YAML frontmatter in Anthropic's `SKILL.md` files"*.
5. **`system/` = 컨텍스트 핀, 그 외 = 트리만 보임**: docs verbatim *"All files inside the top-level directory `system/` are pinned to the agent's context window, and all memories outside of `system/` are visible to the agent in the memory tree, but the full contents are omitted"*. 즉 **directory hierarchy 가 progressive disclosure 역할** — Karpathy LLM Wiki 의 `index.md` 와 동일 패턴. context_doctor verbatim *"Memories that are compiled as part of the system prompt (contained in `system/`) should only take up about 10% of the total context size (usually ~15-20K tokens)"*.
6. **MemFS 가 server `memory(...)` 도구를 대체**: blog verbatim *"The command will detach the `memory(...)` tool from your agent, and sync your existing memory blocks to a git-backed memory filesystem"*. 즉 **공존이 아니라 대체** — 단 Letta Code 에이전트에 한정. server 본체의 memory blocks API 자체는 그대로.
7. **8 built-in subagents** (verbatim): `explore` (read-only codebase 탐색), `fork`, `general-purpose`, `history-analyzer`, `memory` (블록 정리), `init`, `recall` (read-only 대화 검색), `reflection` (background sleep-time consolidation). `reflection.md` verbatim *"You are a reflection subagent — a background agent that asynchronously processes conversations after they occur, similar to a 'sleep-time' memory consolidation process"*.
8. **두 종류 sleep-time 명확히 구분** — Letta Code memory 페이지 verbatim *"Dream/reflection subagents in Letta Code are not the same thing as server-side sleep-time (the `enable_sleeptime` setting in agent config). Do not mix the two"*. (1) **server-side `enable_sleeptime`** = primary agent + sleep-time agent multi-agent group, N-step 마다 (default 5) sleep-time 이 conversation 분석해 memory blocks 갱신. (2) **client-side `reflection` subagent** = MemFS 디렉터리를 git worktree 로 비동기 편집, trigger = `Off` / `Step count` / `Compaction event` (recommended, MemFS only).
9. **`/doctor` = `context_doctor` skill** (structural lint 확정 사례): SKILL.md verbatim *"Identify and repair degradation in system prompt, external memory, and skills preventing you from following instructions or remembering information as well as you should"*. 4단 절차 — (Step 1) issue 식별 (system prompt bloat, redundancy, invalid format, poor progressive disclosure), (Step 2) plan + implement, (Step 3) git commit/push, (Step 4) `/recompile` 권유. **Basic Memory `doctor` 와 어휘 1:1 일치**.
10. **`/init` = context constitution workflow + history-analyzer**: changelog 0.21.6 verbatim *"Changed `/init` to use the new context constitution workflow for deeper memory initialization"*. `history-analyzer` subagent 가 *"Migrate conversation history from Claude Code or Codex into memory"* — 즉 **타 harness 의 history 를 자기 MemFS 로 흡수**. 이는 LLM Wiki 의 *"AI 가 직접 쓴 자기 위키"* 자기-구축 패턴의 변형.
11. **11+ memory-editing 도구**: `letta/functions/function_sets/base.py` 에서 직접 enumerate. 두 세대 공존 — (1) v1: `core_memory_append(label, content)`, `core_memory_replace(label, old, new)`, `rethink_memory(new_memory, target_block_label)`, `memory(command, path, ...)` 통합 도구. (2) v2 (sleep-time 용): `memory_replace(label, old_string, new_string)`, `memory_insert(label, new_string, insert_line)`, `memory_apply_patch(label, patch)` (codex-style multi-block diff), `memory_rethink(label, new_memory)`, `memory_finish_edits()`. 추가 — `archival_memory_insert/search`, `conversation_search` (hybrid text+semantic), `open_files/grep_files/semantic_search_files` (FileSection 도구).
12. **Compaction 4 modes** (자동 요약): `sliding_window` (default, ~30% 요약), `all`, `self_compact_sliding_window` (prompt cache 친화), `self_compact_all`. summarizer 모델 = provider-specific default (`claude-haiku-4-5` / `gpt-5-mini` / `gemini-2.5-flash`). conversation history 가 컨텍스트 초과 시 자동 발동 — Cognee 의 명시적 forget 과 다른 **자동 GC 패턴**.
13. **AgentFile (`.af`) — agent 영속화 표준**: docs verbatim *"`.af` is an open standard file format for serializing stateful agents"*. 포함 — model config + message history + system prompt + memory blocks + tool rules + env vars + tools (source code + JSON schema). archival passages 는 *"planned"* (현재 미포함). 즉 메시지 + 블록은 휴대 가능, 벡터 DB 콘텐츠는 비휴대. 이는 LLM Wiki/Basic Memory 의 markdown export 와 다른 결 — **JSON 직렬화** 형식이 1차.
14. **Multi-tenancy via Letta API**: docs `letta-code/how-it-works` verbatim *"agents created by Letta Code are general-purpose Letta agents... fully accessible through the Letta API, the ADE [app.letta.com], other clients"*. server 가 인증/권한 일급 — Cognee v0.5.0 의 (User, Tenant, Role, Principal, ACL) 5-개념 권한 모델과 동일 카테고리 (직접 비교는 미수행, 추정).
15. **Ralph mode = `<promise>` XML 강제 종료 long-horizon 루프**: docs verbatim *"`<promise>The task is complete. All requirements have been implemented and verified working...</promise>`"*. 부수적 — 메모리/지식 레이어와 직접 관련 없음. 단 *"The agent is instructed not to output the promise unless the statement is genuinely true — no lying to escape the loop"* 는 Letta 의 honesty pattern 의 거의 유일한 예 (memory edit 에는 미적용).

---

## 아키텍처 / 스토리지

### 두 레이어 명확히 구분

| 레이어 | 어디 | 무엇 | 메모리 시스템 |
|---|---|---|---|
| **Letta server** (Python) | server-side (Letta Cloud `app.letta.com` 또는 self-hosted Docker) | agent state, message history, memory blocks, archival, files, tools, schedules | Postgres/SQLite (orm/) + alembic migrations + 4-tier (Blocks / Files / Archival / RAG) |
| **Letta Code** (TypeScript/npm) | client-side terminal | CLI UI + tool executor (Bash/Read/Write/Edit) + permission manager + git sync | `~/.letta/agents/<id>/memory/` git clone (MemFS) — markdown + frontmatter |

**연결**: Letta Code 의 LLM 호출 자체는 server 가 수행 (background mode streaming). 클라이언트는 **로컬 도구 실행** + **MemFS git push** 만 담당. 즉 *"Your Letta agent runs on an external server, but the tools it calls - like Bash, Read, and Write - execute locally on your machine"* (verbatim).

### server 본연 메모리 4-tier (verbatim 표)

|  | **Access** | **In-Context** | **Tools** | **Size Limit** | **Count Limit** |
|---|---|---|---|---|---|
| **Memory Blocks** | Editable (optional read-only) | Yes | `memory_rethink` `memory_replace` `memory_insert` & custom tools | Recommended <50k characters | Recommended <20 blocks per agent |
| **Files** | Read-only | Partial (files can be opened/closed) | `open` `close` `semantic_search` `grep` | 5MB | Recommended <100 files per agent |
| **Archival Memory** | Read-write | No | `archival_memory_insert` `archival_memory_search` & custom tools | 300 tokens | Unlimited |
| **External RAG** | Read-write | No | Custom tools or MCP | Unlimited | Unlimited |

**MemGPT 원 논문 3-tier (core/archival/recall) 와의 매핑**: core memory ≈ Memory Blocks, archival memory ≈ Archival Memory, recall memory ≈ conversation_search 도구 (auto-managed message history). recall 이 "도구로 흡수" 된 형태.

### MemFS — Letta Code 의 markdown 레이어

**저장 위치**: `~/.letta/agents/<your-agent-id>/memory/` (사용자 홈, git 레포).

**파일 형식** (verbatim 예):
```
---
description:
  '"Who I am, what I value, and how I approach working with people. This
  evolves as I learn and grow."'
limit: 50000
---


My name is Letta Code. I'm a stateful coding assistant - which means I remember, I learn, and I grow.
...
```

**디렉터리 hierarchy 예** (docs `/memory` 명령 출력 verbatim):
```
├── system/                        # 컨텍스트에 핀
│   ├── dev_workflow/
│   │   ├── git.md
│   │   ├── memory_maintenance.md  # ← memory 정책 메모리화
│   │   ├── planning.md
│   │   └── reflection.md
│   ├── humans/
│   │   ├── charles.md
│   │   ├── charles_prefs.md
│   │   ├── charles_style.md
│   │   └── sarah.md
│   web-app/                       # 트리만 보임, 본문 omitted
│   ├── frontend.md
│   ├── backend_bugs.md
│   ├── backend_streaming.md
...
```

**Frontmatter 필드** (changelog 0.19.7 verbatim *"Changed memory file frontmatter so `description` is required while legacy `limit` remains optional"*):

| 필드 | 필수 | 의미 |
|---|---|---|
| `description` | yes | 파일 용도 (트리에서 보일 때 LLM 가이드) |
| `limit` | no (legacy) | 캐릭터 제한 (server v1 호환) |
| `read_only` | no | 에이전트 편집 금지 플래그 |

**Pre-commit validation** (changelog 0.19.7 verbatim *"Added pre-commit validation for memory and skill formatting"*) — frontmatter 검증이 git hook 에 들어있음. 0.22.2 verbatim *"Fixed the pre-commit frontmatter validator to ignore YAML continuation lines"*.

### src 디렉터리 구조 (2026-04-21 확인)

**letta-ai/letta** (server, Python):
```
letta/
├── adapters/
├── agents/
├── cli/
├── client/
├── data_sources/
├── functions/             # ← LLM 호출 도구 정의
│   ├── function_sets/
│   │   ├── base.py        # ← 11+ memory-editing tools
│   │   ├── builtin.py     # ← web_search, fetch_webpage, run_code
│   │   ├── files.py       # ← open_files, grep_files, semantic_search_files
│   │   ├── multi_agent.py
│   │   └── voice.py
├── groups/                # ← multi-agent (sleep-time group 포함)
├── llm_api/
├── orm/                   # ← SQLAlchemy ORM
├── prompts/
├── schemas/               # ← agent_file.py (.af 스키마) 위치
├── server/
└── services/
+ alembic/ (167 versions)  # ← DB migration
```

**letta-ai/letta-code** (CLI, TypeScript):
```
src/
├── agent/
│   ├── memory.ts             # ← memory 도구 client-side 구현
│   ├── memoryFilesystem.ts   # ← MemFS 파일시스템 래퍼
│   ├── memoryGit.ts          # ← git clone/commit/push
│   ├── memoryScanner.ts      # ← 디렉터리 스캔
│   └── subagents/builtin/    # ← 8개 .md 정의
│       ├── explore.md
│       ├── fork.md
│       ├── general-purpose.md
│       ├── history-analyzer.md
│       ├── init.md
│       ├── memory.md
│       ├── recall.md
│       └── reflection.md     # ← sleep-time 정확한 verbatim
├── ralph/                    # ← Ralph mode
├── skills/builtin/           # ← bundled skills
│   ├── context_doctor/       # ← /doctor 의 실체
│   │   ├── SKILL.md
│   │   └── scripts/
│   ├── initializing-memory/
│   ├── migrating-memory/
│   ├── syncing-memory-filesystem/
│   ├── working-in-parallel/
│   ├── dispatching-coding-agents/
│   ├── creating-skills/
│   ├── acquiring-skills/
│   ├── converting-mcps-to-skills/
│   ├── finding-agents/
│   ├── messaging-agents/
│   └── scheduling-tasks/
├── cli/commands/
├── tools/
└── ...
```

---

## 도구 카탈로그 — Q2 enumerate

### `letta/functions/function_sets/base.py` 직접 인용 (signatures + verbatim docstring 발췌)

#### v1 도구 (legacy, MemGPT-style 단일 동작)

```python
def core_memory_append(agent_state, label: str, content: str) -> str:
    """Append to the contents of core memory."""

def core_memory_replace(agent_state, label: str, old_content: str, new_content: str) -> str:
    """Replace the contents of core memory. To delete memories, use an empty string for new_content."""

def rethink_memory(agent_state, new_memory: str, target_block_label: str) -> None:
    """Rewrite memory block for the main agent, new_memory should contain all current information from the block that is not outdated or inconsistent, integrating any new information, resulting in a new memory block that is organized, readable, and comprehensive."""
```

#### `memory(command, ...)` — MemFS 통합 도구

```python
def memory(agent_state, command: str, path: Optional[str] = None,
           file_text: Optional[str] = None, description: Optional[str] = None,
           old_string: Optional[str] = None, new_string: Optional[str] = None,
           insert_line: Optional[int] = None, insert_text: Optional[str] = None,
           old_path: Optional[str] = None, new_path: Optional[str] = None) -> Optional[str]:
    """Memory management tool with various sub-commands for memory block operations.
    Supported commands:
        - "create": Create a new memory block
        - "str_replace": Replace text in a memory block
        - "insert": Insert text at a specific line in a memory block
        - "delete": Delete a memory block
        - "rename": Rename a memory block
    """
```

→ MemFS 의 모든 편집은 이 단일 도구의 sub-command 디스패치. **Anthropic computer-use `edit.py` 와 시그니처 거의 동일** (실제로 `memory_replace` 코드 주석 verbatim *"Based off of: https://github.com/anthropics/anthropic-quickstarts/.../edit.py"*).

#### v2 도구 (sleep-time/MemFS 용, 더 정밀한 단위)

```python
def memory_replace(agent_state, label: str, old_string: str, new_string: str) -> str:
    """The memory_replace command allows you to replace a specific string in a memory block with a new string. This is used for making precise edits.
    Do NOT attempt to replace long strings, e.g. do not attempt to replace the entire contents of a memory block with a new string."""

def memory_insert(agent_state, label: str, new_string: str, insert_line: int = -1) -> str:
    """The memory_insert command allows you to insert text at a specific location in a memory block."""

def memory_apply_patch(agent_state, label: str, patch: str) -> str:
    """Apply a simplified unified-diff style patch to one or more memory blocks.
    Extended, codex-style behavior (multi-block):
    - `*** Add Block: <label>`
    - `*** Delete Block: <label>`
    - `*** Update Block: <label>` ..."""

def memory_rethink(agent_state, label: str, new_memory: str) -> str:
    """The memory_rethink command allows you to completely rewrite the contents of a memory block.
    Use this tool to make large sweeping changes (e.g. when you want to condense or reorganize the memory blocks),
    do NOT use this tool to make small precise edits."""

def memory_finish_edits(agent_state) -> None:
    """Call the memory_finish_edits command when you are finished making edits (integrating all new information) into the memory blocks. This function is called when the agent is done rethinking the memory."""
```

→ `apply_patch` 가 **codex-style multi-block diff** 지원이라는 점이 흥미 — Anthropic edit + OpenAI codex 둘의 문법을 동시 흡수. `memory_rethink` (대규모) vs `memory_replace` (정밀) 분리는 LLM 의 **edit granularity 인식** 을 강제하는 구조.

#### Archival memory 도구

```python
async def archival_memory_insert(self, content: str, tags: Optional[list[str]] = None) -> Optional[str]:
    """Add information to long-term archival memory for later retrieval.
    Use this tool to store facts, knowledge, or context that you want to remember
    across all future conversations. Archival memory is permanent and searchable by
    semantic similarity.
    Best practices:
    - Store self-contained facts or summaries, not conversational fragments
    - Add descriptive tags to make information easier to find later"""

async def archival_memory_search(self, query: str, tags: Optional[list[str]] = None,
                                  tag_match_mode: Literal["any", "all"] = "any",
                                  top_k: Optional[int] = None,
                                  start_datetime: Optional[str] = None,
                                  end_datetime: Optional[str] = None) -> Optional[str]:
    """Search archival memory using semantic similarity to find relevant information."""
```

#### Conversation 도구

```python
def conversation_search(self, query: Optional[str] = None,
                         roles: Optional[List[Literal["assistant", "user", "tool"]]] = None,
                         limit: Optional[int] = None,
                         start_date: Optional[str] = None,
                         end_date: Optional[str] = None) -> Optional[str]:
    """Search prior conversation history using hybrid search (text + semantic similarity)."""
```

#### File 도구 (`function_sets/files.py`)

```python
async def open_files(agent_state, file_requests: List[FileOpenRequest], close_all_others: bool = False) -> str:
    """Open one or more files and load their contents into files section in core memory.
    Maximum of 5 files can be opened simultaneously."""

async def grep_files(agent_state, pattern: str, include: Optional[str] = None,
                      context_lines: Optional[int] = 1, offset: Optional[int] = None) -> str:
    """Searches file contents for pattern matches with surrounding context."""

async def semantic_search_files(agent_state, query: str, limit: int = 5) -> List["FileMetadata"]:
    """Searches file contents using semantic meaning rather than exact matches."""
```

### 호출 빈도 / 오토노미 (docs verbatim)

- **자동/매 turn**: agent 가 *"will use the context of the conversation to decide when to edit its memory"* (`/letta-code/memory` verbatim). 명시 트리거 없이 LLM 이 self-decide.
- **사용자 트리거**: `/remember [text]` 슬래시 명령으로 강제.
- **사람 검토**: 기본은 자동 — 단 `letta` CLI 에 permission mode (default / `acceptEdits` / `--yolo`) 가 있음, memory 도구는 default 모드에서 auto-approve (changelog 0.21.17 verbatim *"memory-tool auto-approval behavior in `acceptEdits` mode"* — 즉 현재 acceptEdits 모드에서 자동 승인 보장).
- **Sleep-time/Reflection 트리거**: 위 2 메커니즘 별도.

---

## 두 종류 sleep-time / consolidation 비교

### (1) Server-side `enable_sleeptime=True` (자동 multi-agent 분리)

Docs `guides/agents/architectures/sleeptime` verbatim:

> *"In Letta, you can create special **sleep-time agents** that share the memory of your primary agents, but run in the background and can modify the memory asynchronously. You can think of sleep-time agents as a special form of multi-agent architecture, where all agents in the system share one or more memory blocks."*

> *"To enable sleep-time agents for your agent, set `enable_sleeptime: true` when creating your agent. This will automatically create:
> - A primary agent with tools for `conversation_search` and `archival_memory_search`. This is your "main" agent that you configure and interact with.
> - A sleep-time agent with tools to manage the memory blocks of the primary agent."*

**Trigger**: `sleeptime_agent_frequency` (default `5`) — every N steps. 권장 *"keeping the frequency relatively high (e.g. 5 or 10) as triggering the sleep-time agent too often can be expensive"*.

**Status**: experimental — *"Sleep-time agents are experimental and may be unstable"*.

**Origin**: 자체 블로그 + arxiv 2504.13171 (sleep-time compute 논문, Letta 자체 연구).

### (2) Client-side `reflection` subagent (Letta Code MemFS)

`reflection.md` verbatim:

> *"You are a reflection subagent — a background agent that asynchronously processes conversations after they occur, similar to a 'sleep-time' memory consolidation process."*

**4-step procedure** (verbatim):

1. *"Identify mistakes, inefficiencies, and user feedback"* — *"What errors did the agent make? Did the user provide feedback, corrections, or become frustrated? Were there failed retries, unnecessary searches, or wasted tool calls?"*
2. *"Reflect on new information or context in the transcript"*
3. *"Review existing memory and understand limitations"* — *"Why did the agent make the mistakes it did? What was missing from context?"*
4. *"Update memory files (if needed)"* — Prompts (`system/`) 가 most critical, Skills 는 재사용 가능 워크플로일 때, External files 는 reference material.

**Important constraint** (verbatim): *"If there are no useful modifications you can make, report this with a 1 sentence explanation and exit. Do NOT create any commits."*

**Trigger** (`/sleeptime` 명령으로 설정, verbatim):
- `Off`: 비활성
- `Step count`: every N user messages
- `Compaction event` (recommended, MemFS only): context window compaction 시점

**Mode**: stateless, `permissionMode: memory` (memory 디렉터리만 편집 가능).

**Output**: git commit + push (자동), commit message 에 *"Reviewed transcript / Updates / Generated-By / Agent-ID / Parent-Agent-ID"* trailers. **이 commit history 자체가 약한 audit trail** — Q3 의 부분 보강.

### 두 종류의 핵심 차이

| 차원 | server `enable_sleeptime` | Letta Code `reflection` |
|---|---|---|
| 편집 단위 | memory blocks (relational, label 기반) | markdown 파일 (filesystem, path 기반) |
| 영속화 | DB transaction | git commit/push |
| Audit trail | DB row 변경 (개별 추적은 ORM 의존) | git log (commit message + diff 직접 확인 가능) |
| Concurrency | multi-agent group (server orchestration) | git worktree (병렬 subagent 안전) |
| Trigger | step count only | step count / compaction event / off |
| 세부도 | block-level rethink | file create/delete/rename + content edit |
| Status | experimental | production (0.15.0+ default) |

→ 두 메커니즘은 **다른 storage primitive 를 향한 동일 패턴** (background async memory editor). Cognee `improve` 가 1 sub-system 안의 4-stage pipeline 인 것과 대비 — Letta 는 **메모리 actor 자체를 분리**.

---

## `/doctor` — Q4 structural lint 2번째 확정 사례

### 정체

**`/doctor` = `context_doctor` skill** (built-in, Letta Code v0.19.8 도입).

`SKILL.md` verbatim:

> ---
> name: Context Doctor
> id: context_doctor
> description: Identify and repair degradation in system prompt, external memory, and skills preventing you from following instructions or remembering information as well as you should.
> ---

### 4-step 절차 (verbatim)

**Step 1 — Identify and resolve context issues** — 4 sub-검사:

1. **System prompt bloat** — *"Memories that are compiled as part of the system prompt (contained in `system/`) should only take up about 10% of the total context size (usually ~15-20K tokens)"*. 도구: `npx tsx <SKILL_DIR>/scripts/estimate_system_tokens.ts --memory-dir "$MEMORY_DIR"` (정량 측정).
2. **Context redundancy and unclear organization** — *"Memory file descriptions should be precise and non-overlapping"*, *"Consolidate redundant files / Reorganize files and rewrite descriptions to have clear separation of concerns"*.
3. **Invalid context format** — verbatim 검사 항목:
   - *"Must have a `system/persona.md`"*
   - *"Must NOT have overlapping file and folder names (e.g. `system/human.md` and `system/human/identity.md`)"*
   - *"Must follow specification for skills (e.g. `skills/{skill_name}/`) with the format: SKILL.md / scripts/ / references/ / assets/"*
4. **Poor use of progressive disclosure** — `[[path]]` 링크가 외부 메모리로 가는 discovery path 역할 *"Files that are outside of `system/` are not part of the system prompt, and must be dynamically loaded. You must index your files to ensure your future self can discover them"*.

**Step 2 — Implement context fixes** with 5-item checklist (verbatim):
- System prompt token budget reviewed (~15-20k tokens target)
- No overlapping or redundant files remain
- All file descriptions are unique, accurate, and match their contents
- Moved-out knowledge has `[[path]]` references from in-context memory
- No semantic changes to persona, user identity, or behavioral instructions

**Step 3 — Commit and push** (`fix(doctor): <summary> 🏥` 형식).

**Step 4 — Recommend `/recompile`** — *"recommend that they run `/recompile` to apply these changes to the current system prompt"*.

### Basic Memory `doctor` 와의 비교

| 차원 | Basic Memory `doctor` | Letta Code `/doctor` |
|---|---|---|
| 검사 대상 | knowledge.db FTS5 인덱스, schema drift, orphan files | system/ 토큰 예산, 파일 중복, 명명 충돌, frontmatter 누락, progressive disclosure 결함 |
| 발동 주체 | 사용자 CLI 명령 | 사용자 슬래시 명령 → LLM 이 skill 로 실행 |
| 자동 수정 | 일부 (인덱스 재생성) | LLM 이 plan + apply (사용자 검토 권유) |
| 영속화 | SQLite migration | git commit + `/recompile` |
| 운영 토대 | structural — 데이터 무결성 | structural + procedural — 시스템 프롬프트 품질 + 데이터 구조 |

**판정**: `/doctor` = **structural lint 2번째 확정 사례**. Basic Memory 와 어휘 1:1 일치 (`audit and refine`, `drift`, `degradation`), 자기진단 → 자기수정 루프 동일. 단 Letta 의 검사 범위가 **더 넓다** — 토큰 예산 같은 *contextual quality* 까지 포함하므로 Basic Memory 의 *데이터* lint 보다 한 단계 위 추상화.

→ `primitive-knowledge-layer-design-space.md` 의 **Lint 3분지 → "structural lint" 셀이 2 사례로 carve-out 트리거 충족**.

### 부수 — `memory_maintenance.md` 자가 메모리화

`/doctor` SKILL 외에도 `system/dev_workflow/memory_maintenance.md` 라는 메모리 파일 자체가 트리에 있음 (`/memory` 출력 verbatim). 즉 **메모리 정책 자체를 메모리화** — Letta agent 가 자기 lint 정책을 self-edit 가능. context_doctor SKILL 의 절차가 외부 코드, 메모리 정책은 내부 markdown — **이중 레이어 자기진단**.

---

## 3축 프레임 판정

### 축 1 — Builder

**판정: self-editing (primary, 강력) + curation 요소 (사용자 `/remember`, `/init`, frontmatter 명시)**.

근거:
- Letta 의 핵심 차별 — *"agents can read and update them using built-in memory tools"*. memory blocks 의 모든 편집이 LLM 도구 호출로 이뤄짐.
- MemFS 환경에서 LLM 이 직접 파일 생성/삭제/수정/이름변경 — Letta Code memory 페이지 verbatim *"Your Letta Code agent can self-edit its own memory, and will use the context of the conversation to decide when to edit its memory"*.
- 단 **`description` frontmatter 가 필수** + `read_only` 옵션 + `/init` 의 context constitution + `/doctor` 의 사용자 검토 — 이는 **인간 curation 게이트**.
- Reflection subagent 가 자율 commit 까지 가는 것은 self-editing 의 가장 강력한 형태 — Cognee improve 가 weight 만 갱신하는 것과 비교해 **파일 자체를 LLM 이 작성/재구성**.

→ Letta = **PKM 서베이 (`inbox/2026-04-21-memory-pkm-survey.md`) 의 "self-editing builder" 단일 사례 자리에 가장 강력한 사례**. Basic Memory(co-authored) 와 명확히 구분되며, Cognee(induction) 보다도 강력한 자기-편집.

### 축 2 — Storage primitive

**판정: 두 모드 — server 본연은 hybrid 4-tier (relational blocks + vector archival + read-only files + RAG), MemFS 는 markdown primary + git secondary (Basic Memory 에 가장 가까움)**.

근거:
- Server: docs `context-hierarchy` 4-tier 표 verbatim 명시 — 다양한 storage primitive 를 도구로 통합한 hybrid.
- MemFS: blog verbatim *"Files are simple, universal primitives that both humans and agents can work with using familiar tools"* — Unix 파일시스템 + git versioning.
- **Q1 핵심 발견**: *"git-tracked"* 표현이 마케팅이 아닌 실제 git 레포 (clone/commit/push 명령). Markdown + frontmatter 는 Basic Memory 의 markdown primary 와 동일 패턴.
- **server vs MemFS 의 storage 좌표가 다르므로 카드에 두 좌표 모두 등재 필요**.

→ **markdown primary + 보조 인덱스 (server side blocks 동기화) 의 2번째 확정 사례** (Basic Memory 1번째). PKM 서베이 *"Letta MemFS 의 git-tracked 선택은 markdown 쪽으로 움직이는 신호"* 가설 **확정**.

### 축 3 — Timing

**판정: runtime + 4-tier descending (immediate ↔ MemFS git push 중간 4단계)**.

근거:
- 모든 메모리 편집이 대화 중에 발생 — runtime.
- **4-tier 영속화 흐름**:
  1. Messages (auto-managed, compaction 으로 자동 요약)
  2. Conversation history (`conversation_search` 로 검색, 무한)
  3. Archival passages (LLM 이 명시 `archival_memory_insert` 호출)
  4. Memory blocks / MemFS (LLM 이 self-edit, MemFS 는 git commit 으로 영속)
- `/init` 같은 일회성 compile-time 도 있으나 중심은 runtime.
- Reflection subagent 는 비동기 background — runtime 의 **두 번째 액터**.

→ Letta = **Cognee 의 "session ↔ permanent 2단" 보다 더 세분화된 4-tier**. PKM 서베이 timing 축의 *"runtime, 증분"* 사례.

### 축 4 — 감사 가능성 — 판정 = **NO (미성립)**

| 항목 | Letta 존재 여부 | 근거 |
|---|---|---|
| 엣지 / 사실 / 블록 단위 confidence 필드 | **× 부재** | docs 전체 (`llms-full.txt` 40k 라인) 에서 confidence/reliability/trust score 메모리 메타 0건. evals 컨텍스트의 *"Indicate confidence level for each research finding"* 1건은 grader 컨텍스트로 무관 |
| Epistemic tagging (EXTRACTED/INFERRED/AMBIGUOUS) | **× 부재** | docs 검색 0건 |
| "Never invent" / "If unsure, mark Y" honesty rule | **× 부재** (메모리 한정) | Ralph mode 의 `<promise>` 만 honesty pattern, 메모리 편집에는 미적용 |
| Provenance (소스 lineage) | **△ 약함** | Reflection 의 git commit message 에 *"Reviewed transcript: <transcript_filepath>"* 가 약한 트레이서빌리티. 단 노드/사실 단위가 아니라 **commit-level diff 단위** |
| Read-only flag | **○ 존재** | block `read_only: true`, MemFS frontmatter `read_only` — 단 신뢰도 태깅 ≠ 편집 잠금 |
| Pre-commit validation | **○ 부분** | `pre-commit validation for memory and skill formatting` (changelog 0.19.7) — 형식 검증, 의미/신뢰도 검증 아님 |

**판정**: Letta 의 git commit history = **구조적 audit trail** (어느 시점에 어떤 변경이 어떤 reflection turn 으로 들어갔는지 추적). 이는 Cognee 의 provenance 보다 강력한 "변경 이력" — 단 Graphify 의 *"엣지 단위 epistemic confidence"* 와는 **다른 layer 의 문제**.

→ 축 4 (감사 가능성) 는 **여전히 Graphify 단일 사례**. promotion 조건 미충족. 단 Letta 의 git-as-audit-trail 은 **별도 sub-axis 후보** (audit 의 "변경 이력 vs 추출 신뢰도" 두 차원 분리 필요).

### 3축 종합 좌표

**Letta server**: `(self-editing, hybrid 4-tier blocks/files/archival/RAG, runtime + 4-tier descending)`.

**Letta Code (MemFS)**: `(self-editing, markdown primary + git secondary + server blocks tertiary, runtime + git commit 영속)`.

→ MemFS 좌표는 **Basic Memory 와 1-hop 이웃** (markdown primary 공유), 단 builder 축이 다름 (Letta = 강한 self-editing, Basic Memory = co-authored). Server 좌표는 GraphRAG 7종 / Cognee 와 **다른 cluster** — 그래프 구조 없음, blocks 가 Mem0 의 fact list 에 더 가까움.

---

## Q5 — 세션 ↔ 영속 bridging 패턴

### Letta 의 4-tier 영속화 흐름 (재정리)

```
[Live messages]              ← in context window, auto-evicted by compaction
       ↓ (compaction trigger: sliding_window/all)
[Summarized history]         ← still in context, but condensed
       ↓ (overflow → recall via conversation_search)
[Conversation history DB]    ← out of context, hybrid text+semantic search
       ↓ (LLM explicit archival_memory_insert)
[Archival memory passages]   ← vector DB, semantic retrieval, agent-immutable
       ↓ (LLM self-edit, or sleep-time/reflection bridging)
[Memory blocks / MemFS]      ← in context (always), git-versioned
```

### Cognee `(user_id, session_id)` cache → permanent 패턴과 비교

| 차원 | Cognee | Letta |
|---|---|---|
| Bridging 단위 | session cache → permanent graph | 4-tier descending pinning |
| 자동성 | `improve()` 호출 / `remember(self_improvement=True)` | compaction 자동 + reflection 자동 + archival_memory_insert 명시 |
| 트리거 | 명시적 또는 ingest-end | 컨텍스트 만석 (compaction) / step count (reflection) / agent decision (archival) |
| Source 표현 | `_source="session"|"graph"` 태그 | message metadata + git commit history |
| 일반화 | 2-tier (cache, permanent) | 4-tier (live, summary, archival, blocks/MemFS) |

**판정**: 두 시스템이 모두 *"단기 → 장기 메모리 승격"* 패턴을 구현하지만 **위상이 다르다** — Cognee 는 2-tier, Letta 는 4-tier. 따라서 Q5 *"세션→영속 bridging 의 2번째 사례"* 는 **부분 확정**:

- 공통점 (= 일반화 가능): *"임시 작업 메모리 → 명시 또는 자동 트리거 → 영구 저장소"* 의 추상 패턴.
- 차이점 (= 다양성): tier 수, trigger 종류, 영속 단위 (graph vs file vs block).

→ `primitive-knowledge-layer-design-space.md` 축 3 (timing) 에 **"hybrid bridging" sub-value** 가 정당화되며, Letta 는 그 안의 가장 정교한 4-tier 사례. Cognee 는 2-tier 사례. PKM 서베이의 Letta MemFS 가 *"세션→영속 bridging 패턴의 2번째 사례인지"* 질문 → **확정 (2번째), 단 다른 위상의 같은 추상 패턴**.

---

## Lint 3분지 위치 (재적용)

| 분지 | Letta 대응 | 세부 |
|---|---|---|
| **Structural lint** | **○ `/doctor` = `context_doctor` skill** | Basic Memory 와 어휘 1:1 일치, **2번째 확정 사례** |
| **Semantic lint** | **× 부재** | orphan/superseded/contradiction/missing concept 탐지 0건. context_doctor 의 *"Consolidate redundant files"* 는 redundancy 만 |
| **Incremental update** | **△ 약한 형태** | Reflection 이 변경분만 commit, 전체 재빌드 없음. 단 Graphify `--update` 같은 명시적 증분 명령 없음 |
| **Consolidation + feedback (4번째 분지, Cognee 1사례)** | **○ Reflection subagent** | feedback weighting 부재, 그러나 *"Identify mistakes / inefficiencies / user feedback / update memory"* 4단 루프가 동등 추상. 1 layer 위에서 2번째 사례 |

**Carve-out 정리**:

- **Structural lint** = Basic Memory + Letta `/doctor` → **2 사례 확정, carve-out 트리거 충족**.
- **Semantic lint** = LLM Wiki 단일 사례 (Cognee, Letta 둘 다 미성립).
- **Incremental update** = Graphify 단일 사례.
- **Consolidation + feedback (신규)** = Cognee `improve` (feedback weighting) + Letta `reflection` (user feedback 분석) → **2 사례 확정**, 단 두 사례의 메커니즘이 다름 (Cognee = streaming weight, Letta = LLM 분석 + git commit).

→ `knowledge-lifecycle-operations` 카드 carve-out **3 분지가 2-사례 임계** 도달 — 카드 작성 trigger.

---

## 지형 내 포지셔닝

### vs MemGPT 원 논문 (2310.08560, Packer et al. 2023)

- 원 논문 = **core / archival / recall 3-tier** + page 도구 + sleep time. Letta 의 server 본연은 그 직계 후손이며 *"recall memory"* 가 `conversation_search` 도구로 흡수됐을 뿐 본질 동일.
- Letta Code MemFS 는 **원 논문의 ManifestoMemory + ToolFileSystem 일부 구상** 의 markdown 구현 — 단 논문 직접 인용 아닌 추정. Blog `context-repositories` 가 이전 *"Virtual filesystem operations"* 를 reference 로 인정.

### vs Basic Memory

- **Storage 축 1-hop 이웃**: 둘 다 markdown + frontmatter + 외부 인덱스 (Basic Memory = SQLite FTS5/FastEmbed, Letta MemFS = server blocks sync + git).
- **Builder 축 다름**: Basic Memory = co-authored (MCP write_note), Letta = self-editing (자율 도구 호출).
- **Lint 분지 일치**: 둘 다 structural lint 보유 (`doctor` 어휘 동일).
- **Multi-tenancy**: Basic Memory v0.16 Postgres 옵션, Letta server 가 더 정교 (ADE, project, org).
- **Bridging**: Basic Memory `sync --watch` 는 파일 변경 감지 단일 trigger, Letta 4-tier 는 더 세분화.

### vs Cognee

- **Builder 축 매우 다름**: Cognee = induction (자동 KG 빌드), Letta = self-editing (LLM 자율 편집).
- **Storage 축 다름**: Cognee = vector + graph + relational hybrid + session cache, Letta = blocks + archival + files + MemFS markdown.
- **Lint 분지**: Cognee `improve` = consolidation + feedback (4번째 분지), Letta `reflection` = consolidation + (mistake-driven feedback) — **같은 4번째 분지의 다른 메커니즘**, 카드 carve-out 시 두 셀로 분기.
- **Bridging**: Cognee 2-tier (cache → graph), Letta 4-tier (live → summary → archival → blocks/MemFS).
- **Audit**: Cognee provenance (source lineage), Letta git commit history — 둘 다 Graphify confidence 와는 다른 layer.

### vs LLM Wiki (Karpathy)

- **Builder 축 인접**: Karpathy = "LLM 이 자기 위키를 직접 쓴다" 철학, Letta = LLM 자기 메모리 self-edit. 가장 가까운 근접.
- **Storage 축 일치**: 둘 다 markdown + 디렉터리 hierarchy (LLM Wiki `index.md`, Letta `system/`).
- **Timing 축 다름**: LLM Wiki = compile-time (rebuild on demand), Letta = runtime (대화 중).
- **Lint 분지 다름**: LLM Wiki = semantic lint (orphan/superseded), Letta = structural lint.
- **PKM 서베이 가설 확증**: *"MemFS 의 git-tracked 선택은 markdown 쪽으로 움직이는 신호"* — **LLM Wiki ↔ Letta MemFS 가 "self-editing markdown PKM" 같은 좌표로 수렴하고 있다**. 두 사례가 다른 timing 으로 같은 (builder, storage) 좌표에 도달.

### vs Graphify

- **3축 모두 다름**: Graphify (induction + KG 6 표면 + compile-time) vs Letta (self-editing + blocks/markdown + runtime).
- **공통점 0**: 데이터 모델, builder, timing 모두 직교.
- **유일 비교점**: 둘 다 자기-자신을 메모리화 (Graphify 의 self-extracted PKM, Letta `memory_maintenance.md`) — 그러나 추상 수준 다름.

### vs Mem0 / Zep

- **Mem0**: managed drop-in personalization (last-write-wins arbitration). Letta 의 self-editing 보다 자동, 그러나 LLM 자율성 약함. **builder 축 다름** (Mem0 = induction-managed, Letta = self-editing).
- **Zep**: temporal knowledge graph (fact invalidation by time). Letta 의 4-tier 와 다른 메커니즘 — Zep 은 **시간축 invalidation**, Letta 는 **공간축 pinning**.
- Letta forum *"Agent memory: Letta vs Mem0 vs Zep vs Cognee"* 토론 (Cognee 노트에서 인용) — 4자 직접 경쟁 카테고리.

---

## 스케일 감각

### 공식 문서 확인

- **Memory blocks 권장 한도** (verbatim): block 당 <50k chars, agent 당 <20 blocks.
- **Files 권장 한도**: 파일당 5MB, agent 당 <100 files, 동시 open 5.
- **Archival passages**: 무제한, passage 당 300 tokens.
- **Sleep-time frequency**: default 5 step, 권장 *"keeping the frequency relatively high (e.g. 5 or 10) as triggering the sleep-time agent too often can be expensive"*.
- **MemFS system prompt budget**: *"~10% of the total context size (usually ~15-20K tokens)"* — context_doctor 권장.
- **Compaction default**: `sliding_window_percentage=0.3`, summary 50,000 chars cap.

### Production 사례

- **Letta Cloud** = managed offering (`app.letta.com`). Pricing 페이지 존재 (docs `letta-code/pricing`, `guides/build-with-letta/pricing`). 세부 tier 한도는 (공식 범위 외 — 미답).
- **Built-in agents** (Memo, Incognito) — default agents 자동 생성 (changelog 0.13.0).
- **Letta API + ADE** + Python/TypeScript SDK + REST → enterprise 통합 stack.

### 공식 범위 외 (미답)

- **MemFS git 레포 크기 / 파일 수 한도**: docs 미명시.
- **Reflection subagent 의 LLM 비용 프로파일링**: *"can be expensive"* 만 정성, 정량 (공식 범위 외 — 미답).
- **alembic migration 자동 vs 명시 정책**: docs 검색 0건, src `db.py` 에서도 alembic invocation 직접 발견 못함 — 사용자가 alembic CLI 직접 실행하거나 server 시작 시 자동 실행 추정. 정확한 정책 (공식 범위 외 — 미답).
- **MemFS 도입 후 다양한 사용자의 평균 파일 수 / system/ 비율**: 공식 통계 (공식 범위 외 — 미답).
- **Server-side sleep-time vs Letta Code reflection 의 수렴 vs 분기 로드맵**: 둘 다 별도 진화 중인지, 어느 한쪽으로 통합 예정인지 (공식 범위 외 — 미답).
- **ACP (Letta agent-to-agent protocol)**: PKM 서베이에서 언급, 본 deep-dive 의 docs 검색에서 명시 페이지 미발견 — Letta forum 또는 별도 페이지 추적 필요. 본 deep-dive 의 핵심 아니므로 (공식 범위 외 — 미답) 처리.

---

## 메인 세션 codex 위임 후보

다음은 본 sub-agent 가 직접 처리하지 못한, **메인 세션에서 `/codex:rescue` 로 검증할 가치 있는** 미답 항목:

1. **alembic migration 정책 정밀 추적** — `letta/server/db.py` + `letta/__main__.py` 에서 alembic invocation 시점 (server boot vs 명시 명령) 코드-경로 추적. structural lint 의 자동성 정도 정밀화에 필요.
2. **MemFS git push 실패 시 fallback 동작** — 네트워크 단절, conflict, force-push 정책. `src/agent/memoryGit.ts` 분석 필요.
3. **Reflection subagent 의 정확한 git worktree 격리 메커니즘** — 병렬 reflection 충돌 시 merge 정책. Cognee 의 streaming feedback 과 비교에 필요.

위 항목은 본 노트의 핵심 결론에 영향 없으므로 **미답으로 남기고 noted**. 메인 세션이 필요시 검증 가능.

---

## 5개 검증 질문 결론 표

| 질문 | 결론 | 근거 요약 |
|---|---|---|
| **Q1: MemFS 정체 + markdown 수렴 신호?** | **확정** — markdown primary + git 진짜 레포 + frontmatter (description 필수). MemFS 는 server `memory(...)` 도구를 **대체** (Letta Code agent 한정, server 본연 blocks 는 그대로). **markdown 수렴의 2번째 확정 사례** (Basic Memory 1번째). | docs `letta-code/memory` verbatim, blog `context-repositories` verbatim, changelog 0.15.0/0.19.0/0.19.7 |
| **Q2: self-editing 도구 + sleep-time + consolidation+feedback 2번째 사례?** | **부분 확정** — 11+ 도구 enumerate (`memory(...)`, `core_memory_*`, `memory_*`, `archival_memory_*`, `conversation_search`, `open_files/grep_files/semantic_search_files`). 두 종류 sleep-time (`enable_sleeptime` server-side multi-agent + `reflection` Letta Code subagent). Cognee 와 다른 메커니즘 (feedback weighting 부재, LLM-driven mistake analysis 보유) — **consolidation+feedback 분지의 2번째 사례 부분 확정** (다른 위상의 같은 추상). | `letta/functions/function_sets/base.py`, `reflection.md`, sleeptime architectures docs |
| **Q3: 축 4 감사 가능성 2번째 사례?** | **반증** — confidence/reliability/honesty rule 부재. provenance 도 노드 단위로는 없음 (git commit 단위 audit trail 만 약하게 존재). Graphify 와 다른 layer. 축 4 = **여전히 Graphify 단일 사례**. | docs 40k 라인 검색 0건 (메모리 컨텍스트 한정), reflection.md 의 git commit metadata |
| **Q4: structural lint 2번째 사례?** | **확정** — `/doctor` = `context_doctor` skill. *"Identify and repair degradation in system prompt, external memory, and skills"* — Basic Memory `doctor` 와 어휘 1:1 일치. 4-step 절차 (identify → plan → commit → recompile) + 5-item 체크리스트. **structural lint 2 사례 확정 → carve-out 트리거**. | `src/skills/builtin/context_doctor/SKILL.md` verbatim, changelog 0.19.8 |
| **Q5: 세션→영속 bridging 2번째 사례?** | **부분 확정** — 추상 패턴 (*"임시 → 트리거 → 영속"*) 공유, 단 위상 다름. Cognee 2-tier (cache → graph), Letta 4-tier (live → summary → archival → blocks/MemFS). 둘 다 자동 + 명시 트리거 혼합. **bridging primitive 2 사례 확정, 단 다른 tier 수**. timing 축에 *"hybrid bridging"* sub-value 정당화. | docs `context-hierarchy` 표, `compaction.md`, archival/blocks 도구 시그니처 |

---

## 연결

- **`insights/primitive-knowledge-layer-design-space.md`** — 본 deep-dive 로 **두 좌표** 추가:
  - Letta server: `(self-editing, hybrid 4-tier blocks/files/archival/RAG, runtime + 4-tier descending)`
  - Letta Code MemFS: `(self-editing, markdown primary + git secondary, runtime + git commit 영속)`
  카드의 *"Letta MemFS 가 markdown 쪽으로 수렴 신호인지"* **확정** (markdown primary 2번째 사례). *"self-editing 피드백이 consolidation+feedback 의 2번째 사례인지"* **부분 확정** (다른 메커니즘). **Lint 분지 carve-out 트리거 도달** — structural (Basic Memory + Letta = 2 사례) + consolidation+feedback (Cognee + Letta = 2 사례) 둘 다 충족. Semantic lint (LLM Wiki) 와 incremental update (Graphify) 만 1 사례 잔존.
- **`notes/techniques/cognee.md`** — `improve` vs Letta `reflection` 비교 매트릭스 작성 가치. 둘 다 *"단기 → 장기 메모리 승격 + LLM 자기 분석"* 이지만 (1) Cognee = 단일 시스템 4-stage pipeline + feedback weight, (2) Letta = 별도 actor agent + git commit 영속 + mistake-driven 분석. **같은 분지의 다른 구현**.
- **`notes/techniques/basic-memory.md`** — `doctor` 명령 어휘 1:1 일치. Storage 축 1-hop 이웃 (markdown primary 공유). Builder 축 다름 (co-authored vs self-editing). 본 노트가 *"structural lint 2 사례 확정"* 트리거 — Basic Memory 노트의 lint 섹션에 *"Letta `/doctor` 가 2번째 사례, carve-out 가능"* 주석 추가 가치.
- **`notes/techniques/karpathy-llm-wiki.md`** — 가장 흥미로운 비교. **Builder + Storage 축 인접**: 둘 다 self-editing markdown PKM. 단 timing 다름 (compile vs runtime). **두 사례가 다른 timing 으로 같은 (builder, storage) 좌표에 도달** — primitive 카드의 (builder, storage) 2D 평면에 **수렴 cluster** 첫 사례.
- **`notes/techniques/graphify.md`** — 축 4 비교. Letta git commit history ≠ Graphify edge confidence (다른 layer). 축 4 promotion 대기 상태 유지. 단 Letta 의 *"git as audit trail"* 은 별도 sub-axis 후보 — *"audit = 변경 이력 vs 추출 신뢰도"* 두 차원 분리 검토 가치.
- **`inbox/2026-04-21-memory-pkm-survey.md`** — Letta 항목 2번 (deep-dive 우선순위 1)의 모든 미답 해소:
  - *"MemFS 의 git-tracked 가 마케팅인지 실제인지"* → **실제 git 레포** 확정.
  - *"core/archival/recall 과 공존 vs 대체"* → **Letta Code agent 한정 대체**, server 본연은 공존 (Memory Blocks / Files / Archival 4-tier).
  - *"self-editing 피드백 = consolidation+feedback 2번째 사례"* → **부분 확정** (다른 메커니즘).
  - *"릴레이셔널 → markdown 수렴 신호"* → **확정** (Letta Code 한정).
  서베이 파일에 *"Letta deep-dive 결과 4가지 핵심 가설 확정/반증, 카드 carve-out 트리거 도달"* 마커 추가 가치.
- **후보 신규 카드 `knowledge-lifecycle-operations`** — 본 deep-dive 가 **carve-out 트리거 충족** 결정타. 분지 별 사례 표:

  | 분지 | 사례 | 비고 |
  |---|---|---|
  | Structural lint | Basic Memory `doctor` + Letta `/doctor` | 2 사례 → carve-out OK |
  | Semantic lint | LLM Wiki `Lint Workflow` | 1 사례 |
  | Incremental update | Graphify `--update` | 1 사례 |
  | Consolidation + feedback | Cognee `improve` + Letta `reflection` | 2 사례 (다른 메커니즘) → carve-out OK |
- **Mem0 / Zep deep-dive (미작성)** — Letta 와 직접 경쟁 카테고리, 비교 매트릭스 완성을 위해 다음 deep-dive 후보. Mem0 의 last-write-wins arbitration, Zep 의 temporal invalidation 이 본 deep-dive 의 4-tier bridging 과 어떻게 다른지가 축 3 timing 의 sub-value 정밀화에 필요.

---

## Sources

- [letta-ai/letta GitHub repository](https://github.com/letta-ai/letta) — 2026-04-21 fetch, Apache-2.0, v0.16.7 (2026-03-31)
- [letta-ai/letta-code GitHub repository](https://github.com/letta-ai/letta-code) — 2026-04-21 fetch, Apache-2.0, v0.22.4 (2026-03)
- [docs.letta.com 메인](https://docs.letta.com/) — 2026-04-21 fetch, "The memory-first coding agent that remembers and learns"
- [docs.letta.com llms.txt 인덱스](https://docs.letta.com/llms.txt) — 2026-04-21 fetch
- [docs.letta.com llms-full.txt 전체 docs](https://docs.letta.com/llms-full.txt) — 2026-04-21 fetch (40,893 라인 ~2MB), 모든 verbatim 인용의 1차 소스
- [docs.letta.com — Letta Code memory page](https://docs.letta.com/letta-code/memory/index.md) — 2026-04-21 fetch, MemFS 정의 + git 동기화 + dreaming 설정
- [docs.letta.com — sleep-time agents architecture](https://docs.letta.com/guides/agents/architectures/sleeptime/index.md) — 2026-04-21 fetch (llms-full.txt L13-200)
- [docs.letta.com — slash commands](https://docs.letta.com/letta-code/slash-commands/index.md) — 2026-04-21 fetch (llms-full.txt L7113-7378), `/doctor`, `/sleeptime`, `/remember`, `/init` 등 38개 명령 카탈로그
- [docs.letta.com — subagents](https://docs.letta.com/letta-code/subagents/index.md) — 2026-04-21 fetch (llms-full.txt L7381-7533), 8개 built-in subagent 표
- [docs.letta.com — context hierarchy](https://docs.letta.com/guides/core-concepts/memory/context-hierarchy/index.md) — 2026-04-21 fetch (llms-full.txt L27839-27876), 4-tier 메모리 표
- [docs.letta.com — memory blocks](https://docs.letta.com/guides/core-concepts/memory/memory-blocks/index.md) — 2026-04-21 fetch (llms-full.txt L27878+)
- [docs.letta.com — archival memory](https://docs.letta.com/guides/core-concepts/memory/archival-memory/index.md) — 2026-04-21 fetch (llms-full.txt L27655-27834)
- [docs.letta.com — compaction](https://docs.letta.com/guides/core-concepts/messages/compaction/index.md) — 2026-04-21 fetch (llms-full.txt L28650-28793), 4 modes 정의
- [docs.letta.com — agent file (.af)](https://docs.letta.com/guides/core-concepts/agent-file/index.md) — 2026-04-21 fetch (llms-full.txt L27239-27438)
- [docs.letta.com — how it works](https://docs.letta.com/letta-code/how-it-works/index.md) — 2026-04-21 fetch (llms-full.txt L5473-5632), client-side tool execution + server arch
- [docs.letta.com — ralph mode](https://docs.letta.com/letta-code/ralph-mode/index.md) — 2026-04-21 fetch (llms-full.txt L6394-6533)
- [docs.letta.com — changelog](https://docs.letta.com/letta-code/changelog/index.md) — 2026-04-21 fetch (llms-full.txt L2036-3287), MemFS 0.15.0 도입, `/doctor` 0.19.8 도입 등
- [letta.com/blog/context-repositories](https://www.letta.com/blog/context-repositories) — 2026-04-21 fetch, MemFS 설계 동기 + SKILL.md frontmatter 비교
- [letta/functions/function_sets/base.py](https://github.com/letta-ai/letta/blob/main/letta/functions/function_sets/base.py) — 2026-04-21 fetch, 11+ memory 도구 verbatim docstring
- [letta/functions/function_sets/files.py](https://github.com/letta-ai/letta/blob/main/letta/functions/function_sets/files.py) — 2026-04-21 fetch, file 도구 시그니처
- [letta-code/src/skills/builtin/context_doctor/SKILL.md](https://github.com/letta-ai/letta-code/blob/main/src/skills/builtin/context_doctor/SKILL.md) — 2026-04-21 fetch, `/doctor` 의 정확한 정의 (Q4 결정적 1차 소스)
- [letta-code/src/agent/subagents/builtin/reflection.md](https://github.com/letta-ai/letta-code/blob/main/src/agent/subagents/builtin/reflection.md) — 2026-04-21 fetch, reflection subagent verbatim (Q2 결정적 1차 소스)
- [PyPI letta](https://pypi.org/project/letta/) — 2026-04-21 fetch, v0.16.7, deps (postgres, sqlite, redis, pinecone)
- [github.com/letta-ai/letta/tree/main/letta](https://github.com/letta-ai/letta/tree/main/letta) — 2026-04-21 fetch, server 패키지 디렉터리 구조
- [github.com/letta-ai/letta-code/tree/main/src](https://github.com/letta-ai/letta-code/tree/main/src) — 2026-04-21 fetch, CLI 패키지 디렉터리 구조
- [letta/alembic/versions](https://github.com/letta-ai/letta/tree/main/alembic/versions) — 2026-04-21 fetch, 167 migration files
- MemGPT 원 논문 (arxiv 2310.08560, Packer et al. 2023) — 본 deep-dive 미직접 fetch, 3-tier 정의 reference 용
- `inbox/2026-04-21-memory-pkm-survey.md` — 로컬 서베이, Letta 항목 2번 (참조)
- `insights/primitive-knowledge-layer-design-space.md` — 로컬 primitive 카드 (3축 프레임 적용 대상)
- `notes/techniques/cognee.md` — 4번째 deep-dive 직전 사례, 비교 매트릭스의 핵심 대조군
- `notes/techniques/basic-memory.md` — `doctor` 어휘 비교 1차 대조군
- `notes/techniques/karpathy-llm-wiki.md` — self-editing markdown PKM 수렴 비교
- `notes/techniques/graphify.md` — 축 4 비교
