"""Postgres state store for the studio: topic backlog (with no-repeat history)
and the publish log. Filesystem sidecars remain the source of truth for video
artifacts; the DB is the source of truth for what topics each channel has
covered and what has been posted where.
"""
from __future__ import annotations

import os

import psycopg
from psycopg.rows import dict_row

SCHEMA = """
CREATE TABLE IF NOT EXISTS topics (
    id SERIAL PRIMARY KEY,
    channel TEXT NOT NULL,
    slug TEXT NOT NULL,
    title TEXT NOT NULL,
    angle TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'idea',  -- idea | used
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    used_at TIMESTAMPTZ,
    UNIQUE (channel, slug)
);
CREATE TABLE IF NOT EXISTS publish_log (
    id SERIAL PRIMARY KEY,
    channel TEXT NOT NULL,
    video_file TEXT NOT NULL,
    title TEXT NOT NULL DEFAULT '',
    platform TEXT NOT NULL,
    request_id TEXT,
    published_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    slug TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'draft',  -- draft | live
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS syllabus_nodes (
    id SERIAL PRIMARY KEY,
    course_id INT NOT NULL REFERENCES courses(id),
    module_no INT NOT NULL,
    module_title TEXT NOT NULL DEFAULT '',
    position INT NOT NULL,                 -- global 1..N order
    slug TEXT NOT NULL,
    title TEXT NOT NULL,
    objectives TEXT NOT NULL DEFAULT '',   -- what the learner can DO afterwards
    angle TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'draft',  -- draft | scripted | rendered | approved
    video_file TEXT,
    quiz JSONB,                            -- {questions:[{q,options,answer,explain}], exercise:{...}}
    UNIQUE (course_id, slug)
);
CREATE TABLE IF NOT EXISTS learners (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL DEFAULT '',
    invite_code TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS invite_codes (
    code TEXT PRIMARY KEY,
    label TEXT NOT NULL DEFAULT '',
    max_uses INT NOT NULL DEFAULT 1,
    uses INT NOT NULL DEFAULT 0,
    active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS login_tokens (
    token TEXT PRIMARY KEY,
    learner_id INT NOT NULL REFERENCES learners(id),
    expires_at TIMESTAMPTZ NOT NULL,
    used BOOLEAN NOT NULL DEFAULT false
);
CREATE TABLE IF NOT EXISTS learner_sessions (
    token TEXT PRIMARY KEY,
    learner_id INT NOT NULL REFERENCES learners(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS module_capstones (
    id SERIAL PRIMARY KEY,
    course_id INT NOT NULL REFERENCES courses(id),
    module_no INT NOT NULL,
    title TEXT NOT NULL DEFAULT '',
    scenario TEXT NOT NULL,                -- novel client/situation, never covered in lessons
    deliverable TEXT NOT NULL,             -- the artifact the learner must produce
    rubric JSONB,                          -- [{criterion, expect}]
    UNIQUE (course_id, module_no)
);
CREATE TABLE IF NOT EXISTS submissions (
    id SERIAL PRIMARY KEY,
    learner_id INT NOT NULL REFERENCES learners(id),
    kind TEXT NOT NULL,                    -- explain | exercise | capstone
    node_id INT REFERENCES syllabus_nodes(id),
    capstone_id INT REFERENCES module_capstones(id),
    content TEXT NOT NULL,
    evaluation JSONB,                      -- {score, passed, feedback, misconception, improve}
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS waitlist (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL DEFAULT '',
    email TEXT NOT NULL UNIQUE,
    motivo TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'new',    -- new | invited | dismissed
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS job_targets (
    id SERIAL PRIMARY KEY,
    -- NULL on purpose: the analysis runs BEFORE login (it is the acquisition
    -- surface), and an anonymous row is still a demand signal worth keeping.
    learner_id INT REFERENCES learners(id),
    posting_text TEXT NOT NULL,
    role_title TEXT NOT NULL DEFAULT '',
    company TEXT NOT NULL DEFAULT '',
    analysis JSONB NOT NULL,
    active BOOLEAN NOT NULL DEFAULT false,
    share_token TEXT UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS course_requests (
    id SERIAL PRIMARY KEY,
    learner_id INT NOT NULL REFERENCES learners(id),
    topic TEXT NOT NULL,
    detail TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'new',    -- new | reviewing | building | published | rejected
    course_slug TEXT,                      -- set when the built course goes live
    admin_note TEXT NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS progress (
    id SERIAL PRIMARY KEY,
    learner_id INT NOT NULL REFERENCES learners(id),
    node_id INT NOT NULL REFERENCES syllabus_nodes(id),
    quiz_score REAL,
    quiz_attempts INT NOT NULL DEFAULT 0,
    exercise_done BOOLEAN NOT NULL DEFAULT false,
    review_stage INT NOT NULL DEFAULT 0,
    next_review_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (learner_id, node_id)
);
"""

