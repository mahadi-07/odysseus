# Stage 9 — Frontend: `static/`

← Prev: [Stage 8](08-subsystem.md) · [Index](README.md) · Next: [Stage 10 — Tests & contributing](10-tests-and-contributing.md)
· How lessons run: [TEACHING_GUIDE.md](TEACHING_GUIDE.md)

**Status:** `[ ]` not started

---

### 1. Why this matters
This closes the loop: you've followed a request from the browser all the way to the LLM
and back. Now see the **browser side** — and the good news for a beginner is there's **no
framework** (no React/Vue). It's plain JavaScript that calls the same `/api/...` routes
you already met.

### 2. Concepts you'll need
[`concepts.md`](concepts.md) **§5 SSE** (how the frontend reads a streaming reply) and
**§1 FastAPI & routing** (the `/api/...` URLs it calls).

### 3. Guided reading
- **`static/index.html`** — the single HTML page. It loads the theme, then mounts
  `app.js`.
- **`static/app.js`** — the orchestrator: imports and initializes all the feature
  modules in `static/js/`.
- **`static/js/chat.js`** — trace the chat we studied in Stage 5 from the *other* side:
  - **`static/js/chat.js:921`** — `fetch('/api/chat_stream', { method: 'POST' })`. *This
    is the browser calling the endpoint from Stage 5.*
  - **`static/js/chat.js:972`** — `res.body.getReader()`: reads the **streamed** reply
    chunk-by-chunk (the SSE stream).
  - **`static/js/chatStream.js`** — the richer SSE event handling (tool events,
    heartbeats, stall watchdog).

### 4. Check questions
1. The UI is plain JS — no framework. How does a button click end up running backend code?
   (Name the function the browser calls and the URL.)
2. In Stage 5 the server `yield`ed SSE chunks. Which lines here *consume* that stream?
3. Connect `chat.js:921` to a specific line you read in Stage 5.

### 5. Discuss
Answer; the teacher closes the full circle: **`chat.js:921` (fetch) → `chat_routes.py:331`
(`/api/chat_stream`) → agent/LLM → SSE back → `chat.js:972` (read) → DOM update.**

### 6. Checkpoint (pass bar)
Connect **one UI action to the route that handles it** — naming the frontend `fetch` and
the backend endpoint — and say how the streamed reply gets rendered.

### 7. Record & advance
Write answers below; flip Status to `[x]`; update `README.md`.

---

## Your answers / notes

_(write here as you go)_
