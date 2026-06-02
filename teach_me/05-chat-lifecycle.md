# Stage 5 — Chat lifecycle (the spine of the app)

← Prev: [Stage 4](04-auth.md) · [Index](README.md) · Next: [Stage 6 — The Agent loop](06-agent-loop.md)
· How lessons run: [TEACHING_GUIDE.md](TEACHING_GUIDE.md)

**Status:** `[ ]` not started

---

### 1. Why this matters
This is the **core path** of the whole product: you type a message, it reaches an LLM,
and the reply streams back to your screen word-by-word. Almost everything else is built
around this spine. Slow down here — it's worth real time.

### 2. Concepts you'll need
[`concepts.md`](concepts.md) **§1 FastAPI & routing**, **§3 async/await**, and
**§5 Server-Sent Events (SSE)** — SSE is *how* the reply streams back.

### 3. Guided reading (follow the message's journey, in order)
1. **`routes/chat_routes.py:220`** — `setup_chat_routes(...)` registers the chat endpoints.
2. **`routes/chat_routes.py:236`** — `POST /api/chat`: the simple, *non-streaming* version
   (returns one whole reply). Good warm-up.
3. **`routes/chat_routes.py:331`** — `POST /api/chat_stream`: **the real one the UI uses.**
   *Look for:* a `mode` of `chat` vs `agent`, and that it returns a `StreamingResponse`.
4. **`routes/chat_routes.py:822`** — plain chat mode calls `stream_llm_with_fallback(...)`.
   **`routes/chat_routes.py:936`** — agent mode calls `stream_agent_loop(...)` (Stage 6).
5. **`src/llm_core.py:877`** — `llm_call_async(...)`: the actual single (non-streaming)
   call to the model. **`src/llm_core.py:985`** — `stream_llm(...)`: the streaming version
   that `yield`s SSE chunks. *(This is the #1 most-connected function in the codebase.)*
   Helper files in the chain: `routes/chat_helpers.py`, `src/chat_handler.py`,
   `src/chat_processor.py`.

### 4. Check questions
1. The UI uses `/api/chat_stream`, not `/api/chat`. Why? What does the user gain?
2. Inside `chat_stream`, what decides whether your message goes to plain `stream_llm`
   vs. the `stream_agent_loop`?
3. How does a half-finished reply get from the server to your browser? (Name the
   mechanism from `concepts.md`.)

### 5. Discuss
Answer; the teacher walks the full arrow:
**browser POST → `chat_stream` (331) → mode split → `stream_llm` / `stream_agent_loop` →
`llm_core` calls the model → SSE chunks stream back → browser renders them.**
Try `graphify explain "llm_call_async()"`.

### 6. Checkpoint (pass bar)
Trace **one chat message** end-to-end, naming each hop: the endpoint, the mode decision,
the function that calls the model, and how the reply returns.

### 7. Record & advance
Write answers below; flip Status to `[x]`; update `README.md`.

---

## Your answers / notes

_(write here as you go)_