# Columns added after the initial schema shipped (safe to run repeatedly).
MIGRATIONS = """
ALTER TABLE syllabus_nodes ADD COLUMN IF NOT EXISTS transcript TEXT;
ALTER TABLE syllabus_nodes ADD COLUMN IF NOT EXISTS key_points JSONB;
ALTER TABLE syllabus_nodes ADD COLUMN IF NOT EXISTS written TEXT;
ALTER TABLE syllabus_nodes ADD COLUMN IF NOT EXISTS diagrams JSONB;
ALTER TABLE courses ADD COLUMN IF NOT EXISTS brief TEXT;
ALTER TABLE learners ADD COLUMN IF NOT EXISTS invite_code TEXT;
ALTER TABLE syllabus_nodes ADD COLUMN IF NOT EXISTS explain_prompt TEXT;
ALTER TABLE syllabus_nodes ADD COLUMN IF NOT EXISTS module_description TEXT;
ALTER TABLE courses ADD COLUMN IF NOT EXISTS category TEXT NOT NULL DEFAULT '';
-- Operator review of the tutor: flag an evaluation that got it wrong. Reading
-- learner work is how we tune the evaluator, so the flags are the labelled set.
ALTER TABLE submissions ADD COLUMN IF NOT EXISTS flagged BOOLEAN NOT NULL DEFAULT false;
-- The transversal project belongs to the LEARNER, not to each course (docs/09):
-- one real business/brand/organization/team that every exercise builds on, so
-- work accumulated across courses can compile into one goal document. Also what
-- lets the evaluator judge Aplicación against declared context instead of
-- guessing it (the doc/06 gap).
-- Within-course module prerequisites (docs/09 item 2): which EARLIER modules a
-- module genuinely depends on, extracted conservatively per course. Denormalized
-- per node like module_title/module_description. What makes skipping modules
-- safe: a route may only include a module if its prereqs are in the route too.
ALTER TABLE syllabus_nodes ADD COLUMN IF NOT EXISTS module_prereqs JSONB;
ALTER TABLE learners ADD COLUMN IF NOT EXISTS project_name TEXT NOT NULL DEFAULT '';
ALTER TABLE learners ADD COLUMN IF NOT EXISTS project_desc TEXT NOT NULL DEFAULT '';
ALTER TABLE learners ADD COLUMN IF NOT EXISTS goal TEXT NOT NULL DEFAULT '';
ALTER TABLE submissions ADD COLUMN IF NOT EXISTS flag_note TEXT;
-- Sessions expire server-side (2026-08-12 audit): the cookie's max-age was the
-- ONLY expiry, so a captured token stayed valid forever. Existing rows keep the
-- 90 days they were issued with, counted from when they were created.
ALTER TABLE learner_sessions ADD COLUMN IF NOT EXISTS expires_at TIMESTAMPTZ;
UPDATE learner_sessions SET expires_at = created_at + interval '90 days'
 WHERE expires_at IS NULL;
-- Locked-out learners. Closing the account-takeover hole means an existing
-- learner without a session cannot let themselves back in until email delivery
-- exists; this is the queue that keeps that from being a silent dead end. Also
-- catches the worse case: RESEND configured but FAILING, where the learner is
-- told an email is coming and none ever arrives.
-- What the learner was actually answering, captured at submit time.
-- Lesson content is COMPILED OUTPUT and will be regenerated (better scripts,
-- clearer exercises). Without this, improving a lesson silently reattaches old
-- submissions to a question nobody was ever asked, and the portfolio document —
-- the credibility artifact this whole product sells — quotes work against the
-- wrong prompt. Snapshotting is what makes content safely mutable.
ALTER TABLE submissions ADD COLUMN IF NOT EXISTS prompt_snapshot JSONB;
CREATE TABLE IF NOT EXISTS access_requests (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL,
    learner_id INT REFERENCES learners(id),
    reason TEXT NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    resolved_at TIMESTAMPTZ
);
CREATE TABLE IF NOT EXISTS case_studies (
    id SERIAL PRIMARY KEY,
    learner_id INT NOT NULL REFERENCES learners(id),
    course_id INT NOT NULL REFERENCES courses(id),
    title TEXT NOT NULL DEFAULT '',
    content_md TEXT NOT NULL,
    share_token TEXT UNIQUE,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (learner_id, course_id)
);
CREATE TABLE IF NOT EXISTS project_docs (
    id SERIAL PRIMARY KEY,
    learner_id INT NOT NULL REFERENCES learners(id),
    course_id INT NOT NULL REFERENCES courses(id),
    title TEXT NOT NULL DEFAULT '',
    content_md TEXT NOT NULL,
    share_token TEXT UNIQUE,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (learner_id, course_id)
);
-- The GOAL document (docs/09): one deliverable aimed at one job target,
-- compiled from the learner's best work across every course in the route.
-- Per-course project_docs stay as milestones; this is the endgame artifact.
CREATE TABLE IF NOT EXISTS goal_docs (
    id SERIAL PRIMARY KEY,
    learner_id INT NOT NULL REFERENCES learners(id),
    job_target_id INT NOT NULL REFERENCES job_targets(id),
    title TEXT NOT NULL DEFAULT '',
    content_md TEXT NOT NULL,
    share_token TEXT UNIQUE,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (learner_id, job_target_id)
);
-- CV intake (docs/10). The CV is a CLAIM about what someone already knows, and
-- this platform is built on not trusting claims. So it lives in its own table
-- and produces PROPOSALS; it never writes progress.
-- cv_text has already been through writer.strip_contacts(): no emails, no phone
-- numbers. backup_db.py exports every table offsite, so that matters here.
CREATE TABLE IF NOT EXISTS cv_profiles (
    id SERIAL PRIMARY KEY,
    learner_id INT NOT NULL REFERENCES learners(id),
    cv_text TEXT NOT NULL,
    analysis JSONB NOT NULL,
    active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
-- One row per module the learner skips. DELIBERATELY NOT `progress`: completed_at
-- has to keep meaning "they did the lesson", or the streak, the SM-2 ladder and
-- the Module-1 completion gate all quietly become fiction (docs/06 already lists
-- gates it cannot compute).
--   declarado  — they said they know it. Cosmetic: shortens the route, opens the
--                reto early, changes NO access. An injected CV can reach exactly
--                this and no further.
--   acreditado — they passed the module's reto (a novel case, deliberately not
--                covered in the lessons). Counts as the module's outcome met.
-- What strangers write on the public lesson (docs/11). Not a submission: no
-- learner owns it, it earns nothing, and it never reaches a portfolio. It is
-- kept because it is the only record of how someone explains a concept before
-- they have any stake in the product, and this project's documented shortage is
-- evidence, not features.
CREATE TABLE IF NOT EXISTS demo_attempts (
    id SERIAL PRIMARY KEY,
    node_id INT NOT NULL REFERENCES syllabus_nodes(id),
    content TEXT NOT NULL,
    evaluation JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS module_exemptions (
    id SERIAL PRIMARY KEY,
    learner_id INT NOT NULL REFERENCES learners(id),
    course_id INT NOT NULL REFERENCES courses(id),
    module_no INT NOT NULL,
    status TEXT NOT NULL DEFAULT 'declarado',   -- declarado | acreditado
    source TEXT NOT NULL DEFAULT 'cv',          -- cv | manual | reto
    claim TEXT NOT NULL DEFAULT '',
    capstone_submission_id INT REFERENCES submissions(id),
    score INT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (learner_id, course_id, module_no)
);
"""

# Spaced-repetition intervals (days) by review stage. SM-2-lite.
REVIEW_INTERVALS = [1, 3, 7, 16, 35]


def _dsn() -> str:
    url = os.environ["DATABASE_URL"]
    # Railway hands out postgres:// URLs; psycopg wants postgresql://
    return url.replace("postgres://", "postgresql://", 1)


def connect() -> psycopg.Connection:
    # Force UTF-8 on the wire so text round-trips identically regardless of the
    # host locale (Windows consoles otherwise negotiate an inconsistent encoding).
    return psycopg.connect(_dsn(), row_factory=dict_row, client_encoding="utf-8")


def enabled() -> bool:
    return bool(os.environ.get("DATABASE_URL"))


def init_db() -> None:
    with connect() as conn:
        conn.execute(SCHEMA)
        conn.execute(MIGRATIONS)


def topic_history(conn: psycopg.Connection, channel: str) -> list[str]:
    """Every topic title ever recorded for a channel — fed to the LLM as the
    do-not-repeat list."""
    rows = conn.execute(
        "SELECT title FROM topics WHERE channel = %s ORDER BY id", (channel,)
    ).fetchall()
    return [r["title"] for r in rows]


def unused_topics(conn: psycopg.Connection, channel: str) -> list[dict]:
    return conn.execute(
        "SELECT * FROM topics WHERE channel = %s AND status = 'idea' ORDER BY id",
        (channel,),
    ).fetchall()


def add_topics(conn: psycopg.Connection, channel: str, ideas: list[dict]) -> int:
    added = 0
    for idea in ideas:
        cur = conn.execute(
            "INSERT INTO topics (channel, slug, title, angle) VALUES (%s, %s, %s, %s) "
            "ON CONFLICT (channel, slug) DO NOTHING",
            (channel, idea["slug"], idea["title"], idea.get("angle", "")),
        )
        added += cur.rowcount
    return added


def mark_topic_used(conn: psycopg.Connection, topic_id: int) -> None:
    conn.execute(
        "UPDATE topics SET status = 'used', used_at = now() WHERE id = %s",
        (topic_id,),
    )


