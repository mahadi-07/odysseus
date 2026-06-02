# Stage 6 — The Agent loop: `src/agent_loop.py`

← Prev: [Stage 5](05-chat-lifecycle.md) · [Index](README.md) · Next: [Stage 7 — Tools & MCP](07-tools-and-mcp.md)
· How lessons run: [TEACHING_GUIDE.md](TEACHING_GUIDE.md)

**Status:** `[ ]` not started

---

### 1. Why this matters
This is what turns a *chatbot* into an *agent*. In agent mode the model doesn't just
reply — it can **call tools** (run code, edit docs, manage tasks), see the results, and
keep going until the job is done. This loop is the most impressive machinery in Odysseus.

### 2. Concepts you'll need
[`concepts.md`](concepts.md) **§3 async/await** (the loop is an async generator) and
**§5 SSE** (it streams events to the UI as it works). It builds directly on Stage 5.

### 3. Guided reading
Open **`src/agent_loop.py`** (it's large — focus on the shape, not every line):
- **`src/agent_loop.py:1394`** — `async def stream_agent_loop(...)`. The entry point
  (called from `chat_routes.py:936`). It's an **async generator** — it `yield`s SSE events.
- **Prep (≈1430–1507):** detect intent, pick which tools are relevant for this query (RAG
  tool selection), decide API-vs-local tool style.
- **The round loop (≈1462–2092):** *this is the heart.* For each round (up to a cap):
  1. stream a turn from the LLM **with the tool schemas**,
  2. find any tool the model wants to run — two styles: **native function-calling**
     (hosted APIs emit structured `tool_calls`) or **fenced code blocks** (` ```bash `,
     ` ```python `, ` ```create_document ` for local models),
  3. **run** the tool (handoff to `execute_tool_block` — Stage 7),
  4. feed the result back into the conversation,
  5. repeat until the model produces a final answer (or a loop-breaker trips).
- **Finish (≈2094–2125):** emit metrics, then `data: [DONE]`.

### 4. Check questions
1. In plain words, what is the *loop* doing each round? Why does it need more than one
   round?
2. Name the two ways the model can ask to run a tool. Why support both?
3. What stops the loop from running forever?

### 5. Discuss
Answer; the teacher contrasts **chat mode** (one LLM turn, no tools) with **agent mode**
(loop + tools) and connects step 3 to Stage 7. Try `graphify explain "execute_tool_block()"`.

### 6. Checkpoint (pass bar)
Explain the agent loop in **3 sentences**: how it decides to use a tool, what it does with
the result, and how it knows when to stop.

### 7. Record & advance
Write answers below; flip Status to `[x]`; update `README.md`.

---

## Your answers / notes

_(write here as you go)_
