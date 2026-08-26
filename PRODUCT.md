# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

**Primary: Spanish-speaking adults in Latin America who want to get hired or grow
their own business.** Job seekers and early-career marketers, studying on a phone,
usually on mobile data, in stolen time around a job. They arrive with a goal
("quiero ser X"), not a curiosity about a subject. They are not students; nobody
is grading them for a school.

**Secondary: the operator.** A single person runs the whole product from a
token-gated dashboard — invites, reading learner work, triaging requests. At
current scale, reading every submission takes about fifteen minutes and is 100%
of the product's real usage. That stops being possible around 50 learners.

**Third: a stranger with no invite.** Someone who arrives from a shared document,
a bio link, or word of mouth and has to understand a product whose value —
verified work, not video — is invisible from the outside. Access is invite-gated,
so this person cannot simply try it.

## Product Purpose

A learner says what they want to be — pastes a real job posting, or names a role —
and the platform composes a **route** through a library of module-level
competencies, teaches it, verifies they learned it, and compiles their own
submitted work into a **client-grade work document under their byline**.

Each lesson is a 45–60 second vertical video (the why) plus a written guide (the
how), then an explain-it-back comprehension check that returns a verdict and never
a score, a quiz, and an exercise where the learner pastes work they actually
produced. An AI tutor scores work products on three dimensions, names what is
missing to reach 100, allows unlimited retries keeping the best, and asks one
ownership question only the person who did the work can answer.

Success is a learner finishing a module and producing an artifact they actually
use in front of an employer or client. Not a completion percentage, and
explicitly not a certificate.

## Positioning

Everything a learning product can hand a learner is one of three tiers: a
**certificate** ("an institution says I learned" — worth exactly the issuer's
reputation, which a new platform does not have), a **case study** ("a story about
what I did"), or a **work document** ("the thing a client would have paid for" —
its value is intrinsic and needs no endorsement). This product refuses tier one
and ships tier three.

The mechanism a neighbouring product could not truthfully copy: **generating
courses is now a commodity; verifying that someone learned and composing a
credible route through the library is the defensible half.** Two things follow
that competitors structurally do not do — every exercise is evaluated against the
lesson's real objectives with feedback quoting the learner's own words, and the
matcher reports **what the goal demands that we do not teach**. The system that
says "esto no lo cubrimos" is the one people trust about what it does cover.

## Operating Context

- **Phone-first, on mobile data.** Videos are re-encoded to ~5 MB per lesson
  specifically so a LatAm learner is not paying for the difference.
- **Invite-gated alpha.** Every account is created with a code the operator mints.
  Email delivery currently reaches exactly one inbox, so a returning learner
  cannot always let themselves back in and lands in an operator queue.
- **The library is 14 courses / 420 lessons / 70 modules**, each module carrying a
  declared outcome contract and declared prerequisites. Routes select module
  *sets*, prereq-closed server-side — the module, not the course, is the unit.
- **The daily shape** is one lesson: video → guide → explain-back → quiz →
  exercise with real evidence → the tutor's ownership question. Each module ends
  in a *reto*: a novel business case deliberately not covered in the lessons.
- **The learner declares one transversal project** at orientation — their own
  business, or a real brand they would like to work for — and every exercise
  builds on it, so the accumulated work composes into one document.
- **A learner may skip what they already know** by pasting a CV. The CV only ever
  *proposes* skips; a skip is credited only by passing that module's reto.
- Links get shared over WhatsApp. Share pages are public, unguessable-token URLs.

## Capabilities and Constraints

- **No build step, and this is deliberate.** Both frontends are single vanilla-JS
  HTML files with no bundler, no framework, and no test runner. A visual change
  belongs in the CSS token layer in `:root`, never in element styles.
- **CSP requires `'unsafe-inline'` for scripts** because of the single-file
  frontends, so DOMPurify — not CSP — is the real XSS control. Untrusted Markdown
  renders through `renderMD()` (marked → DOMPurify), never straight to
  `innerHTML`. CDN libraries are pinned to exact versions with SRI.
