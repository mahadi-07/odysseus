# Stage 3 — Data layer: `core/database.py` (+ `core/models.py`)

← Prev: [Stage 2](02-boot-sequence.md) · [Index](README.md) · Next: [Stage 4 — Auth](04-auth.md)
· How lessons run: [TEACHING_GUIDE.md](TEACHING_GUIDE.md)

**Status:** `[x]` done — passed checkpoint 2026-06-05 (explained `Session→ChatMessage`, a 2nd & 3rd link, and the idempotent-migration rationale).

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
- **`core/database.py:155`** — `class ChatMessage`. *Look for* the FK at **:166**
  `session_id = Column(String, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True)`
  and the `relationship` at **:177** (`session = relationship("Session", back_populates="messages")`)
  pairing back to the Session side at **:127**.
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

**Passed 2026-06-05.** Learner has Spring Boot + JPA/Hibernate + Postgres background, so
the ORM model came fast — taught via a JPA→SQLAlchemy translation table. Learning-as-it-comes
for this stage (no upfront concepts read).

**Checkpoint answers (in their words, corrected/confirmed):**
1. **`Session → ChatMessage`** = `@OneToMany`. **Parent = `Session`** (`sessions` table, the
   conversation/thread); **child = `ChatMessage`** (`chat_messages` table, one message =
   one user-or-assistant turn). The link is wired in **three** spots:
   - **:127** `messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")` — the One side.
   - **:166** `session_id = Column(String, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True)` — the FK.
   - **:177** `session = relationship("Session", back_populates="messages")` — the Many side.
   Delete a Session → its messages are deleted via **two** layers: ORM cascade (127,
   = JPA `orphanRemoval`+`CascadeType.ALL`) **and** DB `ondelete=CASCADE` (166), the latter
   only firing because **`PRAGMA foreign_keys=ON`** is set per-connection at **:47** (SQLite
   doesn't enforce FKs by default — unlike Postgres).
2. **2nd link:** `Session → Document` (FK `sessions.id`, `ondelete="SET NULL"` @ :189).
   **3rd link (bonus):** `Document → DocumentVersion` (Document = parent).
3. **`_migrate_*` (35 of them, called in `init_db()` :1510–1545):** they bring an *existing*
   DB up to the current schema. `Base.metadata.create_all()` (:1511) is **create-if-not-exists
   only — it never alters existing tables**, so column additions need the `_migrate_*`
   `ALTER TABLE` steps. Each is **idempotent**: it inspects the live schema first
   (e.g. :930 `PRAGMA table_info(sessions)`, :932 `if "total_input_tokens" not in columns`)
   and only acts if needed → safe to run on **every startup**, so there's no Flyway-style
   version table.

**Key takeaways learner derived:**
- **Two-Session gotcha** framed as **Entity vs POJO/DTO**: `core/database.py:76 Session`
  = `@Entity` (`(TimestampMixin, Base)`, persists); `core/models.py:44 Session` = POJO
  (bare `@dataclass`, no base, "no database logic" per docstring). Plus a **third** "Session":
  the SQLAlchemy DB session (`SessionLocal`/`sessionmaker` :36 ≈ JPA `EntityManager`).
  **Habit to disambiguate: read the `import` path, not the class name.**
- **Indexes map the hot queries:** FK cols are NOT auto-indexed in SQLite *or* Postgres
  (only PKs are; MySQL/InnoDB is the exception) → `session_id` (:166) and `owner` (:90)
  are explicitly `index=True`; `name` (:87) is not.
- **No-Flyway design rationale (learner's own):** hand-rolled migrations trade rigor/rollback
  for zero-ceremony self-hosted upgrades — correct bet for a single-file SQLite app; cost =
  forward-only, order-sensitive, fail-soft (`except: log warning`) migrations.
- **Ties to Stage-1 bug:** "database is locked" was `init_db()` running `ALTER TABLE` writes
  while IntelliJ held a SQLite write-lock (SQLite = single writer; Postgres MVCC wouldn't).

**Anchor drift fixed in this file (verified vs code 2026-06-05):** FK signature at :166 is
not bare (`ondelete="CASCADE", nullable=False, index=True`); token-migration example is at
**:932** (lesson said ~922); dataclass `Session` is `class` on :44 / decorator on :43.
