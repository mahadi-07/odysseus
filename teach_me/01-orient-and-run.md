# Stage 1 — Orient & run it

← [Index](README.md) · Next: [Stage 2 — Boot sequence](02-boot-sequence.md)
· How lessons run: [TEACHING_GUIDE.md](TEACHING_GUIDE.md)

**Status:** `[x]` done

> **Teacher note:** run the [7-step loop](TEACHING_GUIDE.md). This stage is about the
> *user's* view + getting it running — light on code, heavy on orientation.

---

### 1. Why this matters
Before reading any code, you should know what Odysseus *does* and see it run. Building
the user's mental model first gives every later code stage something concrete to attach
to ("oh, *this* function is what powers the chat box I used").

### 2. Concepts you'll need
None yet — this stage is orientation. (Framework basics start in Stage 2 via
[`concepts.md`](concepts.md).)

### 3. Guided reading
- Open **`README.md`** → the **Features** list. Each bullet (Chat, Agent, Email,
  Documents, Memory, Calendar, Tasks, Cookbook, Deep Research, Compare) is a subsystem
  you'll meet later.
- Skim **`ROADMAP.md`** — where the project is heading, and what's half-built.
- Get it running: `./start-macos.sh` → opens `http://127.0.0.1:7860`. First run prints a
  temporary **admin password** in the terminal.
- Click around for 10 minutes: send a chat, open Settings, open the Documents tab.

> ⚠️ **"database is locked" on startup?** Something else holds a write lock on
> `data/app.db` (commonly an IDE's database tool, e.g. IntelliJ/PyCharm). SQLite allows
> one writer at a time and the startup migrations have no busy-timeout, so they fail
> instantly. Fix: disconnect the IDE from the DB (or quit it), kill any stuck `setup.py`,
> then re-run `./start-macos.sh`. Migrations are idempotent — re-running is safe.

### 4. Check questions
1. Name three things Odysseus can do that a plain chatbot can't.
2. Where does the *data* live (what file), and what kind of database is it?
3. Why does the app print a password on first run?

### 5. Discuss
Answer above; the teacher will fill gaps and connect each feature to the subsystem
you'll study later (e.g. "Agent" → Stage 6, "Email" → Stage 8).

### 6. Checkpoint (pass bar)
- The app is running at `http://127.0.0.1:7860` and you've **sent one chat message**.
- In your own words: *"Odysseus is a ___ that lets me ___, storing data in ___."*

### 7. Record & advance
Write your answers below; flip Status to `[x]`; update the pointer in `README.md`.

---

## Your answers / notes

- App runs at http://127.0.0.1:7860. Hit "database is locked" on startup → cause was
  IntelliJ's Database tool holding a write lock on `data/app.db`; fix = disconnect the
  IDE (or quit it), then `./start-macos.sh`.
- _(add your check-question answers here)_
