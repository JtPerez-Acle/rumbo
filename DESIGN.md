---
name: Rumbo
description: A night workshop where the learner's own work is the only thing that glows.
colors:
  lamp-amber: "#F0A43C"
  lamp-amber-high: "#FFC670"
  lamp-amber-deep: "#AD7423"
  amber-ink: "#241603"
  paper: "#F1E6CE"
  paper-dim: "#CFC3A8"
  paper-ink: "#26200F"
  sage: "#A9C48F"
  sage-ink: "#1C2A12"
  terracotta: "#E5825E"
  terracotta-ink: "#33170C"
  workshop-night: "#100D17"
  panel: "#191521"
  raised: "#221D2E"
  line: "#2F2839"
  line-strong: "#453B54"
  text: "#F2EFE9"
  dim: "#B2AABB"
  faint: "#8B8296"
typography:
  display:
    fontFamily: "Fraunces, Georgia, serif"
    fontSize: "31px"
    fontWeight: 600
    lineHeight: 1.08
    letterSpacing: "-0.01em"
  headline:
    fontFamily: "Fraunces, Georgia, serif"
    fontSize: "26px"
    fontWeight: 600
    lineHeight: 1.08
    letterSpacing: "-0.01em"
  title:
    fontFamily: "Archivo, -apple-system, Segoe UI, system-ui, sans-serif"
    fontSize: "18px"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.015em"
  body:
    fontFamily: "Archivo, -apple-system, Segoe UI, system-ui, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "normal"
  label:
    fontFamily: "Archivo, -apple-system, Segoe UI, system-ui, sans-serif"
    fontSize: "11px"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "0.16em"
  numeral:
    fontFamily: "Fraunces, Georgia, serif"
    fontSize: "42px"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.02em"
    fontFeature: "tabular-nums"
  mono:
    fontFamily: "ui-monospace, Menlo, monospace"
    fontSize: "11px"
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "normal"
rounded:
  sm: "10px"
  md: "14px"
  lg: "20px"
  pill: "999px"
spacing:
  s1: "4px"
  s2: "8px"
  s3: "12px"
  s4: "16px"
  s5: "24px"
  s6: "32px"
components:
  button-primary:
    backgroundColor: "{colors.lamp-amber}"
    textColor: "{colors.amber-ink}"
    rounded: "{rounded.pill}"
    padding: "14px 22px"
    typography: "{typography.title}"
  button-ghost:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.text}"
    rounded: "{rounded.pill}"
    padding: "14px 22px"
  button-paper:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.paper-ink}"
    rounded: "{rounded.pill}"
    padding: "14px 22px"
  card:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.text}"
    rounded: "{rounded.lg}"
    padding: "{spacing.s4}"
  card-hero:
    backgroundColor: "{colors.raised}"
    textColor: "{colors.text}"
    rounded: "{rounded.lg}"
    padding: "24px 16px"
  card-paper:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.paper}"
    rounded: "{rounded.lg}"
    padding: "{spacing.s4}"
  input:
    backgroundColor: "{colors.raised}"
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
    padding: "14px"
  input-focus:
    backgroundColor: "{colors.raised}"
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
    padding: "14px"
  pill:
    backgroundColor: "{colors.raised}"
    textColor: "{colors.faint}"
    rounded: "{rounded.pill}"
    padding: "4px 9px"
  lesson-row:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
    padding: "12px 16px"
---

# Design System: Rumbo

## Overview

**Creative North Star: "El Taller Nocturno" (The Night Workshop)**

This is a workshop after hours. The room is warm and dark, there is exactly one
lamp above the bench, and the only thing that truly glows is the work on the
table. That is not decoration — it is the product argument rendered as light. The
platform's whole thesis is that the learner's output, not the platform's
credential, is what has value; so the interface deliberately recedes into warm
darkness and the learner's own work is rendered as paper, lit, slightly warm, the
brightest thing on any screen.

The atmosphere is calm and adult. Learners are working people studying in stolen
time around a job, on a phone, often tired. Nothing shouts, nothing celebrates
prematurely, nothing infantilises. Density is generous rather than compressed:
one decision per screen, a single orchestrated rise on page enter rather than
scattered animation. Where other learning products reach for confetti, badges and
progress dopamine, this one reaches for the feeling of a quiet bench and good
light.

The palette is earth, never neon. Success is sage, not lime; failure is
terracotta, not red. The two accents mean two different things and never trade
places: **amber is the room's light** (where to act, where you are), **paper is
the work** (what you made, what you will show someone). An interface element
never wears paper, and a piece of learner output is never amber.

