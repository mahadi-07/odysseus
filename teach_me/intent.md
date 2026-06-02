# intent.md — read this first

> **Purpose of this file:** give a fresh Claude Code run the full context of what
> I'm doing here, with zero prior memory. If you are an LLM reading this at the
> start of a new session: **reading this one file should be enough** to understand
> my goal, how I want to learn, and how to help me. Read it, then read
> `teach_me/TEACHING_GUIDE.md` (how to teach this course) and `teach_me/README.md`
> (live progress), then continue teaching me.
>
> **How this course is run:** Claude acts as my **teacher**, Socratic style — explain
> a concept, point me to the exact code, let me read it, quiz me, then I explain it
> back (that's the pass bar). The full method is in `teach_me/TEACHING_GUIDE.md`.
> Framework basics I'm new to (FastAPI, async, ORM, SSE) are primed in
> `teach_me/concepts.md`. Don't just lecture — point me to code and ask.

---

## Who I am / my level

- I am **newer to the core stack**: Python, FastAPI, async/await, and SQLAlchemy
  (ORM) are all relatively new to me.
- So: **define terms as they come up, explain framework concepts, go at a slower
  pace.** Don't assume I know web-framework or ORM jargon. Explain *why*, not just
  *what*.

## What I'm trying to do

I want to **understand the Odysseus project end-to-end** — the whole architecture,
not just one feature. Odysseus is an open-source, self-hosted AI workspace
(FastAPI backend + vanilla-JS frontend + SQLite/SQLAlchemy; it's like a
self-hosted ChatGPT/Claude UI). I'm learning it as a mentee learning from a mentor.

My goal is **comprehension, breadth-first**: a solid mental model of how every
major piece fits together, built up in a deliberate sequence so it's not
overwhelming.

## How I want to learn (the method)

- **Step by step, in a fixed sequence.** We follow a 10-stage curriculum (see
  `teach_me/README.md`). One stage at a time, bottom of the stack upward, but
  starting from the boot sequence so the pieces connect.
- **I drive; you guide.** For each stage, give me a clear reading plan: *what file
  to open, what to look for, questions to ask myself, and a checkpoint to know I
  understood it.* I read it myself, then come back with questions. When something
  is fuzzy, I'll ask and you go deep on that specific thing.
- **Grounded in the real code.** This repo has a prebuilt knowledge graph in
  `graphify-out/` (8,525 code entities, 344 subsystems). Use it — e.g.
  `graphify explain "llm_call_async()"`, `graphify path "A" "B"`,
  `graphify query "..."` — so explanations match *this* codebase, not generic
  advice.
- **Keep it traceable.** Always update progress so the next session knows exactly
  where I left off (see "How to use the teach_me folder" below).

## What the `teach_me/` folder is

This folder **is** my learning workspace and the source of truth for my progress.

- **`README.md`** — the main index. Overview of Odysseus, the layered mental-model
  diagram, a jargon cheat-sheet, and the **progress tracker table** (each stage
  marked `[ ]` not started / `[~]` in progress / `[x]` done, with a notes column
  and a link to each stage file). **This is where you check where I am.**
- **`01-...` … `10-...md`** — one dedicated file per stage. Each has the reading
  plan for that stage, prev/next navigation, a `Status:` line, and a
  "Your notes / questions" section I fill in as I go.
- **`intent.md`** — this file. The persistent "why/how" so a fresh run has context.

### The 10 stages (the sequence)

1. **Orient & run it** — `README.md`, `ROADMAP.md`, get the app running.
2. **Boot sequence** — `app.py` (FastAPI orchestrator, middleware, route wiring).
3. **Data layer** — `core/database.py` (models + migrations), `core/session_manager.py`.
4. **Auth** — `core/auth.py` (`AuthManager`, `get_current_user`).
5. **Chat lifecycle** — `routes/chat_routes.py` → `src/ai_interaction.py` →
   `src/llm_core.py` (`llm_call_async()`). The core "send message → stream reply" path.
6. **The Agent loop** — `src/agent_loop.py` (`stream_agent_loop`, `execute_tool_block`).
7. **Tools & MCP** — `src/tool_implementations.py`, `src/mcp_manager.py`.
8. **One subsystem (my pick)** — Email / Documents / Memory / Tasks / Deep Research / Cookbook.
9. **Frontend** — `static/js/*.js`, how the UI calls the routes.
10. **Tests & contributing** — `tests/`, `CONTRIBUTING.md`.

## How to use the teach_me folder (instructions for the LLM)

When I start a fresh session and point you here:

1. **Read this `intent.md`** (you're doing it) to get my goal + learning style.
2. **Open `teach_me/README.md`** and read the progress table + the "Currently on:"
   line to find which stage I'm on.
3. **Open that stage's file** (e.g. `02-boot-sequence.md`) for its reading plan and
   any notes I've written.
4. **Continue teaching from there** in my preferred style (self-driven: give me the
   plan, answer my questions in depth, define terms).
5. **Keep progress current.** When a stage is done, update *both* the table in
   `README.md` and the `Status:` line in that stage's file, and move the
   "Currently on:" pointer. Add anything we figured out to that stage's
   "Your notes / questions" section.

## Where I am right now (snapshot)

- **Stage 1 (Orient & run it):** in progress. The app runs at
  `http://127.0.0.1:7860`. I hit a "database is locked" error on startup — cause
  was IntelliJ's database tool holding a write lock on `data/app.db`; fix is to
  disconnect the IDE (or quit it), then re-run `./start-macos.sh`.
- **Next up: Stage 2 — `app.py`** (the boot sequence / route wiring). It's mostly
  wiring, so it's a beginner-friendly map of the whole backend.

> For anything more detailed than this snapshot, the live state is always in
> `teach_me/README.md` and the individual stage files.
