from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class Post:
    id: int
    title: str
    body: str
    image_path: str
    slug: str
    status: str
    published_at: str | None
    created_at: str


def init_db(db_path: str | Path) -> None:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                title        TEXT    NOT NULL,
                body         TEXT    NOT NULL DEFAULT '',
                image_path   TEXT    NOT NULL,
                slug         TEXT    UNIQUE NOT NULL,
                status       TEXT    NOT NULL CHECK(status IN ('draft', 'published')),
                published_at TEXT,
                created_at   TEXT    NOT NULL
            )
        """)
        conn.commit()


def slugify(title: str) -> str:
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-") or "post"


def unique_slug(conn: sqlite3.Connection, title: str) -> str:
    base = slugify(title)
    slug = base
    n = 1
    while True:
        row = conn.execute("SELECT id FROM posts WHERE slug = ?", (slug,)).fetchone()
        if row is None:
            return slug
        slug = f"{base}-{n}"
        n += 1


def create_post(
    conn: sqlite3.Connection,
    title: str,
    body: str,
    image_path: str,
    status: str,
) -> int:
    now = datetime.now(timezone.utc).isoformat()
    slug = unique_slug(conn, title)
    published_at = now if status == "published" else None
    cur = conn.execute(
        "INSERT INTO posts (title, body, image_path, slug, status, published_at, created_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?)",
        (title, body, image_path, slug, status, published_at, now),
    )
    conn.commit()
    return cur.lastrowid


def _row_to_post(row: tuple) -> Post:
    return Post(
        id=row[0],
        title=row[1],
        body=row[2],
        image_path=row[3],
        slug=row[4],
        status=row[5],
        published_at=row[6],
        created_at=row[7],
    )


def get_latest_published(conn: sqlite3.Connection) -> Post | None:
    row = conn.execute(
        "SELECT id, title, body, image_path, slug, status, published_at, created_at"
        " FROM posts WHERE status = 'published' ORDER BY published_at DESC LIMIT 1"
    ).fetchone()
    return _row_to_post(row) if row else None


def get_post_by_slug(conn: sqlite3.Connection, slug: str) -> Post | None:
    row = conn.execute(
        "SELECT id, title, body, image_path, slug, status, published_at, created_at"
        " FROM posts WHERE slug = ?",
        (slug,),
    ).fetchone()
    return _row_to_post(row) if row else None


def get_prev_next(
    conn: sqlite3.Connection, published_at: str
) -> tuple[Post | None, Post | None]:
    prev_row = conn.execute(
        "SELECT id, title, body, image_path, slug, status, published_at, created_at"
        " FROM posts WHERE status = 'published' AND published_at < ?"
        " ORDER BY published_at DESC LIMIT 1",
        (published_at,),
    ).fetchone()
    next_row = conn.execute(
        "SELECT id, title, body, image_path, slug, status, published_at, created_at"
        " FROM posts WHERE status = 'published' AND published_at > ?"
        " ORDER BY published_at ASC LIMIT 1",
        (published_at,),
    ).fetchone()
    return (
        _row_to_post(prev_row) if prev_row else None,
        _row_to_post(next_row) if next_row else None,
    )