**Key Characteristics:**
- Warm near-black ground (`#100D17`) with a single radial amber wash from above
- One amber accent used sparingly as light, not as brand paint
- Paper tones reserved exclusively for learner-authored output
- Grotesk interface, serif work: Archivo for the app, Fraunces for documents and numbers
- Six type sizes, three surface tiers, three radii — a deliberately small vocabulary
- No shadow scale; the only two shadows are glows that mean "lit"
- Drawn single-stroke SVG icons, never emoji, in the chrome
- Film grain at 3.5% opacity over the whole page

## Colors

Earth pigments under lamplight: a warm violet-black room, one amber source, and
warm off-white paper. Nothing in the palette is fully saturated and nothing is cool.

### Primary
- **Lamp Amber** (`#F0A43C`): the light in the room. Primary actions, the current
  step, active tab, eyebrow labels, the streak flame, progress fill. It marks
  *where to act and where you are* — never used to decorate a surface.
- **Lamp Amber High** (`#FFC670`): the hot centre of the light. Gradient tops on
  primary buttons, the roaring streak, a mid verdict.
- **Lamp Amber Deep** (`#AD7423`): the falloff. Gradient bases, progress-bar
  starts, the brandmark's lower edge.
- **Amber Ink** (`#241603`): text sitting *on* amber. Never a background.

### Secondary
- **The Paper** (`#F1E6CE`): warm off-white, reserved for the learner's own work —
  compiled documents, the copy-paste starting prompt, the portfolio card, the
  landing's document mock. The single most important semantic in the system.
- **Paper Dim** (`#CFC3A8`): paper at rest or secondary within a paper surface.
- **Paper Ink** (`#26200F`): text on paper.

### Tertiary
- **Sage** (`#A9C48F`) / **Sage Ink** (`#1C2A12`): correct, completed, *lo tienes*.
  A dried-herb green, deliberately not a "success green".
- **Terracotta** (`#E5825E`) / **Terracotta Ink** (`#33170C`): wrong, missing,
  *todavía no*, honest gaps. A clay orange-red, deliberately not an "error red" —
  being told what you are missing is not an error state.

### Neutral
- **Workshop Night** (`#100D17`): the room. Page ground and the inset of the brandmark.
- **Panel** (`#191521`): the bench. Default card and row surface.
- **Raised** (`#221D2E`): objects on the bench. Inputs, progress troughs, cluster
  headers, table headers.
- **Line** (`#2F2839`) / **Line Strong** (`#453B54`): hairline separation between
  tiers. Borders do the work shadows would do elsewhere.
- **Text** (`#F2EFE9`): primary reading colour, warm white.
- **Dim** (`#B2AABB`): secondary prose, supporting copy.
- **Faint** (`#8B8296`): micro-labels and de-emphasised meta. Tuned specifically to
  clear WCAG AA (4.5:1) on the workshop ground at 11px; it was `#7E7589` (4.39:1)
  and was raised without changing the palette's character.

### Named Rules

**The One Lamp Rule.** There is exactly one light source. Amber marks where to act
and where you are, and appears on well under 10% of any screen. The moment a
second amber element competes with the primary action on a view, one of them is
wrong.

**The Paper Is The Work Rule.** Paper tones (`#F1E6CE` family) are reserved for
things the *learner* authored or will show someone: documents, case studies, the
starting prompt, the portfolio surface. Chrome never wears paper, and learner
output is never amber. This is the palette carrying the product thesis.

**The Earth Rule.** Semantic colour is pigment, never signal-light. Sage and
terracotta only. No `#22C55E`, no `#EF4444`, no neon of any kind.

## Typography

**Display Font:** Fraunces (with Georgia, serif)
**Body Font:** Archivo (with `-apple-system`, Segoe UI, system-ui, sans-serif)

**Character:** A working pairing, not a fashionable one. Archivo is plain, tight
and legible at small sizes on a phone — it disappears, which is what an interface
should do. Fraunces is warm, slightly bookish and high-contrast, and it appears
only where the product wants to say *this is a made thing*: headlines, compiled
documents, and scores.

### Hierarchy
- **Display** (Fraunces 600, 31px, 1.08, `-0.01em`, `text-wrap: balance`): the one
  headline per view. Never two on a screen.
- **Headline** (Fraunces 600, 26px, 1.08): section-level headline, the second tier
  of the same voice.
- **Title** (Archivo 700, 18px, 1.2, `-0.015em`): card titles, course names,
  question stems. Back to the interface voice.
- **Body** (Archivo 400, 14px, 1.5): all reading copy. Two supporting steps exist
  (12.5px, 15.5px) for density, not hierarchy.
