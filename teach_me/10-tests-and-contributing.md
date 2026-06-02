# Stage 10 — Tests & contributing

← Prev: [Stage 9](09-frontend.md) · [Index](README.md)
· How lessons run: [TEACHING_GUIDE.md](TEACHING_GUIDE.md)

**Status:** `[ ]` not started

---

### 1. Why this matters
You understand the app — now learn how to **change it safely** and submit those changes.
This is the difference between *reading* an open-source project and *contributing* to it.

### 2. Concepts you'll need
None new — this is about workflow and tooling.

### 3. Guided reading
- **`tests/`** — ~138 test files, using **pytest** (the standard Python test runner).
  Open one that matches something you learned, e.g. `tests/test_security_regressions.py`
  (pure-function tests, no DB) or `tests/test_calendar_recurrence.py`.
- **`tests/conftest.py`** — shared setup. *Look for:* it **stubs optional dependencies**
  so tests can run even if some libraries aren't installed. This is why tests can import
  helpers directly without spinning up the whole app.
- **`CONTRIBUTING.md`** — the rules of the road. The key commands (around lines 39–41):
  - `python -m pytest` — run the whole test suite.
  - `python -m py_compile app.py routes/*.py src/*.py` — quick syntax check of Python.
  - `node --check static/js/<file-you-changed>.js` — syntax check of changed JS.
  - PR expectations: small, focused changes, with test results included.

### 4. Check questions
1. How do you run the full test suite? How do you syntax-check a JS file you edited?
2. Why does `conftest.py` stub optional dependencies — what does that buy the tests?
3. You fixed a bug in `routes/email_routes.py`. What checks should you run before opening
   a PR?

### 5. Discuss
Answer; the teacher relates this to the actual workflow: branch → change → run pytest +
compile checks → open a focused PR. (If you ever want to *make* a change, this is where
we'd start.)

### 6. Checkpoint (pass bar)
**Run `python -m pytest`** (or a subset) successfully, and summarize the contribution
workflow from `CONTRIBUTING.md` in your own words.

### 7. Record & advance
Write answers below; flip Status to `[x]`. 🎉 That completes the course — you've gone
browser → routes → agent → tools → core → DB → frontend → tests.

---

## Your answers / notes

_(write here as you go)_
