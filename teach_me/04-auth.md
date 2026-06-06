# Stage 4 — Auth: `core/auth.py` + `AuthMiddleware`

← Prev: [Stage 3](03-data-layer.md) · [Index](README.md) · Next: [Stage 5 — Chat lifecycle](05-chat-lifecycle.md)
· How lessons run: [TEACHING_GUIDE.md](TEACHING_GUIDE.md)

**Status:** `[x]` done — passed checkpoint 2026-06-06 (explained the 3-way division of labor, tokens/passwords, and the `owner_filter` tie-back to Stage 3). Clean stage: all anchors verified vs live code, zero drift.

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
- **`app.py:249`** — `class AuthMiddleware(BaseHTTPMiddleware)` and its `dispatch()`.
  *The linchpin* is **`app.py:359`** (`request.state.current_user = auth_manager.get_username_for_token(token)`);
  cookie read at `:350`, failure split at `:352–355` (401 JSON for `/api/*`, 302 redirect to `/login` otherwise).
  It's **registered** at **`app.py:356`** (`app.add_middleware(AuthMiddleware)`). Checks your cookie or
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

**Passed 2026-06-06.** Taught via a Spring-Security → Odysseus translation table (learner knows
Spring Security/JPA). Brisk pace; learner gave correct security reasoning throughout (CSPRNG,
bcrypt salting, deleted-user revocation, in-memory-token scaling limits).

**The core mental model — 3-way division of labor** (the thing to remember):

| Job | Function | File:line | Spring analogue |
|---|---|---|---|
| **AUTHENTICATE** (once/request) | `AuthMiddleware.dispatch` | `app.py:249`, sets state @ `:359` | Security filter chain (`OncePerRequestFilter`) |
| **READ** identity | `get_current_user` | `auth_helpers.py:8` (⚠️ NOT core/auth.py) | `SecurityContextHolder.getAuthentication()` |
| **ENFORCE** (route + data) | `require_user` / `require_privilege` / `owner_filter` | `auth_helpers.py:44 / 91 / 117` | `@PreAuthorize` / Hibernate `@Filter` |

**The single connective wire: `request.state.current_user`** — middleware writes it (the ONLY place
a token→identity happens), everything downstream reads it. (It's written to `request.state`, not
returned, because the middleware calls `await call_next(request)` and can't return to the handler —
`request.state` = the per-request `SecurityContextHolder`; FastAPI is async so no thread-local.)

**End-to-end flow (`GET /api/sessions`):** `Cookie token` → `AuthMiddleware.dispatch` validates,
sets `request.state.current_user="shakil"` → `require_user` (401 if missing) → `get_current_user`
reads it → `owner_filter(query, Session, "shakil")` appends `WHERE owner='shakil' OR owner IS NULL`
→ only that user's (+ shared) rows return.

**Tokens & passwords (engine = `core/auth.py`):**
- Passwords: **bcrypt** (`_hash_password` :60 = `bcrypt.hashpw(pw, bcrypt.gensalt())`; verify :64 =
  `bcrypt.checkpw`). Random **per-password salt** → same password → different hash (defeats rainbow
  tables, hides reuse); bcrypt is deliberately slow (work factor). = Spring `BCryptPasswordEncoder`.
- Login token: `create_session` :413 → `secrets.token_hex(32)` (**CSPRNG**, 256-bit, unguessable;
  NOT `random`/`uuid4`). Stored **in-memory dict** `self._sessions {token:{username,expiry}}` +
  persisted to `sessions.json` under a lock. **TTL = 7 days** (:41).
- `validate_token` :427 rejects for **two** reasons beyond "missing": (1) **expired**
  (`time.time() > expiry`); (2) **orphaned user** (`username not in self.users` → admin
  deleted/renamed account → kicked out next request = immediate revocation). Both enforced in
  `validate_token` AND `get_username_for_token`.

**Gotchas / subtleties learner internalized:**
- **`get_current_user` lives in `src/auth_helpers.py:8`, NOT `core/auth.py`.** Mnemonic:
  `core/auth.py` = the vault (engine); `auth_helpers.py` = the turnstiles (FastAPI glue).
- `get_current_user` returning `None` is a **fact, not a safe default** — unscoped queries would
  leak everyone's data. Safety comes from **`require_user`** turning that into a 401 (belt-and-
  suspenders vs. middleware bypass / SSRF). `require_user` has 3 deliberate "" pass-through cases:
  `AUTH_ENABLED=false`, first-run loopback, `LOCALHOST_BYPASS=true`.
- **Two failure modes** (`app.py:352–355`): `/api/*` → `401 JSON` (client is JS/`fetch`, needs a
  status code); everything else → `302 → /login` (client is a human browser, needs a page).
- **Two auth paths** in `dispatch`: Bearer API-token path (`current_user="api"` + `api_token_owner`,
  unwrapped later by `effective_user` :13) handled first, then the cookie path.
- **`owner_filter` ties to Stage 3:** uses the `owner` column → DB-layer row scoping =
  multi-tenancy; `owner IS NULL` = shared/global rows. Same single-box design bet as Stage 3
  (in-memory tokens don't horizontally scale, like SQLite's single writer).