- **Three DOM-shim checks stand in for a test runner** and assert user-facing
  *promises*, not layout: the landing's "cómo funciona" block (13 assertions), the
  job-analysis result page (25), and the CV screen (37). They exist because copy
  here has aged silently before. Any overhaul keeps them green or changes them
  deliberately.
- **Hash routing throughout.** Back button, refresh and deep links all work, and
  lesson steps are individually addressable so a pending item surfaced anywhere is
  one tap from the place it can be answered.
- **Nothing a learner earns may ever go down** — work scores, quiz scores, the
  conversation bonus and credited module exemptions all keep the best attempt,
  enforced in SQL rather than by convention.
- **The server decides state; the client only displays it.** Access is recomputed
  per request in one place and every widening rule only ever adds.
- **Evaluations really take 25–35 seconds.** Any request that can outlive a
  learner's patience needs both a timeout and a saved draft.
- **Spanish only**, LatAm register, `tú` not `usted`.
- The admin surface is gated by a path allowlist; a new `/api/*` route not added
  to it ships public.

## Brand Commitments

- **The product is named Rumbo.** Confirmed 2026-08-26: the rename ships across
  the app chrome, the public surfaces, orientation, share pages and email. The
  live product previously said *Aprende IA*, and that name survives in the
  deployed URL and in the existing launch video.
- **El Taller Nocturno is the binding visual identity, to be refined and not
  replaced.** A night workshop: warm darkness, one amber lamp, and the learner's
  work glowing paper-white as the only light that matters. Its load-bearing rule:
  **the interface is grotesk (Archivo), the work is serif (Fraunces)** — documents
  and case studies are paper-styled pages.
- **Iconography is a drawn inline-SVG set** (single stroke, `currentColor`). No
  emoji in the chrome.
- **No badges and no XP.** A daily streak with a one-day grace is the only
  gamification. Measure first, decorate later.
- **Voice:** second person singular, LatAm Spanish, and a standing ban list of
  AI-slop vocabulary applied to every generated string, so the course and the
  tutor speak with one voice.
- **Editorial honesty is a product feature, not a disclaimer.** Name what is not
  covered; label projections as projections; never invent a metric, a capability,
  or a credential.

## Evidence on Hand

Real, and usable:

- **14 courses, 420 lessons, 420 rendered videos**, every lesson with a written
  guide — genuine generated content, not placeholder.
- **70 module outcome contracts** with declared prerequisites.
- Real job-posting fixtures in `studio/fixtures/job-postings/`, including one real
  posting that became the original course roadmap.
- A launch video and its composition in `brag-output/`.
- Real CVs used to calibrate the CV matcher live only on the operator's machine
  and are never committed.

Absences that future work must not paper over — verified against the live
database on 2026-08-26:

- **5 learner accounts, 16 submissions, 3 lesson completions — every one of them a
  lesson 1.** Nobody has ever reached a lesson 2. Most of those accounts belong to
  the operator or are seeded.
- **Zero portfolio documents compiled from a real learner's work.** The single
  existing document belongs to a seeded demo account. The landing already labels
  its sample document as an *example* for exactly this reason, and it must not be
  relabelled as a real learner's until one exists.
- **No testimonials, no customers, no pricing, no press, no case studies, no
  usage statistics.** None of these may be invented, implied, or mocked up as
  though real.

## Product Principles

1. **Proof over credentials.** Ship the artifact a client would have paid for; do
   not issue certificates.
2. **Verification is the product; the content is the delivery mechanism.** The
   defensible half is evaluating real work and composing the route to it.
3. **Say what we do not cover.** Honest gaps are the reason the coverage claim is
   believable at all.
4. **Nothing a learner earns may ever go down**, and the screen — not the schema —
   is where that promise has to be visible.
5. **Gate on doing, never on passing.** Feedback teaches; punishment churns.

## Accessibility & Inclusion

Established product facts: phone-first on low-end Android over metered mobile
data, Spanish-only, and an adult audience studying in short sessions around a job.

**Open decision:** no formal accessibility standard has ever been set for this
product, and none is currently verified. Establishing the target — and measuring
the existing screens against it — is in scope for the current overhaul rather
than assumed here.
