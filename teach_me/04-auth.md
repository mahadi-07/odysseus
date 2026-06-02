# Stage 4 — Auth: `core/auth.py` + `AuthMiddleware`

← Prev: [Stage 3](03-data-layer.md) · [Index](README.md) · Next: [Stage 5 — Chat lifecycle](05-chat-lifecycle.md)
· How lessons run: [TEACHING_GUIDE.md](TEACHING_GUIDE.md)

**Status:** `[ ]` not started

---

### 1. Why this matters
Almost every route needs to know *who* is asking (so it shows your sessions, your email,
your documents — not someone else's). Auth is touched everywhere: `get_current_user` and
`AuthManager` are among the most-connected functions in the whole codebase. Understanding
it explains the `owner` column you saw on every table in Stage 3.

### 2. Concepts you'll need
[`concepts.md`](concepts.md) **§2 Middleware** (auth runs as middleware on every request)
and the "dependency" entry in the glossary.

### 3. Guided reading
- **`core/auth.py:68`** — `class AuthManager`. The brain of auth: it owns users (in
  `data/auth.json`) and login sessions (`data/sessions.json`).
- **`core/auth.py:413`** — `create_session(username, password)`: verify credentials →
  return a token (a long random string) with a 7-day lifetime.
- **`core/auth.py:427`** — `validate_token(token)`: is this token still valid (not
  expired, user still exists)?
- **`core/auth.py:134`** — `_migrate_single_user()`: upgrades an old *single-user*
  `auth.json` to the *multi-user* format. (Another "upgrade" path, like Stage 3's.)
- **`src/auth_helpers.py:8`** — `get_current_user(request)`: pulls the username out of the
  request. *This is what routes call to know who you are.*
- **`app.py:356`** — `AuthMiddleware` is added here. *Look for:* it checks your cookie or
  bearer token on **every** request, so individual routes don't have to.

### 4. Check questions
1. When you log in, what does the server hand back to the browser, and where is it
   checked on your *next* request?
2. A route function needs to show "your" sessions only. How does it learn who "you" are?
   (Name the function.)
3. In Stage 3 every table had an `owner` column. Connect that to what you learned here.

### 5. Discuss
Answer; the teacher links the chain: **login → token → cookie → `AuthMiddleware` →
`get_current_user` → `owner` filter on DB queries.** Try `graphify explain "AuthManager"`
or `graphify path "AuthManager" "Session"`.

### 6. Checkpoint (pass bar)
In **one sentence**, explain how an incoming HTTP request gets associated with a specific
user — naming the middleware and the helper function involved.

### 7. Record & advance
Write answers below; flip Status to `[x]`; update `README.md`.

---

## Your answers / notes

_(write here as you go)_
