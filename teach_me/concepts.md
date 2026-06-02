# concepts.md — the framework basics, in plain language

A primer for the things you're newer to. Each stage links to the section it needs.
Read a section when a stage points you here; you don't have to read it all up front.

Every concept below is paired with **one real spot in Odysseus** so it's not abstract.

---

## 1. FastAPI & routing

**What it is:** FastAPI is a Python library for building web servers. You write a
normal Python function, put a **decorator** on top of it, and FastAPI turns it into
a **route** — a URL the browser can call.

- A **decorator** is the `@something` line above a function. It "wraps" the function
  with extra behavior. `@router.post("/api/chat")` means *"when a POST request hits
  `/api/chat`, run this function."*
- A **route / endpoint** = one URL + method (GET/POST) the server answers.
- A **router** groups related routes; the main app "includes" each router.

**Request → response:** browser sends an HTTP request → FastAPI matches the URL to a
route function → your function returns data → FastAPI sends it back as the response.

**Real example:** `routes/chat_routes.py:236` —
```python
@router.post("/api/chat")
async def chat_endpoint(request: Request, chat_request: ChatRequest): ...
```
That decorator is why typing in the chat box and hitting send reaches this function.
The routers get "plugged into" the app in `app.py:512–699` (~39 of them).

→ *Used in: Stage 2 (Boot), Stage 5 (Chat lifecycle).*

---

## 2. Middleware

**What it is:** middleware is code that runs on **every** request, before and/or after
your route function. Think of it as a stack of wrappers around every endpoint. Common
jobs: check the user is logged in, add security headers, enforce a timeout.

**Order matters.** Each middleware wraps the next. In Odysseus (`app.py`):
```
CORSMiddleware (85)  →  SecurityHeadersMiddleware (104)
   →  _RequestTimeoutMiddleware (145)  →  AuthMiddleware (356, if AUTH_ENABLED)
        →  your route function
```
So a request passes *through* all of these before it ever reaches, say, the chat route.

**Real example:** `AuthMiddleware` (`app.py:356`) checks who you are on every request —
that's why individual routes don't each have to re-check your login.

→ *Used in: Stage 2 (Boot), Stage 4 (Auth).*

---

## 3. async / await

**What it is:** a way for Python to handle many things at once without freezing. When
code is "waiting" (for the LLM to reply, for the database, for the network), `async`
lets the server go do other work instead of blocking.

- `async def foo(): ...` declares a function that can pause and resume.
- `await something` means *"pause here until `something` finishes, but let other work
  run meanwhile."* You can only `await` inside an `async def`.
- An **async generator** is an `async def` that `yield`s values over time (instead of
  returning once). This is how Odysseus streams an LLM reply token-by-token.

**Why it matters here:** an AI reply takes seconds and arrives in pieces. Async lets one
server stream replies to many users at the same time.

**Real example:** `src/agent_loop.py:1394` —
```python
async def stream_agent_loop(...):   # async generator
    ...
    yield f"data: {chunk}\n\n"      # emits each piece as it's ready
```

→ *Used in: Stage 5 (Chat), Stage 6 (Agent loop), Stage 7 (Tools).*

---

## 4. SQLAlchemy ORM

**What it is:** an **ORM** (Object-Relational Mapper) lets you work with database rows
as Python objects instead of writing raw SQL. You define a Python **class**; SQLAlchemy
maps it to a database **table**.

- `class Session(Base)` ↔ the `sessions` table. One object = one row.
- Each `Column(...)` = one field (column) in the table.
- `ForeignKey("sessions.id")` = a link from one table to another (a message belongs to
  a session).
- `relationship(...)` = the Python-side convenience to walk that link, e.g.
  `session.messages` gives you all messages without writing a JOIN.
- A **DB session** (confusingly named — different from a *chat* Session) is your handle
  for a unit of database work: query, add, commit. Odysseus opens one via
  `get_db_session()` and closes it when done.

**Real example:** `core/database.py:76` (`class Session`) and `:155` (`class ChatMessage`,
which has `session_id = Column(ForeignKey("sessions.id"))`). The `relationship` between
them lets code do `session.messages`.

> ⚠️ Odysseus has **two** "Session"/"ChatMessage" definitions: the ORM ones in
> `core/database.py` (what's stored) and lightweight `@dataclass` ones in
> `core/models.py:24,44` (what's passed around in memory). Don't confuse them.

→ *Used in: Stage 3 (Data layer), and everywhere data is read/written.*

---

## 5. Server-Sent Events (SSE)

**What it is:** a simple one-way stream from **server → browser** over a single HTTP
connection. The server keeps the connection open and sends lines of text as events; the
browser reads them as they arrive. Perfect for "show the AI's answer as it's typed."

- The server sends lines like: `data: {"delta": "Hello"}\n\n`
- A special final line — `data: [DONE]` — signals the stream is finished.
- It's one-way (server→browser). The browser's *request* that started it was a normal POST.

**Real example, both ends:**
- Server emits SSE chunks: `src/llm_core.py:985` (`stream_llm`) and the agent loop's
  `yield "data: …"`.
- Browser consumes them: `static/js/chat.js:921` does the `fetch('/api/chat_stream')`,
  then `:972` reads the streamed body with `res.body.getReader()`; richer event handling
  lives in `static/js/chatStream.js`.

→ *Used in: Stage 5 (Chat), Stage 9 (Frontend).*

---

## Quick glossary

| Term | One-liner |
|------|-----------|
| **Route / endpoint** | A URL+method the server answers (in `routes/`). |
| **Decorator** | The `@…` line that wraps a function (e.g. `@router.post(...)`). |
| **Middleware** | Code that runs on every request, around the route. |
| **Dependency** | A value FastAPI injects into a route (e.g. the DB session, the user). |
| **ORM** | Maps Python classes ↔ DB tables (SQLAlchemy). |
| **`relationship()`** | Python-side link to walk a ForeignKey (e.g. `session.messages`). |
| **async generator** | `async def` that `yield`s over time — used for streaming. |
| **SSE** | One-way server→browser text stream; ends with `data: [DONE]`. |
| **MCP** | Model Context Protocol — standard for plugging in external tool servers. |
| **God node** | A heavily-connected function; a core abstraction worth knowing. |

---

*Back to [the index](README.md). Concepts are referenced from individual stage files.*