def ensure_course(conn: psycopg.Connection, slug: str, title: str, description: str,
                  brief: str = "", category: str = "") -> dict:
    """Upsert a course from its TOML profile. The TOML is the single source of
    truth: title, learner-facing description (niche), internal brief and catalog
    category are synced on every factory command — editing the TOML is all it takes."""
    row = conn.execute("SELECT * FROM courses WHERE slug = %s", (slug,)).fetchone()
    if row:
        current = (row["title"], row["description"], row.get("brief") or "", row.get("category") or "")
        if current != (title, description, brief, category):
            row = conn.execute(
                "UPDATE courses SET title = %s, description = %s, brief = %s, category = %s "
                "WHERE slug = %s RETURNING *",
                (title, description, brief, category, slug),
            ).fetchone()
        return row
    return conn.execute(
        "INSERT INTO courses (slug, title, description, brief, category) "
        "VALUES (%s, %s, %s, %s, %s) RETURNING *",
        (slug, title, description, brief, category),
    ).fetchone()


def course_nodes(conn: psycopg.Connection, course_id: int, status: str | None = None) -> list[dict]:
    if status:
        return conn.execute(
            "SELECT * FROM syllabus_nodes WHERE course_id = %s AND status = %s ORDER BY position",
            (course_id, status),
        ).fetchall()
    return conn.execute(
        "SELECT * FROM syllabus_nodes WHERE course_id = %s ORDER BY position", (course_id,)
    ).fetchall()


def job_catalog(conn: psycopg.Connection) -> list[dict]:
    """The module contracts a job posting is matched against (docs/08).

    One row per module, not per lesson: routes can only ever be a per-course
    prefix (`_accessible_ids` gates sequentially inside a course), so modules are
    the real unit of choice. Only courses with rendered video are offered —
    routing someone into a course they cannot watch is a broken promise.
    """
    import json as _json
    rows = conn.execute(
        "SELECT c.slug, c.title AS course_title, n.module_no, "
        "       MIN(n.module_title) AS module_title, "
        "       MIN(n.module_description) AS module_description, "
        "       MIN(n.module_prereqs::text) AS module_prereqs, "
        "       COUNT(*) AS lessons, "
        "       COUNT(n.video_file) AS rendered "
        "FROM syllabus_nodes n JOIN courses c ON c.id = n.course_id "
        "GROUP BY c.id, c.slug, c.title, n.module_no "
        "ORDER BY c.id, n.module_no"
    ).fetchall()
    catalog: dict[str, dict] = {}
    for r in rows:
        if not r["rendered"]:
            continue
        try:
            prereqs = _json.loads(r["module_prereqs"]) if r["module_prereqs"] else None
        except (ValueError, TypeError):
            prereqs = None
        course = catalog.setdefault(
            r["slug"], {"slug": r["slug"], "title": r["course_title"], "modules": []})
        course["modules"].append({
            "module_no": r["module_no"],
            "title": r["module_title"] or "",
            "description": r["module_description"] or "",
            # None = never extracted → callers must fall back to strict sequence
            # (all earlier modules), which is exactly today's behavior.
            "prereqs": prereqs,
            "lessons": r["lessons"],
        })
    return [c for c in catalog.values() if c["modules"]]


def add_node(conn: psycopg.Connection, course_id: int, node: dict) -> None:
    conn.execute(
        "INSERT INTO syllabus_nodes (course_id, module_no, module_title, module_description, "
        "position, slug, title, objectives, angle) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) "
        "ON CONFLICT (course_id, slug) DO NOTHING",
        (course_id, node["module_no"], node["module_title"], node.get("module_description", ""),
         node["position"], node["slug"], node["title"], node["objectives"], node["angle"]),
    )


# Column names are interpolated into SQL below (they cannot be bound as
# parameters), so they must never come from anywhere but this list. Every caller
# today is the operator-run factory passing hardcoded keys, but an interpolated
# identifier one refactor away from a request body is how injection arrives.
_NODE_COLUMNS = frozenset({
    "module_no", "module_title", "module_description", "module_prereqs",
    "position", "slug", "title", "objectives", "angle", "status",
    "script", "transcript", "key_points", "written", "diagrams",
    "explain_prompt", "quiz", "video_file",
})
_NODE_JSON_COLUMNS = ("quiz", "key_points", "diagrams", "module_prereqs")


def update_node(conn: psycopg.Connection, node_id: int, **fields) -> None:
    import json as _json
    unknown = set(fields) - _NODE_COLUMNS
    if unknown:
        raise ValueError(f"update_node: unknown column(s) {sorted(unknown)}")
    if not fields:
        return
    sets, values = [], []
    for key, value in fields.items():
        sets.append(f"{key} = %s")
        values.append(_json.dumps(value, ensure_ascii=False)
                      if key in _NODE_JSON_COLUMNS else value)
    values.append(node_id)
    conn.execute(f"UPDATE syllabus_nodes SET {', '.join(sets)} WHERE id = %s", values)


# -------------------- learners / auth --------------------

def get_or_create_learner(conn: psycopg.Connection, email: str, name: str = "") -> dict:
    email = email.strip().lower()
    row = conn.execute("SELECT * FROM learners WHERE email = %s", (email,)).fetchone()
    if row:
        return row
    return conn.execute(
        "INSERT INTO learners (email, name) VALUES (%s, %s) RETURNING *", (email, name)
    ).fetchone()


def valid_invite(conn: psycopg.Connection, code: str) -> dict | None:
    if not code:
        return None
    return conn.execute(
        "SELECT * FROM invite_codes WHERE code = %s AND active = true AND uses < max_uses",
        (code.strip(),),
    ).fetchone()


def consume_invite(conn: psycopg.Connection, code: str) -> None:
    conn.execute("UPDATE invite_codes SET uses = uses + 1 WHERE code = %s", (code.strip(),))


def list_invites(conn: psycopg.Connection) -> list[dict]:
    """Every invite code with usage and who redeemed it — the operator's one place
    to grab a link to share. Usable codes first (active, with uses left), then
    exhausted/deactivated ones; newest within each group."""
    return conn.execute(
        "SELECT ic.code, ic.label, ic.uses, ic.max_uses, ic.active, ic.created_at, "
        "       COALESCE(array_agg(l.name ORDER BY l.created_at) "
        "                FILTER (WHERE l.id IS NOT NULL), '{}') AS learners "
        "FROM invite_codes ic LEFT JOIN learners l ON l.invite_code = ic.code "
        "GROUP BY ic.code, ic.label, ic.uses, ic.max_uses, ic.active, ic.created_at "
        "ORDER BY (ic.active AND ic.uses < ic.max_uses) DESC, ic.created_at DESC"
    ).fetchall()


def set_invite_active(conn: psycopg.Connection, code: str, active: bool) -> None:
    conn.execute("UPDATE invite_codes SET active = %s WHERE code = %s", (active, code))


def create_invite(conn: psycopg.Connection, code: str, label: str, max_uses: int) -> None:
    conn.execute(
        "INSERT INTO invite_codes (code, label, max_uses) VALUES (%s, %s, %s) "
        "ON CONFLICT (code) DO NOTHING",
        (code, label, max_uses),
    )


def create_login_token(conn: psycopg.Connection, learner_id: int, token: str, ttl_minutes: int = 30) -> None:
    conn.execute(
        "INSERT INTO login_tokens (token, learner_id, expires_at) "
        "VALUES (%s, %s, now() + make_interval(mins => %s))",
        (token, learner_id, ttl_minutes),
    )