- **Label** (Archivo 700, 11px, uppercase): two variants that must not be
  confused — the **eyebrow** (`0.16em`, amber) names the current context and is
  the only uppercase amber in the system; the **microlabel** (`0.13em`, faint)
  names a group of things.
- **Numeral** (Fraunces 700, 42px, tabular): the evaluation score, and the score
  alone. The streak uses the same voice at 56px.
- **Mono** (`ui-monospace` / Menlo, 11px, 1.6): exactly one use — the copy-paste
  starting prompt handed to the learner before an exercise. It is monospace
  because it is *literally something to be copied*, and that is the only reason
  monospace is permitted in this product.

### Named Rules

**The Six Sizes Rule.** Six interface sizes exist (11 / 12.5 / 14 / 15.5 / 18 /
22px) plus three display sizes (26 / 31 / 42px). Adding a seventh is a design
failure, not a design decision.

**The Grotesk/Serif Split.** The interface is grotesk; the work is serif. If a
piece of text is *about* the product, it is Archivo. If it is *the thing the
learner made* — or the number naming its quality — it is Fraunces. This single
rule carries the identity further than the palette does.

**The Verdict Is Not A Grade Rule.** Comprehension checks render a serif *word*
(Lo tienes / Casi / Todavía no) at 22px and never a number. Only work products
get numerals. Putting a score on an explanation is a category error the product
has already made once and corrected.

## Layout

A single centred column, `max-width: 560px`, with `24px` vertical and `16px`
horizontal padding, and bottom padding that clears both the fixed tab bar and
`env(safe-area-inset-bottom)`. Full height is `100svh`, not `100vh`, so mobile
browser chrome does not crop the last row.

The spacing scale is a strict 4px ramp (`4 / 8 / 12 / 16 / 24 / 32`). Vertical
rhythm inside a view comes from a single `gap: 16px` on the column, so views are
composed by appending blocks rather than by tuning margins.

**Responsive behaviour is currently a single column at every width** — the app is
phone-first and has no breakpoints at all. On a wide viewport the column simply
centres in the dark ground. For the app this is a deliberate, defensible choice;
for any surface aimed at strangers arriving on a desktop it is a gap, not a style.

Page entry is one orchestrated rise: direct children of the column animate
`translateY(10px) → 0` with opacity, staggered `40ms` apart to a cap at the eighth
child. There is one motion idea per view, never several competing.

### Named Rules

**The One Column Rule.** Everything lives in one 560px column. There is no
sidebar, no two-up grid, and no desktop-specific layout inside the app. A screen
that needs two columns to work has too much on it.

## Elevation & Depth

**This system has no shadow scale, and that is deliberate.** Depth is tonal: three
stacked surface values (`Workshop Night` → `Panel` → `Raised`) separated by
hairline borders. A card is not lifted off the page; it is a lighter patch of the
same room.

The only two shadows in the system are **glows**, and they do not mean elevation —
they mean *this is lit*:

### Shadow Vocabulary
- **Amber glow** (`0 12px 34px -12px rgba(240,164,60,.5)`): on the primary action,
  the hero card and the spotlight card. The lamp falling on the thing you should
  touch.
- **Paper glow** (`0 10px 32px -14px rgba(241,230,206,.28)`): on paper surfaces and
  the paper button. The learner's work catching the light.

