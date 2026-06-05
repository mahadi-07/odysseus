# teach_me/ — Learning Odysseus, step by step

This folder is a **teacher-led course** for the **Odysseus** codebase, where Claude
acts as your teacher. It runs a Socratic, guided-reading style: Claude explains, points
you to the exact code, you read it, Claude quizzes you, you explain it back. A progress
tracker gives full traceability across sessions.

> 🧭 **Fresh session / new LLM run?** Read **[`intent.md`](intent.md)** first (my goal +
> how I want to learn), then **[`TEACHING_GUIDE.md`](TEACHING_GUIDE.md)** (how to teach
> this course), then come back here for the live progress.

- **`README.md` (this file) is the main index** — overview, mental model, jargon, and
  the progress tracker. **Start here every time.**
- **[`TEACHING_GUIDE.md`](TEACHING_GUIDE.md)** — the 7-step teaching loop Claude follows.
- **[`concepts.md`](concepts.md)** — plain-language primer for the framework basics
  (FastAPI, middleware, async/await, SQLAlchemy ORM, SSE). Stages link to it.
- **Each stage has its own file** (`01-orient-and-run.md` … `10-…md`) structured as a
  lesson: *why it matters → concepts → guided reading (exact `file:line`) → check
  questions → discuss → checkpoint → record*.

How a stage runs: Claude explains → you read the cited code → Claude asks check questions
→ you discuss → **you explain it back** (the pass bar) → mark it done → next stage.

> **What Odysseus is:** a self-hosted AI workspace — "the self-hosted version of
> the ChatGPT/Claude UI experience," running on your own hardware with your own
> data. Local-first, privacy-first. Backend: **FastAPI** (Python). Frontend:
> **vanilla JavaScript** (no framework). Storage: **SQLite** via **SQLAlchemy**.
> Talks to any LLM (local: vLLM / llama.cpp / Ollama; API: OpenAI / OpenRouter).
>
> Scale (from the knowledge graph in `graphify-out/`): **8,525 code entities,
> 17,221 relationships, 344 subsystems.** It's big — that's why we go in order.

---

## Learner profile

- **Level:** newer to Python / FastAPI / async / SQLAlchemy → terms get defined,
  framework concepts explained, slower pace.
- **Goal:** understand the whole thing end-to-end (breadth across all 10 stages).
- **Format:** self-driven. These docs are the plan; bring questions back to the
  mentor for deep dives on anything fuzzy.

---

## The mental model (read this first, every time)

```
  Browser  (static/js/*.js — vanilla JS)
      │  HTTP request  /  Server-Sent Events stream
      ▼
  app.py  ── the orchestrator: builds FastAPI, adds middleware,
      │       wires in ~40 route modules
      ▼
  routes/*.py  ── one file per feature (chat, email, tasks, …)
      │            each calls into…
      ▼
  src/*.py  ── the logic: agent_loop, llm_core, tool_implementations
      │
      ▼
  core/*.py  ── the foundation: database.py (models + migrations),
      │          auth.py, session_manager.py
      ▼
  SQLite (data/app.db)  +  LLM endpoints  +  IMAP/SMTP, CalDAV, MCP servers…
```

**Layers:** `core/` is the floor · `src/` is the logic · `routes/` is the HTTP
surface · `static/` is the UI · `app.py` bolts it all together.

### Jargon cheat-sheet (you'll see these constantly)

| Term | Plain meaning |
|------|---------------|
| **FastAPI** | Python library that turns functions into web endpoints (URLs). |
| **Route / endpoint** | One URL the server answers, e.g. `POST /api/chat`. Lives in `routes/`. |
| **Middleware** | Code that runs on *every* request before/after the route (e.g. auth check). |
| **ORM (SQLAlchemy)** | Treat DB rows as Python objects (a `Session` class ↔ the `sessions` table). |
| **async / await** | Python's way to handle many requests at once without freezing. |
| **SSE** (Server-Sent Events) | One-way server→browser stream; how the reply appears token-by-token. |
| **MCP** | Model Context Protocol — a standard for plugging in external tool servers. |
| **God node** | A heavily-connected function — a core abstraction worth knowing. |

---

## Progress tracker

Legend: `[ ]` not started · `[~]` in progress · `[x]` done

| # | Stage | Status | File | Notes |
|---|-------|:------:|------|-------|
| 1 | Orient & run it | `[x]` | [01-orient-and-run.md](01-orient-and-run.md) | App runs at http://127.0.0.1:7860. Hit "database is locked" → IntelliJ held a lock on `data/app.db`; fix = disconnect IDE then `./start-macos.sh`. |
| 2 | Boot sequence (`app.py`) | `[x]` | [02-boot-sequence.md](02-boot-sequence.md) | ✅ App obj @77, middleware stack (reverse-order insight), ~39 routers as table-of-contents, startup event. |
| 3 | Data layer (`core/database.py`) | `[x]` | [03-data-layer.md](03-data-layer.md) | ✅ `Session→ChatMessage` (FK :166, two-way rel 127↔177, dual cascade + SQLite `PRAGMA foreign_keys=ON` :47). 35 idempotent `_migrate_*` (no-Flyway, by-hand). Entity-vs-POJO "two Sessions" gotcha → read the **import path**. Taught via JPA→SQLAlchemy map (learner knows Spring/Hibernate). |
| 4 | Auth (`core/auth.py`) | `[ ]` | [04-auth.md](04-auth.md) | |
| 5 | Chat lifecycle | `[ ]` | [05-chat-lifecycle.md](05-chat-lifecycle.md) | |
| 6 | The Agent loop (`src/agent_loop.py`) | `[ ]` | [06-agent-loop.md](06-agent-loop.md) | |
| 7 | Tools & MCP | `[ ]` | [07-tools-and-mcp.md](07-tools-and-mcp.md) | |
| 8 | One subsystem (your pick) | `[ ]` | [08-subsystem.md](08-subsystem.md) | Choose: Email / Documents / Memory / Tasks / Deep Research / Cookbook |
| 9 | Frontend (`static/`) | `[ ]` | [09-frontend.md](09-frontend.md) | |
| 10 | Tests & contributing | `[ ]` | [10-tests-and-contributing.md](10-tests-and-contributing.md) | |

**Currently on:** Stage 4 (auth) → next up **Stage 5 (chat lifecycle)**.

---

## Using the knowledge graph as a study aid

A full knowledge graph of this codebase lives in `graphify-out/`. Handy commands:

```bash
graphify explain "llm_call_async()"      # everything connected to a function
graphify path "AuthManager" "Session"    # shortest path between two concepts
graphify query "how does chat streaming work"   # broad traversal answer
```

`graphify-out/graph.html` is an interactive map; `graphify-out/GRAPH_REPORT.md`
lists the god nodes, surprising connections, and suggested questions.

---

## How to ask the mentor for help

- "Walk me through `app.py` lines 85–145 — what's the middleware doing?"
- "I read `core/database.py` but don't get `relationship()` — explain it."
- "Trace a chat message through the code for me." (live Stage 5)
- "I'm stuck on the agent loop." (live Stage 6)
- "Give me the reading plan for the Email subsystem." (Stage 8)

**Suggested next move:** Stage 2 (`app.py`) — it's the map that makes every other
stage navigable, and it's mostly wiring, so it's beginner-friendly.

---

*Last updated: 2026-06-02. Keep the progress table current as you go.*
