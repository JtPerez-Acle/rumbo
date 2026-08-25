# Aprende IA — Consumer Learning Platform (MVP Architecture)

Decisions locked (2026-07-24): **consumer-first**, **video+quiz interactivity is a
MUST**, **the 4 channels stay live as the acquisition funnel**.

Working name: **Aprende IA**. Flagship MVP course: **"Marketing con IA en 30 días"**
— 30 lessons across 5 modules, one lesson/day, delivered as vertical video + action.

**Alpha tester (n=1, before any cohort):** the user's girlfriend, who genuinely needs
to learn AI-driven marketing right now. She is the design partner: real hunger, real
use case, same-household feedback loop. The first course is built FOR her — if she
finishes Module 1, comes back daily without prompting, and can point at something she
*did* with lesson exercises (a campaign brief, ad copy, a content calendar), the format
works. If she stalls, we iterate the lesson format with her before recruiting anyone.
Her course topic doubles as the flagship: "Marketing con IA" has a concrete outcome,
overlaps the Oficina IA channel audience (funnel alignment), and is one of the
highest-demand AI upskilling topics for the eventual paid launch.

Core thesis: the channels' short-video engine becomes a *learning loop* — syllabus
graph → lesson videos → quiz/exercise → progress → spaced review. Video is the
delivery format; the loop is the product. Marginal cost per student ≈ $0 (videos are
canonical per syllabus node; personalization lives in each learner's path).

---

## 1. What gets reused vs. built

| Existing piece | Becomes |
|---|---|
| `cloud/writer.py` (DeepSeek scripts) | Lesson compiler (`write_lesson`): teaching structure + quiz in one call |
| `generate_batch.py` + MoneyPrinterTurbo | Unchanged — renders lesson videos to the volume |
| Postgres `topics` pattern | `syllabus_nodes` (course DAG) |
| Scheduler (APScheduler) | Daily lesson unlock + spaced-repetition due dates |
| Dashboard + approve gate | Course QA: review each lesson video/quiz before publishing the course |
| Fact-check-via-web-search pattern | Verifier pass on lesson scripts (paid product = higher accuracy bar) |
| The 4 channels | Top of funnel: every short links to the course (bio + pinned comment + CTA variant) |

New builds: syllabus generator, quiz generator (same LLM call as script), learner
data model, learner-facing app (feed + player + quiz + streak), magic-link auth.

---

## 2. Data model (extends `cloud/db.py`)

```sql
courses(id, slug UNIQUE, title, description, status,      -- draft|live
        created_at)

syllabus_nodes(id, course_id, module_no, position, slug, title,
        objectives TEXT,           -- what the learner can DO after this lesson
        angle TEXT,                -- the lesson's unique take
        status TEXT,               -- draft|scripted|rendered|approved
        video_file TEXT,           -- output/courses/<course>/<slug>.mp4
        quiz JSONB,                -- {questions:[{q,options[4],answer,explain}], exercise:{instruction,example}}
        UNIQUE(course_id, slug))

learners(id, email UNIQUE, name, tz, created_at)           -- magic-link, no passwords

enrollments(id, learner_id, course_id, started_at, current_position)

progress(id, learner_id, node_id,
        watched_at, quiz_score, quiz_attempts,
        next_review_at, review_interval_days)              -- SM-2-lite
```

Spaced repetition (SM-2 simplified): pass quiz → intervals 1 → 3 → 7 → 16 → 35 days;
fail → reset to 1 day. Review sessions re-serve the same video + a fresh quiz variant.

---

## 3. Lesson format (the pedagogy contract)

Every lesson = **45–60s video + immediate action**, generated together from the node:

- **Video script (110–140 words):** hook (why this matters to YOU) → one concept,
  one concrete example → recap in one line → action CTA: *"haz esto ahora"* (not
  "sígueme"). Deliberately calmer pacing than the virality channels — learners chose
  to be here; clarity beats dopamine, but attention is still real so we stay short.
- **Quiz:** 3 multiple-choice questions with explanations (wrong answers teach too).
- **Exercise:** one hands-on task with a copy-paste starting point (e.g. a prompt to
  try in ChatGPT/Claude, or a mini-challenge for Claude Code lessons). This is the
  MUST-have interactivity: watching ≠ learning; the exercise is where learning happens.

Progression gate: next lesson unlocks after quiz attempt (not necessarily pass —
we gate on engagement, not punishment; failed concepts go into review rotation).

---

## 4. Learner app (new, minimal, mobile-first)

Same Railway service, new FastAPI routes + one static page (same pattern as the
dashboard — no framework, fast to build, PWA-installable):

- `POST /api/auth/magic` → email a login link (Resend free tier); session cookie.
- `GET /api/feed` → ordered: due reviews first, then today's new lesson, then a
  locked preview of tomorrow (curiosity hook).
- Vertical swipe player → quiz modal on video end → exercise card → done state
  with streak + module progress bar.
- Streaks + module completion are the only gamification at MVP. No badges, no XP —
  measure first.

Video serving: from the Railway volume at MVP scale (≤100 beta users). If bandwidth
becomes a problem, move course videos to Cloudflare R2 + CDN (cheap, one afternoon).

---

## 5. Course factory pipeline (admin side)

1. `syllabus.py`: course brief → one LLM call → 30-node DAG (modules, titles,
   objectives, prerequisites) → stored as `draft` nodes.
2. Human review of the syllabus in the dashboard (new Courses tab) — reorder/edit/cut.
3. Lesson compiler runs over approved nodes: script + quiz + exercise per node
   (news-style verifier pass on factual claims).
4. Batch render (existing pipeline) → videos land on the volume.
5. Human approve per lesson (existing gate pattern) → course flips to `live`.

One-time cost per course: ~$0.35 in LLM + ~90 min render. Reused for every student.

---

## 6. Launch plan & what decides success

- **Phase 1 — Course factory** (syllabus gen, lesson compiler, quiz gen, render all
  30 lessons of "Marketing con IA en 30 días", QA in dashboard).
- **Phase 2 — Learner app** (schema, magic-link, feed, quiz flow, streaks, spaced rep).
- **Phase 2.5 — Alpha (n=1):** the girlfriend takes the course for real. Watch
  everything: does she return daily unprompted? Where does she drop? Are exercises
  doable or skipped? Weekly format iterations based on her experience. Exit criteria:
  she completes Module 1 and produces at least one real marketing artifact from the
  exercises. Only then recruit the cohort.
- **Phase 3 — Free beta cohort:** 50–100 users recruited exclusively through the 4
  channels (bio links + course-CTA video variants). Free on purpose: we're buying
  retention data, not revenue.
- **Phase 4 — Price it:** Stripe Payment Link (zero code) once metrics clear the bar.
  LatAm-priced: ~$5–10/mo or one-time course price. Then: second course chosen from
  channel performance data (which topics' videos overperform → that's the demand signal).

**Success gates after 30 days of beta:**
- Module 1 completion ≥ 60% (edutainment products die here — this is THE metric)
- D7 retention ≥ 40%, D30 ≥ 20%
- Median quiz score ≥ 70% on first attempt (lessons actually teach)
- Exercise attempt rate ≥ 50% (interactivity is being used, not skipped)

If Module-1 completion fails the bar, the fix is lesson format iteration — not more
features. If it passes, corporate ("capacitación IA para equipos") is the fast-follow
with real pricing power.

---

## 7. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Edutainment trap (watching ≠ learning) | Exercise-mandatory format; success gates on completion + quiz, not views |
| Factual errors in paid content | Verifier pass (web-search fact-check) + human approve per lesson |
| Email deliverability (magic links) | Resend/Postmark with proper domain setup from day one |
| Railway bandwidth for video | Fine ≤100 users; R2+CDN migration path documented |
| Scope creep before validation | Nothing beyond §4 ships in MVP: no comments, no social, no cert, no multi-course |

The channels keep their own README (`studio/README.md`) and launch plan — nothing
in this document changes them. Same repo, same engine, two products.
