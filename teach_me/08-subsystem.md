# Stage 8 — One subsystem (your pick)

← Prev: [Stage 7](07-tools-and-mcp.md) · [Index](README.md) · Next: [Stage 9 — Frontend](09-frontend.md)
· How lessons run: [TEACHING_GUIDE.md](TEACHING_GUIDE.md)

**Status:** `[ ]` not started

---

### 1. Why this matters
You now know the spine (chat) and the agent. A great way to cement it is to follow **one
feature top-to-bottom** — its route, its logic/service, its DB model, and its frontend.
This "vertical slice" shows how all the layers you've learned snap together for a real
feature.

### 2. Concepts you'll need
Everything so far. Pick whichever subsystem excites you most.

### 3. Guided reading — pick ONE, then read its slice
Each row gives the route → helper/service → DB model so you can trace the whole feature:

| Subsystem | Route(s) | Logic / service | DB model | Frontend |
|---|---|---|---|---|
| **Email** | `routes/email_routes.py`, `routes/email_pollers.py` | `routes/email_helpers.py` | `EmailAccount` (`core/database.py:286`) | `static/js/emailLibrary.js`, `emailInbox.js` |
| **Documents** | `routes/document_routes.py` | `src/document_processor.py`, `src/pdf_form_doc.py` | `Document` (`core/database.py:184`) | `static/js/document.js` |
| **Memory / Skills** | `routes/memory_routes.py`, `routes/skills_routes.py` | `services/memory/*` (ChromaDB / fastembed), `src/embeddings.py` | `Memory` (`core/database.py:611`) | `static/js/memory.js`, `skills.js` |
| **Tasks / Scheduling** | `routes/task_routes.py` | `src/task_scheduler.py` (`TaskScheduler`) | `ScheduledTask` (`core/database.py:508`) | `static/js/tasks.js` |
| **Deep Research** | `routes/research_routes.py` | `src/research_handler.py`, `src/search/*` | (uses sessions/docs) | `static/js/slashCommands.js`, `static/js/research/*` |
| **Cookbook** | `routes/cookbook_routes.py` | `routes/cookbook_helpers.py` | (`data/cookbook_state.json`) | `static/js/cookbook*.js` |

**How to read a slice:** start at the route file → find the endpoint for an action you
care about → follow what it calls into the service file → see which DB model it
reads/writes → (optionally) open the frontend file to see how the UI calls that route.

### 4. Check questions (adapt to your pick)
1. For your subsystem, what's the main endpoint a user action hits, and what does it call?
2. Which DB table does it read/write, and what's the `owner` column doing there?
3. Where does the frontend call this route from?

### 5. Discuss
Tell the teacher which subsystem you chose. **The teacher can spin out a dedicated,
deeper `08-<name>.md` file** for it (full reading plan + check questions + checkpoint).
`graphify query "how does <subsystem> work"` is a good kick-start.

### 6. Checkpoint (pass bar)
Walk the **full vertical slice** of your chosen subsystem out loud: frontend click →
route → service → DB model → response back to the UI.

### 7. Record & advance
Write your pick + answers below; flip Status to `[x]`; update `README.md`.

---

## My pick + notes

_(write which subsystem you chose and your notes here)_
