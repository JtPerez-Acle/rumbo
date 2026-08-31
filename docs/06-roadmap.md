# 06 — Status, roadmap and parked designs

*Verified against the live database 2026-08-31. Nothing in the table below moved
between 2026-08-26 and 2026-08-31, which is itself the finding: five days of
feature work shipped on 08-26 into a product whose last learner submission was
2026-08-21 and whose last completion of anything was 2026-08-07.*

## Where we actually are

Read this before planning anything, because it is the fact that should drive
every decision:

| | |
|---|---|
| Courses live | **14** (420 lessons, 420 videos, all with written guides) |
| Route library | 70 module contracts with declared prerequisites |
| Learners | **5** · 16 submissions · **3 lesson completions, every one of them a lesson 1** |
| Last completion of any kind | **2026-08-07** |
| Verdicts produced by a real learner | 1 (and it was the operator's own account) |
| Conversations answered | **1 of 4 asked**, and that one scored 0 |
| Transversal projects declared | **0 of 5** |
| Job analyses run | 3 (15 distinct gaps, **none recurring**) |
| Modules never selected by any route | **42 of 70** |
| Concierge requests / waitlist | 0 / 0 |
| CV intakes / exemptions claimed | **0 / 0** — shipped 08-26, never used |
| Public-landing demo attempts | **0** — the landing has converted nobody |
| Unresolved *Esperando acceso* rows | **1, waiting since 2026-08-24** |

**We build roughly seventy times faster than we learn.** The machinery is now
genuinely complete — goal engine, verified learning, portfolio compilation,
security hardening, two calibration suites — and the gap between what is built
and what is known is **wider than ever**, not narrower.

**The alpha exit criterion is unchanged and unmet:** one design partner completes
Module 1 (6 lessons) and produces an artifact she actually uses.

### What is blocking, concretely

1. ~~**Email reaches exactly one inbox.**~~ **RESOLVED 2026-08-31.** The domain
   `ponrumbo.com` was registered, verified in Resend (São Paulo region), and
   `EMAIL_FROM` repointed at it; a real magic link was sent and received. The
   blocker turned out to be one step further back than this page said —
   `aprende-ia.app`, which the runbook told you to *verify*, had never been
   registered, so there was nothing to verify and the runbook could not have
   worked as written. **A returning learner can now log themselves back in.**
   The one row still in *Esperando acceso* from 2026-08-24 predates the fix and
   needs a human to tell that person they can simply log in — a successful login
   does not clear the row.
2. **The 15-use invite code has been shared once, and that one use bounced.**
   *(Corrected 2026-08-31 — this page previously said it had never been shared.)*
   "Cohorte agosto 2026" sits at **1/15**: learner 42 signed up 2026-08-17, hit
   the returning-user wall the same day, was unblocked by hand the same day, and
   has never come back. That is no longer an untested funnel. It is one data
   point, and it is negative — and it failed at exactly the step item 1 blocks.
3. Only after those two does any of the roadmap below matter.

### What the data says NOT to do

**Do not build course #15.** 42 of 70 modules have never been selected for
anyone's goal, and no gap in the demand ledger recurs. The catalog is ahead of
demand, not behind it. `GET /api/demand` is the instrument that says so; check it
before generating anything.

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

*(Updated 2026-08-25.)*

1. ~~**Buy a sending domain, verify it, repoint `EMAIL_FROM`.**~~ **Done
   2026-08-31** — `ponrumbo.com`, verified, sending from São Paulo.
2. **Tell the person queued since 2026-08-24 that they can log in**, then
   **re-share the 15-use invite code** and watch what happens. The instruments
   are all in place — demand ledger, access queue, both calibration suites — and
   the one person who used the code in August walked into the login wall that no
   longer exists. This is now the top of the list, and nothing about it is a
   build.
3. **Read the submissions.** Not a build. Dashboard → Alumnos → *Leer su trabajo*.
   The reading view exists; the habit does not. Everything below is guesswork
   until this happens weekly.
4. **Human review of the unreviewed courses** — 10 of 14 have never been read by a
   human. Priority: module 1 of each, because at current traffic nobody reaches
   lesson 7. `check-narration` will also flag scripts written with page-only
   devices while you are in there.
5. **The conversation is still nearly idle** (1 of 4 answered) and **no learner has
   ever declared a transversal project** (0 of 5) despite the orientation fix.
   Both are worth watching in real usage before changing again — the project step
   has already been moved once on a hypothesis.
6. **Social channels** — built, dormant since July, blocked only on Upload-Post
   credentials. The public landing and shareable routes exist with nothing
   pointing traffic at them.

## Shipped 2026-08-26: CV intake (docs/10)

**The first feature demand pulled rather than supply pushed** — a real learner
asked for it. Given a project whose documented failure mode is building seventy
times faster than it learns, that provenance is the most interesting thing about
it and is worth protecting: it is the first entry on this page that answers a
person rather than a hypothesis.

A learner pastes their CV; the matcher proposes module skips, each with a quote
from the CV that must literally appear in it. **The CV proposes, the reto
disposes**: accepting a skip shortens the route and opens that module's reto but
changes no access at all, and only passing the reto (≥70) credits the module.
Skipped is never locked. Full contract, invariants and calibration in docs/10.

What the first calibration run showed, on real CVs: three engineering CVs
produced **zero** proposals against a marketing catalog (the refusal direction
works), and the one real marketing document exposed the matcher **paraphrasing
instead of quoting** — now dropped server-side. **Still uncalibrated: the
positive direction.** Every real CV on hand is an engineering CV, so what is
proven is that we refuse; that a genuine marketing CV gets the *right* skips
rests on a synthetic CV, which docs/07 says does not count. One real marketing
CV is the next thing this feature needs.

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
