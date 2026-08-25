# 06 — Status, roadmap and parked designs

*Current as of 2026-08-12.*

## Where we actually are

Read this before planning anything, because it is the fact that should drive
every decision:

| | |
|---|---|
| Courses live | **14** (420 lessons, 420 videos) — 7 added 2026-08-12: grafos-cultura, cultura-latam, gestión deportiva, vóleibol, influencer marketing, social media, analítica |
| Lessons completed **by humans** | **3** |
| Submissions | 13 |
| Conversations answered genuinely | 0 (two answered adversarially by an operator account) |
| Project documents | 1 (a seeded demo) |
| Concierge requests / waitlist | 0 / 0 (both surfaces went live 2026-08-07) |
| Active learners | the design partner (2 lessons), the operator (1) |

**We build roughly seventy times faster than we learn.** Nearly every system —
comprehension layer, dimensional scoring, the conversation, unlimited retries,
portfolio documents, navigation, the redesign, categories — was shipped on a
*single* round of feedback about an earlier version of the product. The
machinery is good and cost pennies; the bottleneck is not shipping capacity, it
is evidence.

**The alpha exit criterion is unchanged and unmet:** one design partner
completes Module 1 (6 lessons) and produces an artifact she actually uses.

**2026-08-12 changes nothing about that.** The catalog doubled (7 → 14 courses)
and the goal engine completed — posting *or* role → prereq-aware module route →
route-aware access → a goal document compiled from real work, with non-destructive
goal switching. A 15-use invite code (`Cohorte agosto 2026`) exists and has not
been shared. So the machinery is now genuinely ready and the gap between what is
built and what is known is **wider than ever**, not narrower. The next real
progress is a stranger finishing lesson 1.

## Success gates (fixed before the data, so the data can't negotiate)

After ~30 days of a free beta (50–100 users, recruited via the social channels):

| Metric | Bar | Why |
|---|---|---|
| Module-1 completion | ≥ 60% | Edutainment products die here; THE metric |
| D7 retention | ≥ 40% | Habit exists or it doesn't |
| D30 retention | ≥ 20% | |
| Median first-attempt quiz score | ≥ 70% | Lessons actually teach |
| Exercise **submission** rate | ≥ 50% | Now genuinely measurable (evidence, not self-report) |

Only after the gates clear: pricing (LatAm-anchored, ~$5–10/mo or per-course via
a Stripe link), then the corporate fast-follow where pricing power lives.

## Shipped 2026-08-06/07 (so you don't rebuild it)

Course concierge · comprehension layer (explain-back, evidence-based exercises,
capstone retos) · portfolio: project documents + STAR case studies with public
paper share pages · 4 new courses (Google Ads, SEO+AEO, Email, Automatización) ·
per-lesson explain prompts and module descriptions · catalog standardisation and
categories · public landing + browsable temarios + waitlist · Hoy tab (with the
spaced-repetition surface, which had been invisible) · Portafolio tab · hash
routing · orientation · **El Taller Nocturno** design system · unlimited retries
with best-attempt-wins · dimensional scoring + the conversation (ownership
probe) · verdict-based comprehension checks · operator reading view with
evaluation flagging · offsite DB backups · learner access links.

## Next, in the order I'd do it

*(Updated 2026-08-12. Shipped since the original list: learner profile — the
transversal project now lives on the learner and feeds the evaluator; the
matcher has a real fixture suite; docs 08–09 shipped the whole goal engine.)*

1. **Read the submissions and watch a learner do a lesson.** Not a build. The
   reading view exists (dashboard → Alumnos → *Leer su trabajo*); the habit
   doesn't. Everything below is guesswork until this happens.
