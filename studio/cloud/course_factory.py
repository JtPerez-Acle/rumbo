"""Course factory: brief (+ optional research) → syllabus DAG → lesson videos + quizzes.

Multi-course: pass the course slug as the first argument to any command. Each
course is defined by channels/<slug>.toml (kind="course", with course_brief and
optional research_file keys). Lessons can be grounded in provided research so
fast-changing topics (ad platforms) stay factually accurate.

Usage:
    python course_factory.py <slug> preflight   # validate BEFORE generating (exit != 0 on problems)
    python course_factory.py <slug> verify      # count what exists (exit != 0 if incomplete)
    python course_factory.py <slug> syllabus    # generate/print the syllabus
    python course_factory.py <slug> compile     # write lessons + queue renders
    python course_factory.py <slug> render       # render queued videos
    python course_factory.py <slug> reconcile    # match rendered mp4s to nodes
    python course_factory.py <slug> backfill-text # add key_points/transcript to nodes
    python course_factory.py <slug> capstones    # generate per-module integrative retos
    python course_factory.py <slug> fix-titles   # sentence-case existing titles
    python course_factory.py <slug> status       # node status summary

Videos are canonical per node (rendered once, reused for every learner);
personalization lives in each learner's path.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path

from loguru import logger

STUDIO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STUDIO))

from cloud import db, writer  # noqa: E402
from cloud.writer import _chat, _channel_system  # noqa: E402

PENDING_DIR = STUDIO / "queue" / "pending"

# Set by main() from the CLI slug argument.
COURSE_SLUG = "curso-marketing-ia"


def _profile() -> dict:
    return tomllib.load(open(STUDIO / "channels" / f"{COURSE_SLUG}.toml", "rb"))


def _course_meta() -> tuple[str, str, str, str]:
    """(title, learner-facing description, internal brief, catalog category)
    from the course TOML. `niche` is what learners see; `course_brief` drives
    generation only; `category` groups the catalog."""
    p = _profile()
    return (p["name"], p.get("niche", ""),
            p.get("course_brief", p.get("niche", "")), p.get("category", ""))


def _research() -> str:
    """Load the course's research source material, if configured and present.
    Tolerates stray non-UTF-8 bytes (pasted research files sometimes carry a few)
    — a single bad byte must never zero out a course generation."""
    p = _profile()
    rf = p.get("research_file", "")
    if not rf:
        return ""
    path = STUDIO / "research" / rf
    if not path.is_file():
        return ""
    return path.read_bytes().decode("utf-8", errors="replace")


def generate_syllabus() -> list[dict]:
    title, _, brief, _ = _course_meta()
    research = _research()
    research_block = (
        "MATERIAL DE INVESTIGACIÓN (basa el temario en esto; refleja funciones, "
        "pasos y buenas prácticas reales, no inventadas):\n" + research + "\n\n"
        if research else ""
    )
    result = _chat(
        _channel_system(_profile()),
        (
            f"{research_block}"
            f"Diseña el temario completo del curso «{title}».\n\n"
            f"Brief: {brief}\n\n"
            "Responde con JSON: {\"modules\": [{\"no\": 1-5, \"title\": str, "
            "\"description\": \"1-2 frases (máx 35 palabras) de lo que el alumno "
            "PODRÁ HACER al terminar el módulo — contrato de resultado, de tú\", "
            "\"lessons\": [{\"slug\": \"kebab-case-corto\", \"title\": str, "
            "\"objectives\": \"lo que el alumno PODRÁ HACER al terminar (verbos de "
            "acción, medible)\", \"angle\": \"el enfoque único de la lección en 1 "
            "frase\"}] (6 por módulo)}]}\n"
            "Progresión estricta: cada lección asume solo lo cubierto antes.\n"
            # Platform contract (docs/02): every course opens by having the
            # learner choose the real project every later exercise builds on.
            # It lived only in course_brief, and the syllabus prompt optimises
            # for topic coverage — so 3 of 4 new courses silently dropped it.
            # Without it the exercises have nothing concrete to be grounded in,
            # which is precisely what the Aplicación dimension scores.
            "OBLIGATORIO: la lección 1 es SIEMPRE donde el alumno elige el "
            "proyecto real y concreto sobre el que trabajará todo el curso (su "
            "negocio, una marca real, una organización, un equipo, un fenómeno "
            "que estudie). Su título y su objetivo deben decir eso explícitamente. "
            "Las demás lecciones asumen que ese proyecto ya está elegido."
        ),
    )
    nodes, position = [], 0
    for module in result["modules"]:
        for lesson in module.get("lessons", []):
            slug = (lesson.get("slug") or lesson.get("title", f"leccion-{position+1}"))
            if not lesson.get("title"):
                continue
            position += 1
            nodes.append({
                "module_no": module.get("no", 1),
                "module_title": module.get("title", ""),
                "module_description": module.get("description", ""),
                "position": position,
                "slug": re.sub(r"[^a-z0-9-]", "", slug.lower().replace(" ", "-"))[:60] or f"leccion-{position}",
                "title": lesson["title"],
                "objectives": lesson.get("objectives", ""),
                "angle": lesson.get("angle", ""),
            })
    return nodes


def cmd_syllabus() -> None:
    with db.connect() as conn:
        course = db.ensure_course(conn, COURSE_SLUG, *_course_meta())
        nodes = db.course_nodes(conn, course["id"])
        if not nodes:
            logger.info("generating syllabus...")
            for node in generate_syllabus():
                db.add_node(conn, course["id"], node)
            conn.commit()
            nodes = db.course_nodes(conn, course["id"])
        current_module = None
        for n in nodes:
            if n["module_no"] != current_module:
                current_module = n["module_no"]
                print(f"\nMÓDULO {n['module_no']}: {n['module_title']}", flush=True)
            print(f"  {n['position']:2d}. [{n['status']:9s}] {n['title']}", flush=True)


def cmd_compile(limit: int | None = None) -> None:
    profile = _profile()
    research = _research()
    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    # Fetch the draft list once, then use a fresh short-lived DB connection per
    # lesson. A long-held connection dies over Railway's public proxy during the
    # ~30-minute run; per-lesson connections keep each write independent.
    with db.connect() as conn:
        course = db.ensure_course(conn, COURSE_SLUG, *_course_meta())
        drafts = db.course_nodes(conn, course["id"], status="draft")
    if limit:
        drafts = drafts[:limit]
    for node in drafts:
        try:
            spec = writer.write_lesson(profile, node, research=research)
            entry = {
                "channel": COURSE_SLUG,
                "subject": spec.get("subject", node["title"]),
                "title": spec["title"],
                "description": spec.get("description", ""),
                "hashtags": [],
                # SPOKEN form: the transcript keeps the readable one.
                # One string cannot serve both a reader and a voice.
                "script": writer.narration_text(spec["script"]),
                "terms": spec["terms"],
            }
            # Namespaced by course: the old name was curso-<pos>-<slug>.json with
            # no course in it, so two courses sharing a position and slug
            # silently overwrote each other's queue entry. Now that lesson 1 is
            # always "elige tu proyecto" in every course, that collision went
            # from unlikely to probable. (Rendering was never affected —
            # generate_batch filters on the `channel` field inside the JSON.)
            (PENDING_DIR / f"{COURSE_SLUG}-{node['position']:02d}-{node['slug']}.json").write_text(
                json.dumps(entry, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            with db.connect() as conn:
                db.update_node(conn, node["id"], status="scripted", quiz=spec["quiz"],
                               transcript=spec["script"], key_points=spec.get("key_points", []),
                               written=spec.get("written", ""), diagrams=spec.get("diagrams", []),
                               explain_prompt=spec.get("explain_prompt", ""))
                conn.commit()
            logger.info(f"lesson {node['position']:02d} scripted: {spec['title']}")
        except Exception as exc:
            logger.error(f"lesson {node['position']} ({node['slug']}) failed: {exc}")
            continue


def cmd_backfill_text() -> None:
    """Add transcript + key_points to nodes that don't have them yet, reading the
    script from the rendered queue json (queue/done). For courses generated before
    the written-text feature."""
    done = STUDIO / "queue" / "done"
    with db.connect() as conn:
        course = db.ensure_course(conn, COURSE_SLUG, *_course_meta())
        nodes = db.course_nodes(conn, course["id"])
    for node in nodes:
        if node.get("key_points"):
            continue
        # Namespaced name first; fall back to the legacy un-namespaced one for
        # courses rendered before the queue filenames carried the course slug.
        files = sorted(done.glob(f"*{COURSE_SLUG}-{node['position']:02d}-{node['slug']}.json")) \
            or sorted(done.glob(f"*curso-{node['position']:02d}-{node['slug']}.json"))
        if not files:
            logger.warning(f"lesson {node['position']:02d}: no script file to backfill")
            continue
        try:
            entry = json.loads(files[0].read_text(encoding="utf-8"))
            script = entry.get("script", "")
            points = writer.key_points_from_script(script) if script else []
            with db.connect() as conn:
                db.update_node(conn, node["id"], transcript=script, key_points=points)
                conn.commit()
            logger.info(f"lesson {node['position']:02d}: backfilled {len(points)} key points")
        except Exception as exc:
            logger.error(f"lesson {node['position']:02d} backfill failed: {exc}")


def cmd_render() -> None:
    subprocess.run(
        [sys.executable, str(STUDIO / "generate_batch.py"), "--channel", COURSE_SLUG],
        check=False,
    )


def cmd_reconcile() -> None:
    output_dir = STUDIO / "output" / COURSE_SLUG
    with db.connect() as conn:
        course = db.ensure_course(conn, COURSE_SLUG, *_course_meta())
        for node in db.course_nodes(conn, course["id"], status="scripted"):
            # Rendered filenames derive from the queue entry's name, so they
            # carry the course slug now. Match the namespaced form first and
            # fall back to the legacy one for courses rendered before that.
            matches = (list(output_dir.glob(
                           f"*{COURSE_SLUG}-{node['position']:02d}-{node['slug']}.mp4"))
                       or list(output_dir.glob(
                           f"*curso-{node['position']:02d}-{node['slug']}.mp4")))
            if matches:
                db.update_node(
                    conn, node["id"], status="rendered",
                    video_file=f"{COURSE_SLUG}/{matches[0].name}",
                )
                conn.commit()
                logger.info(f"lesson {node['position']:02d} rendered: {matches[0].name}")


def cmd_fix_titles() -> None:
    """One-shot: rewrite existing node titles into Spanish sentence case,
    preserving acronyms and brand names. Fixes titles generated before the
    sentence-case rule existed."""
    with db.connect() as conn:
        course = db.ensure_course(conn, COURSE_SLUG, *_course_meta())
        nodes = db.course_nodes(conn, course["id"])
    titles = {str(n["position"]): n["title"] for n in nodes}
    result = _chat(
        "Corriges títulos de lecciones al español correcto. Responde solo JSON.",
        (
            "Reescribe cada título en formato oración del español: solo la primera "
            "letra en mayúscula, más nombres propios y siglas (IA, SMART, PAS, CTA, "
            "KPI, ROI, Instagram, Facebook, Google, Zapier, ChatGPT, A/B). No cambies "
            "el significado ni acortes. Devuelve JSON {\"titles\": {\"1\": \"...\", ...}} "
            "con las mismas claves.\n\n" + json.dumps(titles, ensure_ascii=False)
        ),
    )
    fixed = result.get("titles", {})
    with db.connect() as conn:
        for n in nodes:
            new = fixed.get(str(n["position"]))
            if new and new != n["title"]:
                conn.execute("UPDATE syllabus_nodes SET title=%s WHERE id=%s", (new, n["id"]))
                logger.info(f"{n['position']:02d}: {new}")
        conn.commit()


def cmd_backfill_explain() -> None:
    """Generate the lesson-specific explain-back question for nodes that lack one
    (lessons compiled before explain_prompt existed). Idempotent."""
    with db.connect() as conn:
        course = db.ensure_course(conn, COURSE_SLUG, *_course_meta())
        nodes = db.course_nodes(conn, course["id"])
    for node in nodes:
        if node.get("explain_prompt"):
            continue
        try:
            prompt = writer.explain_prompt_from_lesson(
                node["title"], node.get("objectives") or "", node.get("transcript") or "")
            if not prompt:
                logger.warning(f"lesson {node['position']:02d}: empty explain prompt, skipped")
                continue
            with db.connect() as conn:
                db.update_node(conn, node["id"], explain_prompt=prompt)
                conn.commit()
            logger.info(f"lesson {node['position']:02d}: {prompt}")
        except Exception as exc:
            logger.error(f"lesson {node['position']:02d} explain backfill failed: {exc}")


def cmd_check_narration() -> None:
    """Flag scripts written with page-only devices (blanks, markdown, hashtags).

    Severity depends on whether the lesson has been rendered yet:

      not rendered  -> ERROR. The narration is about to be generated; fix the
                       script now, because a blank you cannot fill while
                       watching a 60-second video is weak teaching anyway.
      rendered      -> warning. `narration_text` sanitises at queue time, so the
                       audio is already correct; the script is merely odd for
                       video and worth rewriting on the next pass.

    The first version failed on everything containing an underscore, which after
    remediation meant failing forever on 13 lessons whose audio was already
    fixed. A check that always fails is a check nobody runs.
    """
    with db.connect() as conn:
        course = db.ensure_course(conn, COURSE_SLUG, *_course_meta())
        nodes = db.course_nodes(conn, course["id"])
    blocking = 0
    for n in nodes:
        warn = writer.narration_warnings(n.get("transcript") or "")
        if not warn:
            continue
        if n.get("video_file"):
            logger.warning(f"lección {n['position']:02d}: {'; '.join(warn)} "
                           f"(audio ya saneado al renderizar)")
        else:
            blocking += 1
            logger.error(f"lección {n['position']:02d}: {'; '.join(warn)} "
                         f"— se va a narrar así, corrige el guion")
    if blocking:
        logger.error(f"{blocking} lecciones sin renderizar con texto solo-para-página")
        raise SystemExit(1)
    logger.info(f"narración correcta en {len(nodes)} lecciones")


def cmd_backfill_written() -> None:
    """Generate the written guide (+ diagrams) for nodes that have a script but
    no `written`. Idempotent: a node that already has one is never touched, so
    this can be re-run after a partial failure.

    Exists because curso-marketing-ia predates the written-guide feature and is
    the only course missing it — on all 30 lessons, including the first lesson
    every new learner sees. Recompiling would regenerate scripts and quizzes for
    a course learners have already used; this only fills the gap.
    """
    with db.connect() as conn:
        course = db.ensure_course(conn, COURSE_SLUG, *_course_meta())
        nodes = db.course_nodes(conn, course["id"])
    todo = [n for n in nodes if not (n.get("written") or "").strip()]
    logger.info(f"{len(todo)} of {len(nodes)} lessons need a written guide")
    for node in todo:
        if not (node.get("transcript") or "").strip():
            logger.warning(f"lesson {node['position']:02d}: no transcript, skipped")
            continue
        try:
            spec = writer.written_guide_from_lesson(
                node["title"], node.get("objectives") or "",
                node.get("transcript") or "", course.get("title") or "")
            if not spec["written"]:
                logger.warning(f"lesson {node['position']:02d}: empty guide, skipped")
                continue
            with db.connect() as conn:
                db.update_node(conn, node["id"], written=spec["written"],
                               diagrams=spec["diagrams"])
                conn.commit()
            logger.info(f"lesson {node['position']:02d}: guide {len(spec['written'])} chars, "
                        f"{len(spec['diagrams'])} diagram(s)")
        except Exception as exc:
            logger.error(f"lesson {node['position']:02d} written backfill failed: {exc}")


def cmd_backfill_modules() -> None:
    """Generate outcome-focused module descriptions for courses created before the
    field existed. One LLM call per course; idempotent."""
    with db.connect() as conn:
        course = db.ensure_course(conn, COURSE_SLUG, *_course_meta())
        nodes = db.course_nodes(conn, course["id"])
    if not nodes:
        logger.warning("no syllabus yet, skipping")
        return
    modules: dict[int, dict] = {}
    for n in nodes:
        m = modules.setdefault(n["module_no"], {"title": n["module_title"], "lessons": []})
        m["lessons"].append(n)
    missing = {no for no, m in modules.items()
               if not (m["lessons"][0].get("module_description") or "").strip()}
    if not missing:
        logger.info("all modules already described, skipping")
        return
    title, _, _, _ = _course_meta()
    descriptions = writer.write_module_descriptions(title, modules)
    with db.connect() as conn:
        for no in sorted(missing):
            desc = descriptions.get(no, "")
            if not desc:
                logger.warning(f"module {no}: no description generated")
                continue
            conn.execute(
                "UPDATE syllabus_nodes SET module_description = %s "
                "WHERE course_id = %s AND module_no = %s",
                (desc, course["id"], no),
            )
            logger.info(f"module {no}: {desc}")
        conn.commit()


def cmd_backfill_prereqs() -> None:
    """Extract within-course module prerequisites (docs/09): the data that makes
    module-skipping routes safe. One LLM call per course; idempotent — modules
    that already carry prereqs are kept."""
    with db.connect() as conn:
        course = db.ensure_course(conn, COURSE_SLUG, *_course_meta())
        nodes = db.course_nodes(conn, course["id"])
    if not nodes:
        logger.warning("no syllabus yet, skipping")
        return
    modules: dict[int, dict] = {}
    for n in nodes:
        m = modules.setdefault(n["module_no"], {
            "title": n["module_title"], "description": n.get("module_description") or "",
            "lessons": []})
        m["lessons"].append(n)
    have = {no for no, m in modules.items()
            if m["lessons"][0].get("module_prereqs") is not None}
    if have == set(modules):
        logger.info("all modules already have prereqs, skipping")
        return
    title, _, _, _ = _course_meta()
    prereqs = writer.extract_module_prereqs(title, modules)
    with db.connect() as conn:
        for no, m in sorted(modules.items()):
            deps = prereqs.get(no)
            if deps is None:
                logger.warning(f"module {no}: no prereqs extracted, defaulting to "
                               f"strict-sequence (all earlier modules)")
                deps = list(range(1, no))
            for lesson in m["lessons"]:
                db.update_node(conn, lesson["id"], module_prereqs=deps)
        conn.commit()
    for no in sorted(modules):
        got = prereqs.get(no, list(range(1, no)))
        logger.info(f"module {no} prereqs: {got or 'ninguno (autónomo)'}")


def cmd_capstones() -> None:
    """Generate the integrative challenge (reto) for each module that lacks one.
    Idempotent: existing capstones are kept."""
    profile = _profile()
    research = _research()
    with db.connect() as conn:
        course = db.ensure_course(conn, COURSE_SLUG, *_course_meta())
        nodes = db.course_nodes(conn, course["id"])
        existing = {c["module_no"] for c in db.course_capstones(conn, course["id"])}
    modules: dict[int, dict] = {}
    for n in nodes:
        m = modules.setdefault(n["module_no"], {"title": n["module_title"], "lessons": []})
        m["lessons"].append(n)
    for module_no in sorted(modules):
        if module_no in existing:
            logger.info(f"module {module_no}: capstone already exists, skipping")
            continue
        try:
            spec = writer.write_capstone(
                profile, module_no, modules[module_no]["title"],
                modules[module_no]["lessons"], research=research,
            )
            with db.connect() as conn:
                course = db.ensure_course(conn, COURSE_SLUG, *_course_meta())
                db.add_capstone(conn, course["id"], module_no, spec)
                conn.commit()
            logger.info(f"module {module_no} capstone: {spec['title']}")
        except Exception as exc:
            logger.error(f"module {module_no} capstone failed: {exc}")


def cmd_sync() -> None:
    """Push the TOML's title/description/brief to the courses row. Run after
    editing a course TOML; no other side effects."""
    with db.connect() as conn:
        course = db.ensure_course(conn, COURSE_SLUG, *_course_meta())
        conn.commit()
    print(f"{course['slug']}: title={course['title']!r}", flush=True)
    print(f"  description={course['description']!r}", flush=True)


# Catalog clusters. Coarse on purpose — a category with one course looks broken
# (docs/04). Adding one is a deliberate act, so it lives here and preflight
# refuses anything else rather than silently bucketing it into "Más cursos".
CATEGORIES = {
    "Marketing y contenido",
    "Publicidad digital",
    "Analítica y automatización",
    "Ciencias sociales",
    "Deporte",
    "Redes y creadores",
}

REQUIRED_TOML = ("name", "slug", "niche", "category", "audience", "tone",
                 "cta", "course_brief")


def cmd_preflight() -> int:
    """Validate everything checkable BEFORE burning 2-3 hours of generation.

    Every check here corresponds to something that actually went wrong once:
    a single invalid byte in a research file zeroed a whole course while the
    pipeline logged "done"; a course shipped with the default deliverable
    because nobody added a PROJECT_TEMPLATES entry; catalog cards broke when a
    niche line ran long. Cheap to run, and it is the only step that can save a
    wasted afternoon. Returns a non-zero exit code on any failure.
    """
    problems: list[str] = []
    notes: list[str] = []
    toml_path = STUDIO / "channels" / f"{COURSE_SLUG}.toml"
    if not toml_path.is_file():
        print(f"FAIL  no existe {toml_path}", flush=True)
        return 1
    p = _profile()

    for key in REQUIRED_TOML:
        if not str(p.get(key, "")).strip():
            problems.append(f"TOML: falta `{key}`")
    if p.get("kind") != "course":
        problems.append('TOML: `kind` debe ser "course"')
    if p.get("slug") and p["slug"] != COURSE_SLUG:
        problems.append(f"TOML: slug={p['slug']!r} no coincide con el archivo {COURSE_SLUG!r}")

    niche = str(p.get("niche", ""))
    if len(niche) > 110:
        problems.append(f"TOML: `niche` tiene {len(niche)} chars (máx 110) — "
                        f"la tarjeta del catálogo se corta")
    if re.match(r"(?i)^curso\b", niche):
        problems.append("TOML: `niche` repite el título; debe ser solo la promesa de resultado")
    # Course titles carry no time claim (dropped 2026-08-12): a route may send a
    # learner through 12 lessons of a course, so "en 30 días" contradicted the
    # route on the very next screen. The card already states "N lecciones · N
    # módulos" factually, one line below the title.
    if re.search(r"(?i)en \d+ d[ií]as", str(p.get("name", ""))):
        problems.append("TOML: `name` no debe prometer una duración — el conteo "
                        "de lecciones ya lo dice, y las rutas usan solo parte del curso")
    if p.get("category") and p["category"] not in CATEGORIES:
        problems.append(f"TOML: category={p['category']!r} no está en CATEGORIES "
                        f"({', '.join(sorted(CATEGORIES))}). Si es nueva, agrégala "
                        f"aquí a propósito y no dejes una categoría con un solo curso.")

    # A voice or stroke colour reused across COURSES makes two of them sound and
    # look like the same one. Social channels are excluded on purpose: they are
    # dormant, never heard alongside a course, and flagging them made preflight
    # cry wolf on a course that was fine.
    voice = (p.get("voice") or {}).get("voice_name", "")
    stroke = (p.get("style") or {}).get("stroke_color", "")
    for other in sorted((STUDIO / "channels").glob("*.toml")):
        if other.stem == COURSE_SLUG:
            continue
        try:
            q = tomllib.load(open(other, "rb"))
        except tomllib.TOMLDecodeError:
            continue
        if q.get("kind") != "course":
            continue
        if voice and (q.get("voice") or {}).get("voice_name") == voice:
            problems.append(f"voz {voice!r} ya la usa {other.stem}")
        if stroke and (q.get("style") or {}).get("stroke_color") == stroke:
            problems.append(f"color {stroke!r} ya lo usa {other.stem}")

    rf = p.get("research_file", "")
    if not rf:
        notes.append("sin research_file: el curso se generará solo desde course_brief")
    else:
        path = STUDIO / "research" / rf
        if not path.is_file():
            problems.append(f"research: no existe {path}")
        else:
            raw = path.read_bytes()
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError as exc:
                # _research() decodes with errors="replace" so this no longer
                # zeroes the course, but a mangled byte still corrupts content.
                problems.append(f"research: byte inválido en offset {exc.start} "
                                f"(el archivo debe ser UTF-8 limpio)")
                text = raw.decode("utf-8", errors="replace")
            words = len(text.split())
            if words < 3000:
                problems.append(f"research: solo {words} palabras — insuficiente para "
                                f"30 lecciones fundamentadas")
            elif words < 5000:
                notes.append(f"research: {words} palabras (los buenos van 6000-10000)")
            else:
                notes.append(f"research: {words} palabras")

    tpl = writer.PROJECT_TEMPLATES.get(COURSE_SLUG)
    if not tpl:
        problems.append(f"writer.PROJECT_TEMPLATES no tiene entrada para {COURSE_SLUG!r} — "
                        f"el curso entregaría el documento por defecto (auditoría)")
    else:
        notes.append(f"entregable: {tpl['doc_type']}")

    for n in notes:
        print(f"  ·  {n}", flush=True)
    for pr in problems:
        print(f"FAIL  {pr}", flush=True)
    if problems:
        print(f"\npreflight: {len(problems)} problema(s) — NO generes todavía", flush=True)
        return 1
    print("\npreflight OK", flush=True)
    return 0


def cmd_verify() -> int:
    """The counting ritual as a command. 'exit 0' is not verification (docs/07):
    a pipeline once reported success while producing zero lessons. This counts
    rows and returns non-zero with what is missing."""
    expected_caps = 5
    with db.connect() as conn:
        course = db.ensure_course(conn, COURSE_SLUG, *_course_meta())
        nodes = db.course_nodes(conn, course["id"])
        caps = conn.execute(
            "SELECT COUNT(*) AS n FROM module_capstones WHERE course_id = %s",
            (course["id"],)).fetchone()["n"]
    total = len(nodes)
    fields = {
        "lecciones": total,
        "con video": sum(1 for n in nodes if n["video_file"]),
        "con transcript": sum(1 for n in nodes if n.get("transcript")),
        "con module_description": sum(1 for n in nodes if n.get("module_description")),
        "con explain_prompt": sum(1 for n in nodes if n.get("explain_prompt")),
        "con quiz": sum(1 for n in nodes if n.get("quiz")),
        "con written": sum(1 for n in nodes if n.get("written")),
    }
    # `written` is optional: the oldest course predates the written-guide feature,
    # so an incomplete count there is a note, not a failure.
    OPTIONAL = {"con written"}
    problems, notes = [], []
    if total == 0:
        problems.append("0 lecciones — la generación no produjo nada")
    for label, got in fields.items():
        if label == "lecciones" or not total or got >= total:
            continue
        msg = f"{label}: {got}/{total} (faltan {total - got})"
        (notes if label in OPTIONAL else problems).append(msg)
    if caps != expected_caps:
        problems.append(f"capstones: {caps}/{expected_caps}")

    # Files actually present on this machine's output dir (the volume in prod).
    out = STUDIO / "output" / COURSE_SLUG
    on_disk = len(list(out.glob("*.mp4"))) if out.is_dir() else 0

    print(json.dumps({**fields, "capstones": caps, "mp4 en disco": on_disk},
                     ensure_ascii=False, indent=1), flush=True)
    for n in notes:
        print(f"  ·  {n} (opcional)", flush=True)
    if on_disk < fields["con video"]:
        print(f"  ·  {fields['con video'] - on_disk} videos marcados en la DB no están "
              f"en disco — si ya corriste reconcile, sube con upload_videos.py YA "
              f"(el curso aparece disponible y los alumnos ven reproductores rotos)",
              flush=True)
    for pr in problems:
        print(f"FAIL  {pr}", flush=True)
    if problems:
        print(f"\nverify: {len(problems)} problema(s)", flush=True)
        return 1
    print("\nverify OK", flush=True)
    return 0


def cmd_status() -> None:
    with db.connect() as conn:
        course = db.ensure_course(conn, COURSE_SLUG, *_course_meta())
        nodes = db.course_nodes(conn, course["id"])
        counts: dict = {}
        for n in nodes:
            counts[n["status"]] = counts.get(n["status"], 0) + 1
        print(json.dumps({"total": len(nodes), **counts}, ensure_ascii=False), flush=True)


def main(argv: list[str]) -> None:
    global COURSE_SLUG
    # First arg is the course slug when it matches a channels/<slug>.toml; else
    # default to the marketing course (back-compat with the old single-course CLI).
    args = list(argv)
    if args and (STUDIO / "channels" / f"{args[0]}.toml").is_file():
        COURSE_SLUG = args.pop(0)
    command = args[0] if args else "status"
    extra = args[1] if len(args) > 1 else None
    dispatch = {
        "preflight": cmd_preflight,
        "verify": cmd_verify,
        "syllabus": cmd_syllabus,
        "render": cmd_render,
        "reconcile": cmd_reconcile,
        "fix-titles": cmd_fix_titles,
        "backfill-text": cmd_backfill_text,
        "backfill-written": cmd_backfill_written,
        "check-narration": cmd_check_narration,
        "backfill-explain": cmd_backfill_explain,
        "backfill-modules": cmd_backfill_modules,
        "backfill-prereqs": cmd_backfill_prereqs,
        "capstones": cmd_capstones,
        "sync": cmd_sync,
        "status": cmd_status,
    }
    if command == "compile":
        cmd_compile(int(extra) if extra else None)
    elif command == "all":
        # Preflight gates the expensive part. Generation runs for hours; every
        # check it makes is one that has cost a real afternoon before.
        if cmd_preflight() != 0:
            sys.exit(1)
        cmd_syllabus(); cmd_compile(); cmd_render(); cmd_reconcile()
        cmd_backfill_text(); cmd_backfill_modules(); cmd_backfill_explain()
        cmd_capstones()
        # Prereqs feed the route matcher (docs/09); idempotent — existing
        # extractions are kept, so re-running `all` never re-spends.
        cmd_backfill_prereqs()
        sys.exit(cmd_verify())
    else:
        # Commands that return an int are checks: their exit code is the result.
        rc = dispatch.get(command, cmd_status)()
        if isinstance(rc, int):
            sys.exit(rc)


if __name__ == "__main__":
    main(sys.argv[1:])