def consume_login_token(conn: psycopg.Connection, token: str) -> int | None:
    row = conn.execute(
        "SELECT learner_id FROM login_tokens WHERE token = %s AND used = false "
        "AND expires_at > now()", (token,),
    ).fetchone()
    if not row:
        return None
    conn.execute("UPDATE login_tokens SET used = true WHERE token = %s", (token,))
    return row["learner_id"]


SESSION_DAYS = 90


def create_session(conn: psycopg.Connection, learner_id: int, token: str) -> None:
    conn.execute(
        "INSERT INTO learner_sessions (token, learner_id, expires_at) "
        "VALUES (%s, %s, now() + make_interval(days => %s))",
        (token, learner_id, SESSION_DAYS),
    )


def learner_for_session(conn: psycopg.Connection, token: str) -> dict | None:
    """Resolve a session cookie to its learner, honouring expiry.

    The cookie always carried a 90-day max-age, but the SERVER used to accept
    any token that existed — forever, and a browser is not the only thing that
    can hold a cookie. Expiry now lives in the database, which is the only place
    a client cannot edit it. Rows predating the column were backfilled to
    created_at + 90 days by MIGRATIONS.
    """
    if not token:
        return None
    return conn.execute(
        "SELECT l.* FROM learners l JOIN learner_sessions s ON s.learner_id = l.id "
        "WHERE s.token = %s AND (s.expires_at IS NULL OR s.expires_at > now())",
        (token,),
    ).fetchone()


def delete_session(conn: psycopg.Connection, token: str) -> None:
    """Revoke one session server-side. Logout used to only drop the cookie,
    which left the token valid for anyone who had already captured it."""
    if token:
        conn.execute("DELETE FROM learner_sessions WHERE token = %s", (token,))


def purge_expired_auth(conn: psycopg.Connection) -> dict[str, int]:
    """Drop expired sessions and spent/expired magic links (docs/06 housekeeping).
    Cheap, idempotent, and safe to run on boot."""
    sessions = conn.execute(
        "DELETE FROM learner_sessions WHERE expires_at IS NOT NULL AND expires_at <= now()"
    ).rowcount
    tokens = conn.execute(
        "DELETE FROM login_tokens WHERE used = true OR expires_at <= now()"
    ).rowcount
    return {"sessions": sessions, "login_tokens": tokens}


# -------------------- comprehension: capstones & submissions --------------------

def add_capstone(conn: psycopg.Connection, course_id: int, module_no: int, spec: dict) -> None:
    import json as _json
    conn.execute(
        "INSERT INTO module_capstones (course_id, module_no, title, scenario, deliverable, rubric) "
        "VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (course_id, module_no) DO NOTHING",
        (course_id, module_no, spec.get("title", ""), spec["scenario"],
         spec["deliverable"], _json.dumps(spec.get("rubric", []), ensure_ascii=False)),
    )


def course_capstones(conn: psycopg.Connection, course_id: int) -> list[dict]:
    return conn.execute(
        "SELECT * FROM module_capstones WHERE course_id = %s ORDER BY module_no", (course_id,)
    ).fetchall()


def get_capstone(conn: psycopg.Connection, capstone_id: int) -> dict | None:
    return conn.execute(
        "SELECT * FROM module_capstones WHERE id = %s", (capstone_id,)
    ).fetchone()


def add_submission(
    conn: psycopg.Connection,
    learner_id: int,
    kind: str,
    content: str,
    evaluation: dict,
    node_id: int | None = None,
    capstone_id: int | None = None,
    prompt: dict | None = None,
) -> dict:
    """Store one evaluated piece of work, WITH the prompt it answered.

    `prompt` is the question/instruction as the learner saw it. It is not
    redundant with node_id: the node's content is regenerable, this is not.
    """
    import json as _json
    return conn.execute(
        "INSERT INTO submissions (learner_id, kind, node_id, capstone_id, content, "
        "evaluation, prompt_snapshot) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *",
        (learner_id, kind, node_id, capstone_id, content,
         _json.dumps(evaluation, ensure_ascii=False),
         _json.dumps(prompt, ensure_ascii=False) if prompt else None),
    ).fetchone()


def latest_submissions(conn: psycopg.Connection, learner_id: int) -> list[dict]:
    """Newest submission per (kind, node/capstone) — the learner's current state
    (what they last wrote). Use best_submissions for anything that shows a score."""
    return conn.execute(
        "SELECT DISTINCT ON (kind, node_id, capstone_id) * FROM submissions "
        "WHERE learner_id = %s ORDER BY kind, node_id, capstone_id, id DESC",
        (learner_id,),
    ).fetchall()


def best_submissions(conn: psycopg.Connection, learner_id: int) -> list[dict]:
    """Highest-scoring submission per (kind, node/capstone), newest as tiebreak.
    Retrying must never lower what a learner has earned, so every surface that
    displays a score — or compiles their work — reads from here."""
    return conn.execute(
        "SELECT DISTINCT ON (kind, node_id, capstone_id) * FROM submissions "
        "WHERE learner_id = %s ORDER BY kind, node_id, capstone_id, "
        "COALESCE((evaluation->>'final_score')::int, (evaluation->>'score')::int, 0) DESC, "
        "id DESC",
        (learner_id,),
    ).fetchall()


def best_score_for(conn: psycopg.Connection, learner_id: int, kind: str,
                   node_id: int | None = None, capstone_id: int | None = None) -> int | None:
    """Highest score this learner has ever earned on ONE work item.

    The stored best already survives a weak retry (`best_submissions`), but the
    learner never saw it: the evaluation screen showed only the attempt they had
    just made. A real learner watched a 30 count up on work that had scored 79
    and stopped using the product. The number is only reassuring if it is on
    screen, so the submit response now carries it.
    """
    row = conn.execute(
        "SELECT max(COALESCE((evaluation->>'final_score')::int, "
        "                    (evaluation->>'score')::int)) AS best "
        "FROM submissions WHERE learner_id = %s AND kind = %s "
        "AND node_id IS NOT DISTINCT FROM %s AND capstone_id IS NOT DISTINCT FROM %s",
        (learner_id, kind, node_id, capstone_id),
    ).fetchone()
    return row["best"] if row else None


def learner_portfolio(conn: psycopg.Connection, learner_id: int) -> list[dict]:
    """All submissions with lesson/capstone titles and their course, newest first
    (the Portafolio tab groups these by course)."""
    return conn.execute(
        "SELECT s.*, n.title AS node_title, cap.title AS capstone_title, cap.module_no, "
        "COALESCE(cn.slug, cc.slug) AS course_slug, "
        "COALESCE(cn.title, cc.title) AS course_title "
        "FROM submissions s "
        "LEFT JOIN syllabus_nodes n ON n.id = s.node_id "
        "LEFT JOIN courses cn ON cn.id = n.course_id "
        "LEFT JOIN module_capstones cap ON cap.id = s.capstone_id "
        "LEFT JOIN courses cc ON cc.id = cap.course_id "
        "WHERE s.learner_id = %s ORDER BY s.id DESC",
        (learner_id,),
    ).fetchall()


# -------------------- operator: reading learner work --------------------