2. **Human review of the unreviewed courses** — now 10 of 14 no human has read
   (courses 4–7 plus tonight's seven, minus sampled module 1s). Priority:
   module 1 of each, because at current traffic nobody reaches lesson 7.
3. **`RESEND_API_KEY`** — one key + DNS. Unlocks returning-user login (today an
   invite code gates *every* login), "your module opened" re-engagement, and the
   concierge "your course is ready" notification.
4. ~~**Tutor-evaluator fixture set in the repo**~~ **Shipped 2026-08-12** —
   `check_tutor.py`, 6 cases, real LLM calls, exits non-zero. It asserts what the
   product actually promises: identical work scores the same (spread 1 on the
   first run, band 10), better work scores higher (95 / 50 / 10), and restoring
   what the rubric rewards pays (**45 → 94** through the retry path). Real
   learner work is pulled from `submissions` at runtime rather than committed.
   Run it before any change to the evaluator prompts.
5. **Social channels** — fully built, dormant since July, blocked only on
   Upload-Post credentials. This is the acquisition engine, and the public
   landing + shareable rutas now exist with nothing pointing traffic at them.

## Security hardening (shipped 2026-08-12)

A full audit exploited four issues in production before fixing them: `/complete`
had no access check (any lesson/video unlockable, `quiz_score` uncapped), `/login`
handed a working session for any known email, the evaluators obeyed instructions
pasted into a submission (100/100 on garbage), and the public paper pages rendered
learner Markdown unsanitised. All four are fixed, verified dead in production, and
written up as recurring shapes in docs/07; the controls are tabulated in docs/03.

Two consequences worth knowing:

- **Returning-user login now requires the operator** until `RESEND_API_KEY` is
  set — self-service re-login returns 409 by design. That moves the email key
  from "nice to have" (item 3 above) to the thing standing between you and a
  cohort that can log itself back in.
- **`_client_ip` is only safe behind Railway's proxy**, which overwrites
  `X-Forwarded-For`. Moving hosts means revisiting every rate limit.

## UX audit (shipped 2026-08-12)

A full walkthrough on a phone, plus the first real reading of the design
partner's submissions, found that **the funnel does not leak at the catalog — it
leaks inside lesson 1**, and that three signature mechanisms had effectively
never run:

| Found | Evidence | Fixed by |
|---|---|---|
| Identical work scored **79 → 50 → 30** | byte-identical text, five days apart | identical resubmissions are no longer re-graded; `best_score` now ships with every evaluation and the card says what she keeps |
| Work lost on reload; no timeout anywhere | 25–35s evaluations (not the documented 10–20s), 5000-char textarea never saved | `postWithTimeout` + per-work-item `localStorage` drafts |
| The route was sold, then never mentioned | new learners landed on "elige tu primer curso"; the one real learner did lesson 1 of two unrelated courses | Hoy leads with "Dinos qué quieres ser"; browsing is the second door |
| Project skipped by **4 of 4** learners | form at 1763px of a 1947px page, all fields optional | project step moved above the explainer; nudges state that it is worth 40 of 100 points |
| Flagship missing its written guide on **all 30** lessons | only course affected; orientation promises it | new `course_factory <slug> backfill-written` |
| Landing showed seeded data as "documento real de una alumna" | that account has 0 completed lessons and submissions at lessons 4–11, impossible via the product | relabelled as an example until real work exists |

Verified working and worth keeping: the verdict system (correct on its first-ever
real use), the rubric (93/100 on genuinely grounded work), the conversation
(8/10 with actionable "how to reach 10"), and the retry loop, which took the
design partner from 30 to 79.

**Still open, deliberately:** the portfolio needs 3 *distinct* work items — three
lessons — so nobody has ever reached it; and the conversation bonus is invisible
when the work already scores 100 (`min(100, score+bonus)`). Both are design
decisions, not bugs, and should be decided rather than patched.

## Parked designs (specified, deliberately not built)

**Module time-gate.** A motivated learner can binge a "30-day" course in a
weekend. Design: module N+1 unlocks when module N is complete **and** ≥5 days
have passed since module N's *first* lesson completion — invisible at a healthy
pace, binding only on crammers; derivable from existing timestamps
(`MODULE_GATE_DAYS`, 0 = off). Submitting the module's reto shortens the wait to
3 days: an *earned* fast lane. Locked-module UI frames the wait as práctica days.
**Prerequisite:** email, so "tu módulo se abrió" can reach people. ~1 hour.

**"Mi portafolio" public hub.** One public URL per learner listing their
documents and case studies — the platform *becomes* the portfolio site that job
seekers should have and mostly don't. Builds on existing share tokens.

**Voice explain-back.** "Mándame un audio" fits LatAm's WhatsApp culture.
Server-side `faster-whisper` in our own container (free). V2 — the text loop
must prove itself first.

**Critique exercises.** A generated artifact with three planted flaws: find
them, fix them, justify. Detection of subtle wrongness is the strongest
comprehension test there is and it is literally the job now. Rides with the next
course generation.

**On-demand course generation.** The end-state: request → deep research →
course, self-serve. Sequenced *after* retention validation on purpose — supply
was never the bottleneck, and the concierge already rehearses the flow manually.

**Smaller:** health monitoring (a
dead OpenRouter key currently fails silently as 503s); admin analytics panel;
video CDN if beta bandwidth demands it. *(Prompt-injection delimiters and
session/token purge shipped 2026-08-12 — see the hardening section above.)*

## Risks

| Risk | Mitigation in place |
|---|---|
| Edutainment trap (watching ≠ learning) | Evidence-based exercises, comprehension verdicts, capstones; gates measured on submission |
| AI evaluation drift | Shared `VOICE_GUIDE`, per-kind contracts, `rubric_version`; **`check_tutor.py` (6 cases) — run it before touching an evaluator prompt** |
| Factual errors in paid content | Research-grounded generation, evidence-tier discipline; **courses 4–7 unreviewed** |
| Fabricated-looking portfolios | Compiler refuses invented metrics; projections labelled |
| Single-operator bus factor | These docs, TOML-as-truth, idempotent pipelines, boring schema |
| Building past the evidence | The reading view now exists — use it |
