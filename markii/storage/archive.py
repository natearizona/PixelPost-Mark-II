from __future__ import annotations

import sqlite3
from contextlib import AbstractContextManager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from markii.media.inventory import Artifact


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS import_runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  profile_name TEXT,
  operation TEXT NOT NULL,
  started_at TEXT NOT NULL,
  completed_at TEXT,
  status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS source_artifacts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_path TEXT NOT NULL,
  filename TEXT NOT NULL,
  artifact_type TEXT NOT NULL,
  file_size INTEGER,
  sha256 TEXT,
  detection_rule TEXT NOT NULL,
  created_at TEXT NOT NULL,
  UNIQUE(source_path, sha256)
);

CREATE TABLE IF NOT EXISTS provenance_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  import_run_id INTEGER NOT NULL,
  source_artifact_id INTEGER NOT NULL,
  entity_type TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  decision TEXT NOT NULL,
  notes TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY(import_run_id) REFERENCES import_runs(id),
  FOREIGN KEY(source_artifact_id) REFERENCES source_artifacts(id)
);
"""


class Archive(AbstractContextManager):
    def __init__(self, path: Path):
        self.path = path
        self.connection: sqlite3.Connection | None = None

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self.connection.executescript(SCHEMA)
        return self

    def __exit__(self, exc_type, exc, traceback):
        if self.connection is None:
            return None
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        self.connection.close()
        self.connection = None
        return None

    def create_import_run(self, profile_name: str | None, operation: str) -> int:
        cursor = self._connection.execute(
            """
            INSERT INTO import_runs (profile_name, operation, started_at, status)
            VALUES (?, ?, ?, ?)
            """,
            (profile_name, operation, utc_now(), "running"),
        )
        return int(cursor.lastrowid)

    def complete_import_run(self, run_id: int, status: str) -> None:
        self._connection.execute(
            """
            UPDATE import_runs
            SET completed_at = ?, status = ?
            WHERE id = ?
            """,
            (utc_now(), status, run_id),
        )

    def upsert_source_artifact(self, artifact: Artifact) -> int:
        self._connection.execute(
            """
            INSERT INTO source_artifacts (
              source_path, filename, artifact_type, file_size, sha256,
              detection_rule, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(source_path, sha256) DO UPDATE SET
              filename = excluded.filename,
              artifact_type = excluded.artifact_type,
              file_size = excluded.file_size,
              detection_rule = excluded.detection_rule
            """,
            (
                artifact.source_path,
                artifact.filename,
                artifact.artifact_type,
                artifact.file_size,
                artifact.sha256,
                artifact.detection_rule,
                utc_now(),
            ),
        )
        row = self._connection.execute(
            """
            SELECT id FROM source_artifacts
            WHERE source_path = ?
              AND (sha256 = ? OR (sha256 IS NULL AND ? IS NULL))
            """,
            (artifact.source_path, artifact.sha256, artifact.sha256),
        ).fetchone()
        return int(row["id"])

    def record_provenance_event(
        self,
        import_run_id: int,
        source_artifact_id: int,
        entity_type: str,
        entity_id: str,
        decision: str,
        notes: str | None = None,
    ) -> int:
        cursor = self._connection.execute(
            """
            INSERT INTO provenance_events (
              import_run_id, source_artifact_id, entity_type, entity_id,
              decision, notes, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                import_run_id,
                source_artifact_id,
                entity_type,
                entity_id,
                decision,
                notes,
                utc_now(),
            ),
        )
        return int(cursor.lastrowid)

    def counts(self) -> dict[str, int]:
        return {
            "source_artifacts": self._count("source_artifacts"),
            "import_runs": self._count("import_runs"),
            "provenance_events": self._count("provenance_events"),
        }

    def _count(self, table: str) -> int:
        row = self._connection.execute(f"SELECT COUNT(*) AS count FROM {table}").fetchone()
        return int(row["count"])

    @property
    def _connection(self) -> sqlite3.Connection:
        if self.connection is None:
            raise RuntimeError("Archive is not open")
        return self.connection


def fetch_counts(path: Path) -> dict[str, int]:
    with sqlite3.connect(path) as connection:
        return {
            "source_artifacts": _fetch_count(connection, "source_artifacts"),
            "import_runs": _fetch_count(connection, "import_runs"),
            "provenance_events": _fetch_count(connection, "provenance_events"),
        }


def fetch_sample(path: Path, table: str, limit: int = 5) -> list[dict[str, Any]]:
    with sqlite3.connect(path) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(f"SELECT * FROM {table} ORDER BY id LIMIT ?", (limit,)).fetchall()
        return [dict(row) for row in rows]


def _fetch_count(connection: sqlite3.Connection, table: str) -> int:
    row = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
    return int(row[0])


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