def learner_work(conn: psycopg.Connection, learner_id: int) -> list[dict]:
    """Everything one learner has written, oldest first, with the lesson/capstone
    and course it belongs to. Chronological on purpose: the operator is reading a
    journey, and retries appear in sequence so progress is visible."""
    return conn.execute(
        "SELECT s.*, n.title AS node_title, n.position, n.objectives, "
        "cap.title AS capstone_title, cap.module_no, "
        "COALESCE(cn.title, cc.title) AS course_title "
        "FROM submissions s "
        "LEFT JOIN syllabus_nodes n ON n.id = s.node_id "
        "LEFT JOIN courses cn ON cn.id = n.course_id "
        "LEFT JOIN module_capstones cap ON cap.id = s.capstone_id "
        "LEFT JOIN courses cc ON cc.id = cap.course_id "
        "WHERE s.learner_id = %s ORDER BY s.id",
        (learner_id,),
    ).fetchall()


def learner_course_progress(conn: psycopg.Connection, learner_id: int) -> list[dict]:
    return conn.execute(
        "SELECT c.title AS course_title, c.slug, "
        "count(*) FILTER (WHERE p.completed_at IS NOT NULL) AS done, "
        "(SELECT count(*) FROM syllabus_nodes sn WHERE sn.course_id = c.id) AS total, "
        "max(p.updated_at) AS last_activity "
        "FROM progress p JOIN syllabus_nodes n ON n.id = p.node_id "
        "JOIN courses c ON c.id = n.course_id "
        "WHERE p.learner_id = %s GROUP BY c.id, c.title, c.slug "
        "ORDER BY last_activity DESC",
        (learner_id,),
    ).fetchall()


def set_submission_flag(conn: psycopg.Connection, submission_id: int,
                        flagged: bool, note: str) -> dict | None:
    return conn.execute(
        "UPDATE submissions SET flagged = %s, flag_note = %s WHERE id = %s "
        "RETURNING id, flagged, flag_note",
        (flagged, note or None, submission_id),
    ).fetchone()


# -------------------- public waitlist --------------------

def add_waitlist(conn: psycopg.Connection, name: str, email: str, motivo: str) -> None:
    conn.execute(
        "INSERT INTO waitlist (name, email, motivo) VALUES (%s, %s, %s) "
        "ON CONFLICT (email) DO NOTHING",
        (name, email.strip().lower(), motivo),
    )


def list_waitlist(conn: psycopg.Connection) -> list[dict]:
    return conn.execute(
        "SELECT * FROM waitlist ORDER BY (status = 'new') DESC, id DESC"
    ).fetchall()


def save_job_target(conn: psycopg.Connection, posting_text: str, analysis: dict,
                    share_token: str, learner_id: int | None = None) -> dict:
    """Store a job-posting analysis (docs/08-job-target.md).

    `learner_id` is None for the public, pre-login analysis. Those rows are the
    demand signal: what people are actually trying to get hired for.
    """
    import json as _json
    return conn.execute(
        "INSERT INTO job_targets (learner_id, posting_text, role_title, company, "
        "analysis, share_token) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *",
        (learner_id, posting_text, (analysis.get("role_title") or "")[:200],
         (analysis.get("company") or "")[:200],
         # ensure_ascii=False like every other JSONB write here — this codebase
         # has a history with mangled accents.
         _json.dumps(analysis, ensure_ascii=False), share_token),
    ).fetchone()


def claim_job_target(conn: psycopg.Connection, share_token: str, learner_id: int) -> dict | None:
    """Attach an anonymous analysis to a learner once they sign up, and make it
    their active target. This is what closes the loop from the public paste box
    to the logged-in route — without it the analysis that convinced them to join
    is orphaned."""
    row = conn.execute(
        "SELECT * FROM job_targets WHERE share_token = %s", (share_token,)
    ).fetchone()
    if not row or (row["learner_id"] and row["learner_id"] != learner_id):
        return None
    conn.execute("UPDATE job_targets SET active = false WHERE learner_id = %s",
                 (learner_id,))
    return conn.execute(
        "UPDATE job_targets SET learner_id = %s, active = true WHERE id = %s "
        "RETURNING *", (learner_id, row["id"]),
    ).fetchone()


def job_target_by_token(conn: psycopg.Connection, share_token: str) -> dict | None:
    """Public lookup for the shareable route page. The token is the capability —
    there is no other guard, so it must stay unguessable."""
    return conn.execute(
        "SELECT j.*, l.name AS learner_name FROM job_targets j "
        "LEFT JOIN learners l ON l.id = j.learner_id WHERE j.share_token = %s",
        (share_token,),
    ).fetchone()


def learner_job_targets(conn: psycopg.Connection, learner_id: int) -> list[dict]:
    """Every goal this learner has analysed, active first then newest.

    Switching goals is non-destructive by design: `active` is a flag, `progress`
    is keyed per lesson (so completed work counts toward ANY route containing
    it), and each target keeps its own goal document. History exists so a
    learner can go back to a goal they set aside."""
    return conn.execute(
        "SELECT j.*, (gd.id IS NOT NULL) AS has_doc "
        "FROM job_targets j "
        "LEFT JOIN goal_docs gd ON gd.job_target_id = j.id AND gd.learner_id = j.learner_id "
        "WHERE j.learner_id = %s ORDER BY j.active DESC, j.created_at DESC",
        (learner_id,),
    ).fetchall()


def active_job_target(conn: psycopg.Connection, learner_id: int) -> dict | None:
    return conn.execute(
        "SELECT * FROM job_targets WHERE learner_id = %s AND active "
        "ORDER BY id DESC LIMIT 1", (learner_id,),
    ).fetchone()


def record_demo_attempt(conn: psycopg.Connection, node_id: int, content: str,
                        evaluation: dict) -> None:
    """Store one public-lesson answer (docs/11). Deliberately NOT a submission:
    submissions belong to a learner, count toward a portfolio and can never go
    down. This is anonymous, earns nothing, and exists only as evidence."""
    import json as _json
    conn.execute(
        "INSERT INTO demo_attempts (node_id, content, evaluation) VALUES (%s, %s, %s)",
        (node_id, content[:8000], _json.dumps(evaluation or {}, ensure_ascii=False)),
    )


def save_cv_profile(conn: psycopg.Connection, learner_id: int, cv_text: str,
                    analysis: dict) -> dict:
    """Store a CV reading (docs/10). Only one profile is active at a time; older
    ones stay for history, the same way a superseded job target does.

    `cv_text` must ALREADY be through `writer.strip_contacts` — this is the last
    place a phone number could enter the database, and backup_db.py exports every
    table offsite.
    """
    import json as _json
    conn.execute("UPDATE cv_profiles SET active = false WHERE learner_id = %s",
                 (learner_id,))
    return conn.execute(
        "INSERT INTO cv_profiles (learner_id, cv_text, analysis, active) "
        "VALUES (%s, %s, %s, true) RETURNING *",
        # ensure_ascii=False like every other JSONB write here.
        (learner_id, cv_text, _json.dumps(analysis, ensure_ascii=False)),
    ).fetchone()


def active_cv_profile(conn: psycopg.Connection, learner_id: int) -> dict | None:
    return conn.execute(
        "SELECT * FROM cv_profiles WHERE learner_id = %s AND active "
        "ORDER BY id DESC LIMIT 1", (learner_id,)).fetchone()


