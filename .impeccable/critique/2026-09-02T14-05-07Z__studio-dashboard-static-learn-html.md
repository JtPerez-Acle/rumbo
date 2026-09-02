---
timestamp: 2026-09-02T14-05-07Z
slug: studio-dashboard-static-learn-html
---
{
  "target": "studio/dashboard/static/learn.html",
  "date": "2026-09-02",
  "mode": "persuade",
  "provenance": "two isolated sub-agents (A design review, B detector+browser); not degraded",
  "verdict": "Design-specificity is split: the demo lesson is uncopyable, everything around it is a generic course marketplace chassis.",
  "heuristics": {"visibility":3,"match":3,"control":2,"consistency":2,"prevention":3,"recognition":3,"flexibility":2,"minimalist":2,"errors":1,"help":"n/a"},
  "causal_findings": [
    "Catalog owns the document outline: 14 of 17 h3s are course names",
    "Cursos is nav item 2 and /cursos is a top-level destination",
    "publicCourseCard shows '30 lecciones · 5 módulos' (volume-as-value), 14x on two pages",
    "Syllabus CTA reads 'Quiero tomar este curso' on all 14 SEO landing pages",
    "Wordmark subtitle 'Aprende haciendo, con tutora IA' is also the crawler H1 in prerender.py",
    "Peak-end: catalog is the last impression before the closing CTA",
    "/cursos og:description is '14 cursos, 420 lecciones' - inventory framing in every WhatsApp share"
  ],
  "not_causal": ["dark ground + amber lamp", "the 59s video", "the written guide", "existence of a library", "founder note"],
  "defects": [
    "5 nav anchors unfocusable (a with no href/tabindex) on all public pages - CONFIRMED live",
    "zero landmarks (nav/header/main/footer) on all 3 pages",
    "/curso/<slug> has no h1; landing and /cursos skip h1->h3",
    "9 of 22 interactive elements under 44x44 on mobile",
    "2 contrast pairs at 4.47:1 (#8b8296 on #221d2e), 0.03 short of AA",
    "lamp/grain absent on 4 of 6 public routes, including /oferta",
    "evaluate-failure path sets textContent only, no doors appended - dead end at the 4/hr cap",
    "post-hydration DOM has 6 anchors total, 5 without href: JS crawlers see zero internal links"
  ],
  "detector": {"exit": 2, "findings": 15, "real": ["dark-glow"], "false_positive": ["marquee (.readline i renders on no public page)"]},
  "perf": {"warm_domready_ms": {"/": 342, "/cursos": 300, "/curso/curso-seo-aeo": 277}, "console_errors": 0}
}
