# Stage 2 — Boot sequence: `app.py`

← Prev: [Stage 1](01-orient-and-run.md) · [Index](README.md) · Next: [Stage 3 — Data layer](03-data-layer.md)
· How lessons run: [TEACHING_GUIDE.md](TEACHING_GUIDE.md)

**Status:** `[ ]` not started

---

### 1. Why this matters
`app.py` is the **map of the whole backend**. It builds the web server, sets up the
request pipeline (middleware), and "plugs in" ~39 feature modules. Once you can read
this file, you can find *any* feature's code by following its `setup_*_routes` line.

### 2. Concepts you'll need
Read these in [`concepts.md`](concepts.md): **§1 FastAPI & routing** and **§2 Middleware**.
(Optional preview: §3 async/await — you'll see `async def` here.)

### 3. Guided reading
Open **`app.py`** and look at these spots (don't read all 1000+ lines — just these):
- **`app.py:77`** — `app = FastAPI(...)`. *The web-server object is born here.*
- **`app.py:85–145`** — the middleware stack, in order: `CORSMiddleware` (85) →
  `SecurityHeadersMiddleware` (104) → `_RequestTimeoutMiddleware` (145). *Look for:* what
  each one does to every request.
- **`app.py:356`** — `AuthMiddleware` (added only if `AUTH_ENABLED`). *This is the
  "who are you?" check — you'll study it in Stage 4.*
- **`app.py:512–699`** — the long run of `app.include_router(...)` calls (~39 of them:
  auth, chat, email, tasks, calendar, memory, documents, gallery, cookbook, …). *This is
  the table of contents for the entire backend.*
- **`app.py:797`** — `@app.on_event("startup")`. *Code that runs once when the server
  boots* (MCP connect, scheduler start, warmups). `:1022` is the matching shutdown.

### 4. Check questions
1. If a request comes in while `AUTH_ENABLED` is true, name two pieces of middleware it
   passes through *before* reaching the chat route.
2. You want to find the code for the Email feature. Which line in `app.py` points you to
   its route file, and how did you know?
3. What's the difference between a middleware and a route?

### 5. Discuss
Answer; the teacher will connect this to the mental model (middleware = the wrappers,
routers = the feature doors) and use `graphify explain "app.py"` if a connection helps.

### 6. Checkpoint (pass bar)
Name **5 route modules** and what each does, reading only the `include_router` lines —
and explain, in one sentence, what runs before a request reaches its route.

### 7. Record & advance
Write answers below; flip Status to `[x]`; update `README.md`.

---

## Your answers / notes

_(write here as you go)_
