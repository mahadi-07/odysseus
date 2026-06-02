# Stage 3 — Data layer: `core/database.py` (+ `core/models.py`)

← Prev: [Stage 2](02-boot-sequence.md) · [Index](README.md) · Next: [Stage 4 — Auth](04-auth.md)
· How lessons run: [TEACHING_GUIDE.md](TEACHING_GUIDE.md)

**Status:** `[ ]` not started

---

### 1. Why this matters
The data model **is** the domain. Every feature ultimately reads/writes these tables, so
knowing the shape of a `Session`, a `ChatMessage`, a `Document` unlocks everything else.
This is also where the "upgrade" path lives — the migrations that keep an old database
working with new code.

### 2. Concepts you'll need
Read [`concepts.md`](concepts.md) **§4 SQLAlchemy ORM** (class ↔ table, `Column`,
`ForeignKey`, `relationship()`, DB session). It also explains the two-`Session` gotcha
below.

### 3. Guided reading
Open **`core/database.py`** — read the **class** definitions, *skim* the `_migrate_*`
functions:
- **`core/database.py:76`** — `class Session` (a chat conversation: name, model, owner,
  archived, folder, token counts…).
- **`core/database.py:155`** — `class ChatMessage`. *Look for* `session_id =
  Column(ForeignKey("sessions.id"))` and the `relationship` linking it back to `Session`.
- **`core/database.py:184`** — `class Document` (a living doc). Plus `EmailAccount` (286),
  `ScheduledTask` (508), `Memory` (611) — skim to feel the breadth.
- **`core/database.py:1505`** — `init_db()`. It calls `Base.metadata.create_all(...)`
  (creates tables) then **35** `_migrate_*` functions in order. *You don't need each one
  — understand WHY they exist:* they patch older databases to the new schema on startup
  (the "upgrade" path). They're idempotent (safe to re-run).
- Then open **`core/models.py:24` and `:44`** — lightweight `@dataclass` `ChatMessage`
  and `Session`. ⚠️ **Two different "Session"s exist:** the ORM one in `database.py` (what
  gets stored) vs. the dataclass here (what's passed around in memory). Notice they're not
  the same class.

### 4. Check questions
1. A `ChatMessage` "belongs to" a `Session`. Which line of code creates that link, and
   what's the SQLAlchemy name for it?
2. Why does `init_db()` run 35 migration functions instead of just creating the tables
   once? (Hint: think about a user who already has data from an old version.)
3. There are two classes named `Session`. What's the difference, and why might that be
   confusing in a bug report?

### 5. Discuss
Answer; the teacher will draw the `Session → ChatMessage` link and tie migrations back
to the "database is locked" error you hit in Stage 1 (that error happened *here*, during
`init_db`). Try `graphify explain "init_db()"` to see the migration fan-out.

### 6. Checkpoint (pass bar)
Sketch (on paper or in words) the **`Session → ChatMessage`** relationship and **one
other** table link, and explain in a sentence what the `_migrate_*` functions are for.

### 7. Record & advance
Write answers below; flip Status to `[x]`; update `README.md`.

---

## Your answers / notes

_(write here as you go)_