Two atmospheric layers sit above everything at `z-index: 0`, both
`pointer-events: none`: a `640×420px` radial amber wash anchored above the top
edge (the lamp itself), and an SVG fractal-noise grain at `3.5%` opacity (the
room's air). Content rides at `z-index: 1`.

### Named Rules

**The No-Shadow Rule.** Surfaces are flat and separated by tone and a hairline.
If something needs to feel closer, it gets *light* (a glow), not lift. There is no
`box-shadow` in this system that is not one of the two named glows.

## Shapes

Soft, generous, and consistently rounded — a workshop of worn edges rather than
machined ones. Three radii carry everything: `10px` for small inline objects
(notes, score pills, key caps, segmented buttons), `14px` for rows, inputs and
mid-weight cards, `20px` for primary cards and video. Anything interactive that
reads as a *control* rather than a *surface* goes fully round (`999px`): buttons,
pills, chips, progress bars, the streak flame.

Borders are always `1px` and almost always `Line`. State is expressed by tinting
that border with the state's own colour at 30–55% alpha rather than by thickening
it, so rows never shift by a pixel when their state changes.

The one deliberate break: the **document mock** on the landing uses a `6px` radius
and `rotate(-1.6deg)`. Paper is cut square and lies at an angle on a bench; it is
the only rotated element in the product and the only near-square corner.

## Components

### Buttons
- **Shape:** fully round (`999px`), full-width by default, `14px 22px`, weight 700
- **Primary:** amber gradient (`140deg`, High → Amber) on Amber Ink, with the amber
  glow. One per view.
- **Paper:** paper gradient (`150deg`, `#FBF3E1` → Paper) on Paper Ink, with the
  paper glow. Reserved for acting on the learner's own document.
- **Ghost:** `rgba(255,255,255,.04)` with a `Line` border; border brightens to
  `Line Strong` on hover.
- **Small:** auto-width, 12.5px, `9px 14px` — for inline actions inside a card.
- **States:** `:active` scales to `0.98` with a 150ms ease. **There is currently no
  `:hover` on primary or paper, and no `:focus-visible` anywhere in the system.**

### Cards / Containers
- **Corner Style:** `20px` (`14px` for the quiet variant)
- **Default** (`.card`): Panel on a `Line` hairline. The workhorse.
- **Hero** (`.card-hero`): `165deg` Raised → Panel, amber-tinted border, amber
  glow, roomier padding. The single "do this next" card on a view.
- **Paper** (`.card-paper`): Panel with a paper-tinted border and the paper glow —
  the learner's work, on the bench.
- **Spotlight** (`.card-spot`): full amber border, for a moment that deserves
  attention (the tutor's ownership question).
- **Quiet** (`.quiet`): `14px` radius, compressed padding, for supporting rows.

### Inputs / Fields
- **Style:** Raised ground, `Line` border, `14px` radius, `14px` padding, 15.5px text
- **Focus:** the border becomes Lamp Amber over 200ms. `outline: none` is set, and
  **no replacement focus ring is defined** — the border shift is the only cue.
- **Label:** 12.5px, weight 600, Dim, `4px` below.

### Navigation
- **Tab bar:** fixed to the bottom, `rgba(16,13,23,.9)` with a `14px` backdrop
  blur and a top hairline, four items, `10px` labels under `21px` icons, padded for
  the safe-area inset. Inactive is Faint; active is Lamp Amber.
- **Back:** a text affordance ("‹ Hoy"), Dim → Text on hover. Not a button.

### Signature: the lesson row (`.lrow`)
The temario's atom, and the clearest expression of the system. A `28px` rounded
square carrying either the lesson number or a state icon, the title, and a `10px`
uppercase state label. Completed rows take a sage number chip and a sage-tinted
border; the current row takes an amber chip and an amber border; locked and
upcoming rows drop to `55%` opacity. Tapping a locked row reveals its objectives
inline — nobody studies blind.

### Signature: the evaluation reveal
A 42px serif numeral counting up, three `5px` dimension bars filling behind their
labels, then the tutor's feedback. The score is coloured by band (sage / amber
high / terracotta) and is the only place a large number appears.

### Signature: the reading state (`.readline`)
A `3px` trough with a 40%-wide amber gradient sweeping across it on a 1.4s loop,
under the words "tu tutora está leyendo". Used wherever a real model call is in
flight (25–35s), because a dead spinner on a wait that long reads as a hang.

### Signature: the staged wait (`.jstage`)
For the ~2-minute route analysis: named stages that light one at a time against a
real elapsed clock, each with a sentence explaining what is actually happening.
Honest duration, not a fake percentage.

## Do's and Don'ts

### Do:
- **Do** put every visual change in the `:root` token block. A colour or size
  written inline is a bug in this codebase, not a shortcut.
- **Do** reserve paper tones for the learner's own output and amber for light and
  action, in every new surface.
- **Do** use tone and a hairline border for depth, and a glow only to mean "lit".
- **Do** state state on the border colour at 30–55% alpha, never by changing border
  width or the element's box size.
- **Do** render comprehension as a serif word and work quality as a serif numeral.
- **Do** keep one display headline and one primary action per view.
- **Do** name a real wait honestly and show what is happening during it.
- **Do** honour `prefers-reduced-motion` — the system already disables all
  animation and transition under it, and new motion must stay inside that rule.

### Don't:
- **Don't** introduce a seventh interface type size or a fourth radius.
- **Don't** add a generic `box-shadow` scale; the only shadows are the two glows.
- **Don't** use emoji in the chrome. Icons are the drawn single-stroke SVG set at
  `1.7` stroke width and `currentColor`.
- **Don't** use neon or signal-light semantics (`#22C55E`, `#EF4444`). Sage and
  terracotta only.
- **Don't** add badges, XP, levels, or confetti. The daily streak is the only
  gamification the product permits.
- **Don't** put a number on a comprehension check.
- **Don't** let an interface element wear paper, or a learner's document wear amber.
- **Don't** scatter animation. One orchestrated entrance per view.
