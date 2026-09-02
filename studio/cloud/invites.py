"""Manage learner invite codes.

    python invites.py create "<label>" <max_uses>   # generate a code
    python invites.py list                           # show codes + usage
    python invites.py purge-test                     # remove @test.com learners
"""
import secrets
import sys
from pathlib import Path

STUDIO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STUDIO))
from cloud import db  # noqa


def create(label: str, max_uses: int) -> None:
    code = secrets.token_urlsafe(9)  # ~12 chars, unguessable
    with db.connect() as conn:
        db.create_invite(conn, code, label, max_uses)
        conn.commit()
    print(f"code: {code}  (label: {label!r}, max_uses: {max_uses})")
    print(f"invite link: /login?invite={code}")


def show() -> None:
    with db.connect() as conn:
        rows = conn.execute("SELECT * FROM invite_codes ORDER BY created_at").fetchall()
    for r in rows:
        print(f"{r['code']}  {r['uses']}/{r['max_uses']}  active={r['active']}  {r['label']!r}")
    if not rows:
        print("(no invite codes yet)")


def purge_test() -> None:
    with db.connect() as conn:
        n = conn.execute("DELETE FROM learner_sessions WHERE learner_id IN "
                         "(SELECT id FROM learners WHERE email LIKE '%@test.com')").rowcount
        conn.execute("DELETE FROM progress WHERE learner_id IN "
                     "(SELECT id FROM learners WHERE email LIKE '%@test.com')")
        conn.execute("DELETE FROM login_tokens WHERE learner_id IN "
                     "(SELECT id FROM learners WHERE email LIKE '%@test.com')")
        m = conn.execute("DELETE FROM learners WHERE email LIKE '%@test.com'").rowcount
        conn.commit()
    print(f"purged {m} test learners, {n} sessions")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "create":
        create(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 1)
    elif cmd == "purge-test":
        purge_test()
    else:
        show()
