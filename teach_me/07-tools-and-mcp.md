# Stage 7 — Tools & MCP

← Prev: [Stage 6](06-agent-loop.md) · [Index](README.md) · Next: [Stage 8 — One subsystem](08-subsystem.md)
· How lessons run: [TEACHING_GUIDE.md](TEACHING_GUIDE.md)

**Status:** `[ ]` not started

---

### 1. Why this matters
Stage 6 showed the loop *deciding* to use a tool. This stage is **what the tools
actually are** — the agent's hands. It's also where "MCP" comes in: a standard way to
plug in *external* tool servers so the agent can gain new abilities without code changes.

### 2. Concepts you'll need
[`concepts.md`](concepts.md) **§3 async/await** and the **MCP** glossary entry. Builds on
Stage 6's loop.

### 3. Guided reading
- **`src/tool_execution.py:542`** — `async def execute_tool_block(...)`. **The
  dispatcher.** It takes "the model wants to run tool X with content Y" and routes it to
  the right handler, returning `(description, result)`. *(Note: this is in
  `tool_execution.py`, not `tool_implementations.py`.)*
- **`src/tool_implementations.py`** — the actual capabilities, one `async def do_*` each:
  - `do_create_document` (`:196`) — create a living doc.
  - `do_manage_tasks` (`:837`) — list/add/complete todos.
  - `do_manage_notes` (`:1782`) — manage notes.
  - `do_manage_calendar` (`:1998`) — calendar events.
  - (bash/python/read_file/write_file are handled in `tool_execution.py` itself.)
- **`src/agent_tools.py`** — a thin **facade** that re-exports tool parsing, schemas, and
  execution so the rest of the code imports from one place. The MCP getter
  `get_mcp_manager()` lives here (`:75`).
- **`src/mcp_manager.py:34`** — `class McpManager`; `connect_server(...)` (`:47`) connects
  an external tool server (stdio subprocess or SSE). Its tools become available to the
  agent loop alongside the built-in `do_*` ones.

### 4. Check questions
1. The model emits a ` ```bash ` block. Which function receives it, and how does it know
   what to do with it?
2. What's the difference between a built-in tool (`do_*`) and an MCP tool?
3. Why is `agent_tools.py` described as a "facade"? What problem does that solve?

### 5. Discuss
Answer; the teacher draws the handoff: **loop (Stage 6) → `execute_tool_block` (542) →
the right `do_*` (or an MCP server) → result back to the loop.** Try
`graphify explain "execute_tool_block()"`.

### 6. Checkpoint (pass bar)
List **5 things the agent can do**, pointing at the function for each, and explain in one
sentence where MCP fits.

### 7. Record & advance
Write answers below; flip Status to `[x]`; update `README.md`.

---

## Your answers / notes

_(write here as you go)_