def delete_cv_profiles(conn: psycopg.Connection, learner_id: int) -> int:
    """Forget the CV entirely, including history. The declared exemptions it
    produced go with it (see `clear_declared_exemptions`); CREDITED ones do not —
    those were earned by passing a reto and nothing a learner earned may ever go
    down (docs/07)."""
    return conn.execute(
        "DELETE FROM cv_profiles WHERE learner_id = %s", (learner_id,)).rowcount


def set_module_exemption(conn: psycopg.Connection, learner_id: int, course_id: int,
                         module_no: int, claim: str = "", source: str = "cv") -> dict:
    """Record that the learner says they already know this module.

    Status starts at 'declarado' and NEVER regresses: re-declaring a module that
    is already 'acreditado' leaves the credit alone.
    """
    return conn.execute(
        "INSERT INTO module_exemptions (learner_id, course_id, module_no, claim, source) "
        "VALUES (%s, %s, %s, %s, %s) "
        "ON CONFLICT (learner_id, course_id, module_no) DO UPDATE "
        "SET claim = EXCLUDED.claim, source = EXCLUDED.source, updated_at = now() "
        "RETURNING *",
        (learner_id, course_id, module_no, claim, source),
    ).fetchone()


def credit_module_exemption(conn: psycopg.Connection, learner_id: int, course_id: int,
                            module_no: int, submission_id: int, score: int) -> dict:
    """Promote an exemption to 'acreditado': they passed the module's reto.

    `GREATEST` on the score for the same reason every other number in this schema
    keeps its best value — a weaker later attempt must never lower what they
    already proved.
    """
    return conn.execute(
        "INSERT INTO module_exemptions "
        "  (learner_id, course_id, module_no, status, source, capstone_submission_id, score) "
        "VALUES (%s, %s, %s, 'acreditado', 'reto', %s, %s) "
        "ON CONFLICT (learner_id, course_id, module_no) DO UPDATE "
        "SET status = 'acreditado', "
        "    capstone_submission_id = CASE WHEN EXCLUDED.score > COALESCE(module_exemptions.score, -1) "
        "                                  THEN EXCLUDED.capstone_submission_id "
        "                                  ELSE module_exemptions.capstone_submission_id END, "
        "    score = GREATEST(COALESCE(module_exemptions.score, 0), EXCLUDED.score), "
        "    updated_at = now() "
        "RETURNING *",
        (learner_id, course_id, module_no, submission_id, score),
    ).fetchone()


def clear_module_exemption(conn: psycopg.Connection, learner_id: int, course_id: int,
                           module_no: int) -> bool:
    """Undo a DECLARED skip — "enséñamelo igual". Returns whether a row went.

    A credited exemption is deliberately untouchable here: it is not a preference,
    it is a passed reto, and it stays on the record with its score.
    """
    return conn.execute(
        "DELETE FROM module_exemptions WHERE learner_id = %s AND course_id = %s "
        "AND module_no = %s AND status = 'declarado'",
        (learner_id, course_id, module_no)).rowcount > 0


def clear_declared_exemptions(conn: psycopg.Connection, learner_id: int) -> int:
    """Drop every declared skip (used when the CV that proposed them is deleted).
    Credited ones survive — see `delete_cv_profiles`."""
    return conn.execute(
        "DELETE FROM module_exemptions WHERE learner_id = %s AND status = 'declarado'",
        (learner_id,)).rowcount


def learner_exemptions(conn: psycopg.Connection, learner_id: int) -> list[dict]:
    """Every exemption with its course slug, for the route and temario surfaces."""
    return conn.execute(
        "SELECT e.*, c.slug AS course_slug, c.title AS course_title "
        "FROM module_exemptions e JOIN courses c ON c.id = e.course_id "
        "WHERE e.learner_id = %s ORDER BY c.id, e.module_no",
        (learner_id,)).fetchall()


def exempt_modules_for(conn: psycopg.Connection, learner_id: int,
                       course_id: int) -> set[int]:
    """The module numbers this learner has skipped in one course, declared or
    credited. Callers that need to tell them apart use `learner_exemptions`."""
    rows = conn.execute(
        "SELECT module_no FROM module_exemptions WHERE learner_id = %s AND course_id = %s",
        (learner_id, course_id)).fetchall()
    return {r["module_no"] for r in rows}


def record_access_request(conn: psycopg.Connection, email: str,
                          learner_id: int | None, reason: str) -> None:
    """Queue a locked-out learner for the operator. Idempotent per email: one
    open row per person, so someone retrying five times is one line to act on,
    not five."""
    open_row = conn.execute(
        "SELECT id FROM access_requests WHERE email = %s AND resolved_at IS NULL",
        (email,)).fetchone()
    if open_row:
        conn.execute("UPDATE access_requests SET created_at = now(), reason = %s "
                     "WHERE id = %s", (reason[:200], open_row["id"]))
        return
    conn.execute(
        "INSERT INTO access_requests (email, learner_id, reason) VALUES (%s, %s, %s)",
        (email, learner_id, reason[:200]))


def open_access_requests(conn: psycopg.Connection) -> list[dict]:
    """Everyone waiting to be let back in, oldest first — they have been stuck
    the longest."""
    return conn.execute(
        "SELECT ar.id, ar.email, ar.learner_id, ar.reason, ar.created_at, "
        "       l.name AS learner_name "
        "FROM access_requests ar LEFT JOIN learners l ON l.id = ar.learner_id "
        "WHERE ar.resolved_at IS NULL ORDER BY ar.created_at").fetchall()


def resolve_access_request(conn: psycopg.Connection, email: str) -> None:
    """Clear the queue entry once the learner is back in. Called when a magic
    link is minted for them and when a session is created, so the list empties
    itself rather than needing to be tidied."""
    conn.execute(
        "UPDATE access_requests SET resolved_at = now() "
        "WHERE email = %s AND resolved_at IS NULL", (email,))


