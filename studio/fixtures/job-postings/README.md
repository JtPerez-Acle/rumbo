# Job-posting fixtures for the matcher

Calibration inputs for `writer.analyze_job_posting`. Run them with
`python studio/cloud/check_job_matcher.py` before any change to
`JOB_MATCH_SYSTEM`, `JOB_JSON_SPEC` or `_normalise_job_analysis`.

**Why these live in the repo:** doc 06 names "evaluator fixtures die in a
session scratchpad" as a real risk. These don't.

| File | Kind | Pass condition |
|---|---|---|
| `real-content-ecommerce-latam.txt` | **Real.** The posting Liv is targeting (semi-senior content / e-commerce marketer), extracted from `liv-docs/liv-tema-a-estudiar.docx`. | Coverage 60–95 (measured: 83). Route names seo-aeo and email-marketing. **Planning tools (Trello/ClickUp/Notion) reported as a gap.** No baseline traits (ortografía, años de experiencia) in `competencies`. Ads courses stop **before module 5** — the posting says the role does not manage ad budget. Núcleo 12–54 lessons and listed first. |
| `adversarial-out-of-coverage.txt` | **Authored, deliberately.** A senior data-engineering role with nothing in our catalog. | **Coverage ≤ 20, route nearly empty, gaps honest, and `doc_type`/`doc_title`/`pitch` all empty.** If it invents a path through the marketing courses — or promises a deliverable — the prompt is broken. |

**One expectation here was wrong, and the catalog corrected it.** This file used
to require organic social-media management as a gap. It is not one:
`curso-marketing-ia` M3 covers *"posts para redes … planificarás un mes entero de
contenido"*. The assertion had also been passing by accident, because a substring
test for `"red"` matched `"Redacción"`. Two lessons: fixtures answer to the data,
and match on word boundaries.

## The authoring rule, and its one exception

Doc 07: *do not author your own calibration data* — the original rubric bug
survived because it was only ever tested against examples written by the person
who wrote the rubric.

That rule governs the **representative** cases: those must be real postings from
real people, and the set grows as stage-0 postings arrive.

The **degenerate** case is the exception, and doc 07 demands it separately:
*"include a degenerate input and confirm it scores badly."* You cannot collect a
"job that has nothing to do with us" from your own funnel, and its pass
condition is a refusal, not a judgement call. `adversarial-out-of-coverage.txt`
is authored on purpose and is labelled as such so nobody mistakes it for
evidence about real demand.

## Adding a posting

Drop the raw text in as `real-<role>-<market>.txt`, add a row above with its
expected shape, and re-run the checker. Never edit a real posting to make it
match better.
