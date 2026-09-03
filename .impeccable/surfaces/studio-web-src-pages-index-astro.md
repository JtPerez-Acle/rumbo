---
version: 1
slug: "studio-web-src-pages-index-astro"
primary_target: "studio/web/src/pages/index.astro"
related_targets:
  - "studio/web/src/layouts/Public.astro"
  - "studio/web/src/components/DemoAsk.svelte"
  - "studio/web/src/components/VideoPlate.svelte"
  - "studio/web/src/components/TutorPanel.astro"
  - "studio/web/src/styles/app.css"
---

# Surface brief — the public landing (`/`)

<!-- Repointed 2026-09-02: this described `#/` inside learn.html, a 3,192-line
     single file that no longer exists. The landing is a built Astro page now and
     the brief below still describes it accurately — the surface did not change,
     only the file that implements it. -->

**Scope:** the unauthenticated landing, including the free lesson, the catalog
clusters and the two doors. Not the app behind login.

**Visitor mode:** Persuade.

**Audience & job:** a stranger with no invite, arriving from a shared document, a
bio link or word of mouth. They cannot try the product — access is invite-gated —
and its value (verified work, not video) is invisible from outside.

**Action:** understand the mechanism by experiencing it, then take one of three
doors: analyse a job posting, join the waitlist, or sign in with an invite.

**Proof / content:** the real first lesson of Marketing con IA — video, written
guide, key points — plus a real verdict from the production evaluator, and this
module's real exercise and reto. All live content, no mockups.

**Constraints:**
- No real learner document exists yet, and no testimonials, customers, pricing or
  press. None may be invented or implied. The old document mock was an example
  and has been removed rather than dressed up.
- The evaluator call is unauthenticated: 4/hour per IP, honeypot, one fixed
  lesson id that the caller can never choose.
- `renderHow` and `renderJobResult` are asserted by two copy checks; changing
  their promises means changing the checks deliberately.

**Direction:** "La lección, en vivo" (seed c4df1581, dealt lead). The page runs
the loop instead of describing it. Memorable moment: the serif verdict —
*Lo tienes / Casi / Todavía no* — landing on words the visitor wrote themselves,
with what is missing named underneath.

**Layout:** `body.wide` opens the public surface to 1000px at ≥900px and splits
the lesson two-up. Every other route stays the 560px phone column.

**Unresolved:** whether the demo lesson should rotate per visitor or stay fixed
(fixed for now — one lesson that stands alone is easier to keep honest); and
whether `demo_attempts` should feed the admin reading view.