def demand_ledger(conn: psycopg.Connection, limit: int = 500) -> dict:
    """What people asked to become, what we served, and what we did not have.

    Every public analysis already computes an honest gap list (docs/08) and then
    buries it in `job_targets.analysis`. Nobody has ever read one: this helper's
    predecessor, `list_job_targets`, carried a docstring saying the gap lists
    "are what should decide which course gets built next" and was called from
    nowhere. So the demand signal the whole supply/demand-clock design rests on
    has been accumulating in JSONB, unread, since the feature shipped.

    Two halves, deliberately:

      gaps    — the DEMAND side. What roles ask for that we cannot teach.
                Recurrence is the signal; a gap seen once is noise (docs/08:
                build course N when the SAME gap recurs).
      modules — the SUPPLY side, and the more uncomfortable one. Which modules
                have ever been selected for anyone's goal. At the time of
                writing, 56 of 70 never had. A catalog running that far ahead of
                demand does not need more courses; it needs someone to route to
                the ones it has.

    Aggregation happens in Python rather than SQL because route entries come in
    two shapes (v2 module SETS, v1 `through_module` prefixes) and that expansion
    already lives in Python — see `_route_modules_for`. One place, one rule.
    """
    rows = conn.execute(
        "SELECT id, learner_id, role_title, company, analysis, created_at "
        "FROM job_targets ORDER BY id DESC LIMIT %s", (limit,),
    ).fetchall()

    def norm(s: str) -> str:
        return " ".join(str(s or "").strip().lower().split())

    gaps: dict[str, dict] = {}
    routed: dict[tuple[str, int], int] = {}
    coverages: list[int] = []
    anonymous = 0

    for r in rows:
        a = r["analysis"] or {}
        if a.get("coverage") is not None:
            coverages.append(int(a["coverage"]))
        if r["learner_id"] is None:
            anonymous += 1
        for g in (a.get("gaps") or []):
            key = norm(g.get("name"))
            if not key:
                continue
            e = gaps.setdefault(key, {
                "gap": (g.get("name") or "").strip(), "count": 0,
                "severities": [], "roles": [], "last_seen": r["created_at"],
            })
            e["count"] += 1
            if g.get("severity"):
                e["severities"].append(g["severity"])
            if r["role_title"] and r["role_title"] not in e["roles"]:
                e["roles"].append(r["role_title"])
            if r["created_at"] > e["last_seen"]:
                e["last_seen"] = r["created_at"]
        for entry in (a.get("ruta") or []):
            slug = entry.get("course_slug")
            if not slug:
                continue
            mods = entry.get("modules")
            if not (isinstance(mods, list) and mods):
                try:
                    depth = int(entry.get("through_module", 1))
                except (TypeError, ValueError):
                    depth = 1
                mods = list(range(1, max(1, depth) + 1))
            for m in mods:
                try:
                    routed[(slug, int(m))] = routed.get((slug, int(m)), 0) + 1
                except (TypeError, ValueError):
                    continue

    catalog = job_catalog(conn)
    modules = []
    for course in catalog:
        for m in course.get("modules", []):
            key = (course["slug"], m["module_no"])
            modules.append({
                "course_slug": course["slug"], "course_title": course.get("title", ""),
                "module_no": m["module_no"], "title": m.get("title", ""),
                "lessons": m.get("lessons", 0), "times_routed": routed.get(key, 0),
            })
    never = [m for m in modules if not m["times_routed"]]
    coverages.sort()
    median = coverages[len(coverages) // 2] if coverages else None

    ledger = sorted(gaps.values(), key=lambda g: (-g["count"], g["gap"]))
    for g in ledger:
        sev = g.pop("severities")
        g["severity"] = max(set(sev), key=sev.count) if sev else ""
        g["last_seen"] = g["last_seen"].date().isoformat()

    return {
        "analyses": len(rows),
        "anonymous": anonymous,
        "median_coverage": median,
        "gaps": ledger,
        "modules": sorted(modules, key=lambda m: (-m["times_routed"], m["course_slug"],
                                                  m["module_no"])),
        "modules_total": len(modules),
        "modules_never_routed": len(never),
    }


def list_job_targets(conn: psycopg.Connection, limit: int = 200) -> list[dict]:
    """Operator view: every posting analysed, newest first. The gap lists across
    these rows are what should decide which course gets built next."""
    return conn.execute(
        "SELECT j.*, l.name AS learner_name, l.email AS learner_email "
        "FROM job_targets j LEFT JOIN learners l ON l.id = j.learner_id "
        "ORDER BY j.id DESC LIMIT %s", (limit,),
    ).fetchall()


# -------------------- portfolio case studies (STAR) --------------------

def upsert_case_study(conn: psycopg.Connection, learner_id: int, course_id: int,
                      title: str, content_md: str, share_token: str) -> dict:
    """Create or refresh the learner's case study for a course. The share token
    is kept stable across regenerations so a shared link never breaks."""
    return conn.execute(
        "INSERT INTO case_studies (learner_id, course_id, title, content_md, share_token) "
        "VALUES (%s, %s, %s, %s, %s) "
        "ON CONFLICT (learner_id, course_id) DO UPDATE SET "
        "title = EXCLUDED.title, content_md = EXCLUDED.content_md, updated_at = now() "
        "RETURNING *",
        (learner_id, course_id, title, content_md, share_token),
    ).fetchone()


def get_case_study(conn: psycopg.Connection, learner_id: int, course_id: int) -> dict | None:
    return conn.execute(
        "SELECT * FROM case_studies WHERE learner_id = %s AND course_id = %s",
        (learner_id, course_id),
    ).fetchone()


def case_study_by_token(conn: psycopg.Connection, token: str) -> dict | None:
    if not token:
        return None
    return conn.execute(
        "SELECT cs.*, l.name AS learner_name, c.title AS course_title "
        "FROM case_studies cs JOIN learners l ON l.id = cs.learner_id "
        "JOIN courses c ON c.id = cs.course_id WHERE cs.share_token = %s",
        (token,),
    ).fetchone()


def upsert_project_doc(conn: psycopg.Connection, learner_id: int, course_id: int,
                       title: str, content_md: str, share_token: str) -> dict:
    """Create or refresh the learner's project document (the client-grade
    deliverable compiled from their submissions). Share token stays stable."""
    return conn.execute(
        "INSERT INTO project_docs (learner_id, course_id, title, content_md, share_token) "
        "VALUES (%s, %s, %s, %s, %s) "
        "ON CONFLICT (learner_id, course_id) DO UPDATE SET "
        "title = EXCLUDED.title, content_md = EXCLUDED.content_md, updated_at = now() "
        "RETURNING *",
        (learner_id, course_id, title, content_md, share_token),
    ).fetchone()


def get_project_doc(conn: psycopg.Connection, learner_id: int, course_id: int) -> dict | None:
    return conn.execute(
        "SELECT * FROM project_docs WHERE learner_id = %s AND course_id = %s",
        (learner_id, course_id),
    ).fetchone()


def project_doc_by_token(conn: psycopg.Connection, token: str) -> dict | None:
    if not token:
        return None
    return conn.execute(
        "SELECT pd.*, l.name AS learner_name, c.title AS course_title "
        "FROM project_docs pd JOIN learners l ON l.id = pd.learner_id "
        "JOIN courses c ON c.id = pd.course_id WHERE pd.share_token = %s",
        (token,),
    ).fetchone()


def doc_by_token(conn: psycopg.Connection, token: str) -> dict | None:
    """Any paper document by its share token — course docs and goal docs share
    one public page, so this is the one lookup that page's API needs. `kind`
    tells the caller which credit line to write; `context` is the course title
    or the role the goal doc aims at."""
    row = project_doc_by_token(conn, token)
    if row:
        return {"kind": "course", "title": row["title"], "content_md": row["content_md"],
                "learner_name": row["learner_name"], "context": row["course_title"],
                "updated_at": row["updated_at"]}
    row = conn.execute(
        "SELECT gd.*, l.name AS learner_name, jt.role_title "
        "FROM goal_docs gd JOIN learners l ON l.id = gd.learner_id "
        "JOIN job_targets jt ON jt.id = gd.job_target_id WHERE gd.share_token = %s",
        (token,),
    ).fetchone()
    if row:
        return {"kind": "goal", "title": row["title"], "content_md": row["content_md"],
                "learner_name": row["learner_name"], "context": row["role_title"],
                "updated_at": row["updated_at"]}
    return None


def set_learner_profile(conn: psycopg.Connection, learner_id: int,
                        project_name: str, project_desc: str, goal: str) -> None:
    conn.execute(
        "UPDATE learners SET project_name = %s, project_desc = %s, goal = %s "
        "WHERE id = %s",
        (project_name[:120], project_desc[:500], goal[:200], learner_id),
    )


def get_goal_doc(conn: psycopg.Connection, learner_id: int, job_target_id: int) -> dict | None:
    return conn.execute(
        "SELECT * FROM goal_docs WHERE learner_id = %s AND job_target_id = %s",
        (learner_id, job_target_id),
    ).fetchone()


def upsert_goal_doc(conn: psycopg.Connection, learner_id: int, job_target_id: int,
                    title: str, content_md: str, share_token: str) -> dict:
    """Create or refresh the goal document. Same contract as project docs:
    regenerable as the learner progresses, share token stable forever."""
    return conn.execute(
        "INSERT INTO goal_docs (learner_id, job_target_id, title, content_md, share_token) "
        "VALUES (%s, %s, %s, %s, %s) "
        "ON CONFLICT (learner_id, job_target_id) DO UPDATE SET "
        "title = EXCLUDED.title, content_md = EXCLUDED.content_md, updated_at = now() "
        "RETURNING *",
        (learner_id, job_target_id, title, content_md, share_token),
    ).fetchone()


# -------------------- course concierge (learner requests) --------------------

REQUEST_STATUSES = ["new", "reviewing", "building", "published", "rejected"]
OPEN_REQUEST_STATUSES = ("new", "reviewing", "building")


def create_course_request(conn: psycopg.Connection, learner_id: int, topic: str, detail: str) -> dict:
    return conn.execute(
        "INSERT INTO course_requests (learner_id, topic, detail) VALUES (%s, %s, %s) RETURNING *",
        (learner_id, topic, detail),
    ).fetchone()


def learner_requests(conn: psycopg.Connection, learner_id: int) -> list[dict]:
    return conn.execute(
        "SELECT * FROM course_requests WHERE learner_id = %s ORDER BY id DESC", (learner_id,)
    ).fetchall()


def open_request_count(conn: psycopg.Connection, learner_id: int) -> int:
    return conn.execute(
        "SELECT count(*) AS n FROM course_requests WHERE learner_id = %s AND status = ANY(%s)",
        (learner_id, list(OPEN_REQUEST_STATUSES)),
    ).fetchone()["n"]


def all_course_requests(conn: psycopg.Connection) -> list[dict]:
    """Every request with the requester's identity — the admin triage view."""
    return conn.execute(
        "SELECT r.*, l.email AS learner_email, l.name AS learner_name "
        "FROM course_requests r JOIN learners l ON l.id = r.learner_id "
        "ORDER BY (r.status = ANY(%s)) DESC, r.id DESC",
        (list(OPEN_REQUEST_STATUSES),),
    ).fetchall()


def update_course_request(
    conn: psycopg.Connection,
    request_id: int,
    status: str,
    course_slug: str | None = None,
    admin_note: str | None = None,
) -> dict | None:
    return conn.execute(
        "UPDATE course_requests SET status = %s, "
        "course_slug = COALESCE(%s, course_slug), "
        "admin_note = COALESCE(%s, admin_note), "
        "updated_at = now() WHERE id = %s RETURNING *",
        (status, course_slug, admin_note, request_id),
    ).fetchone()


# -------------------- progress / spaced repetition --------------------

def progress_map(conn: psycopg.Connection, learner_id: int) -> dict[int, dict]:
    rows = conn.execute(
        "SELECT * FROM progress WHERE learner_id = %s", (learner_id,)
    ).fetchall()
    return {r["node_id"]: r for r in rows}


def completions_today(conn: psycopg.Connection, learner_id: int) -> int:
    return conn.execute(
        "SELECT count(*) AS n FROM progress WHERE learner_id = %s AND completed_at IS NOT NULL "
        "AND completed_at::date = (now() AT TIME ZONE 'America/Santiago')::date",
        (learner_id,),
    ).fetchone()["n"]


def streak_days(conn: psycopg.Connection, learner_id: int) -> int:
    rows = conn.execute(
        "SELECT DISTINCT (completed_at AT TIME ZONE 'America/Santiago')::date AS d "
        "FROM progress WHERE learner_id = %s AND completed_at IS NOT NULL ORDER BY d DESC",
        (learner_id,),
    ).fetchall()
    if not rows:
        return 0
    import datetime as _dt
    today = conn.execute(
        "SELECT (now() AT TIME ZONE 'America/Santiago')::date AS t"
    ).fetchone()["t"]
    dates = [r["d"] for r in rows]
    # Streak counts back from today or yesterday (grace for "not done yet today").
    if dates[0] not in (today, today - _dt.timedelta(days=1)):
        return 0
    streak, cursor = 0, dates[0]
    for d in dates:
        if d == cursor:
            streak += 1
            cursor -= _dt.timedelta(days=1)
        elif d < cursor:
            break
    return streak


def record_completion(conn: psycopg.Connection, learner_id: int, node_id: int, quiz_score: float) -> dict:
    """Upsert progress on lesson completion and schedule the first review."""
    # A first completion always starts the review ladder at stage 0, whatever the
    # quiz score — the platform gates on engagement, not on passing (docs/02).
    # This used to read `0 if passed else 0`, a no-op ternary that looked like it
    # branched on the score and did not.
    stage = 0
    interval = REVIEW_INTERVALS[stage]
    return conn.execute(
        "INSERT INTO progress (learner_id, node_id, quiz_score, quiz_attempts, "
        "exercise_done, review_stage, next_review_at, completed_at, updated_at) "
        "VALUES (%s, %s, %s, 1, true, %s, now() + make_interval(days => %s), now(), now()) "
        # Best attempt wins here too: redoing a lesson can never lower what you scored.
        "ON CONFLICT (learner_id, node_id) DO UPDATE SET "
        "quiz_score = GREATEST(COALESCE(progress.quiz_score, 0), EXCLUDED.quiz_score), "
        "quiz_attempts = progress.quiz_attempts + 1, "
        "exercise_done = true, completed_at = COALESCE(progress.completed_at, now()), "
        "updated_at = now() RETURNING *",
        (learner_id, node_id, quiz_score, stage, interval),
    ).fetchone()


def record_review(conn: psycopg.Connection, learner_id: int, node_id: int, quiz_score: float) -> None:
    """Advance or reset the spaced-repetition ladder after a review session."""
    row = conn.execute(
        "SELECT review_stage FROM progress WHERE learner_id = %s AND node_id = %s",
        (learner_id, node_id),
    ).fetchone()
    if not row:
        return
    stage = row["review_stage"] + 1 if quiz_score >= 0.5 else 0
    stage = min(stage, len(REVIEW_INTERVALS) - 1)
    interval = REVIEW_INTERVALS[stage]
    # The ladder responds to THIS review's result, but the stored score keeps
    # the learner's best — a shaky review never erases what they earned.
    conn.execute(
        "UPDATE progress SET review_stage = %s, "
        "quiz_score = GREATEST(COALESCE(quiz_score, 0), %s), "
        "quiz_attempts = quiz_attempts + 1, "
        "next_review_at = now() + make_interval(days => %s), updated_at = now() "
        "WHERE learner_id = %s AND node_id = %s",
        (stage, quiz_score, interval, learner_id, node_id),
    )


def log_publish(
    conn: psycopg.Connection,
    channel: str,
    video_file: str,
    title: str,
    platform: str,
    request_id: str | None,
) -> None:
    conn.execute(
        "INSERT INTO publish_log (channel, video_file, title, platform, request_id) "
        "VALUES (%s, %s, %s, %s, %s)",
        (channel, video_file, title, platform, request_id),
    )
