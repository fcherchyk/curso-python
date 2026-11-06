"""Progress persistence in SQLite (single local user)."""

from __future__ import annotations

import sqlite3
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path

from app.legacy_ids import translate_id

SCHEMA = """
CREATE TABLE IF NOT EXISTS chapters (
    id          TEXT PRIMARY KEY,
    read        INTEGER NOT NULL DEFAULT 0,
    quiz_ok     INTEGER NOT NULL DEFAULT 0,
    quiz_best   REAL    NOT NULL DEFAULT 0,
    tests_ok    INTEGER NOT NULL DEFAULT 0,
    code        TEXT,
    updated     TEXT    NOT NULL DEFAULT (datetime('now'))
)
"""


@dataclass(frozen=True)
class Status:
    read: bool = False
    quiz_ok: bool = False
    quiz_best: float = 0.0
    tests_ok: bool = False
    code: str | None = None

    @property
    def complete(self) -> bool:
        return self.read and self.quiz_ok and self.tests_ok


class Progress:
    def __init__(self, path: Path) -> None:
        self.path = path

    def _connect(self) -> sqlite3.Connection:
        con = sqlite3.connect(self.path)
        con.row_factory = sqlite3.Row
        # Idempotent: if you delete progress.db while the app runs, it is recreated.
        con.execute(SCHEMA)
        return con

    def import_legacy(self, legacy_path: Path) -> int:
        """Imports progress from the Spanish-era database (`progreso.db`, table `capitulos`).

        Only runs while this store is empty, so it is safe to call on every startup. Old ids
        (with or without the course prefix) are mapped to the current English slugs. The legacy
        file is only read, never modified. Returns the number of imported chapters.
        """
        if not legacy_path.exists() or legacy_path.resolve() == self.path.resolve():
            return 0
        with closing(self._connect()) as con:
            if con.execute("SELECT 1 FROM chapters LIMIT 1").fetchone():
                return 0
        with closing(sqlite3.connect(f"file:{legacy_path}?mode=ro", uri=True)) as old:
            old.row_factory = sqlite3.Row
            try:
                rows = old.execute("SELECT * FROM capitulos").fetchall()
            except sqlite3.DatabaseError:
                return 0
        with closing(self._connect()) as con, con:
            con.executemany(
                "INSERT OR IGNORE INTO chapters "
                "(id, read, quiz_ok, quiz_best, tests_ok, code, updated) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                [
                    (
                        translate_id(r["id"]),
                        r["leido"],
                        r["quiz_ok"],
                        r["quiz_mejor"],
                        r["tests_ok"],
                        r["codigo"],
                        r["actualizado"],
                    )
                    for r in rows
                ],
            )
        return len(rows)

    def _upsert(self, chapter_id: str, **fields: object) -> None:
        columns = ", ".join(fields)
        placeholders = ", ".join("?" for _ in fields)
        assignments = ", ".join(f"{c} = excluded.{c}" for c in fields)
        sql = (
            f"INSERT INTO chapters (id, {columns}) VALUES (?, {placeholders}) "
            f"ON CONFLICT(id) DO UPDATE SET {assignments}, updated = datetime('now')"
        )
        with closing(self._connect()) as con, con:
            con.execute(sql, (chapter_id, *fields.values()))

    def status(self, chapter_id: str) -> Status:
        return self.all().get(chapter_id, Status())

    def all(self) -> dict[str, Status]:
        with closing(self._connect()) as con:
            rows = con.execute("SELECT * FROM chapters").fetchall()
        return {
            r["id"]: Status(
                read=bool(r["read"]),
                quiz_ok=bool(r["quiz_ok"]),
                quiz_best=r["quiz_best"],
                tests_ok=bool(r["tests_ok"]),
                code=r["code"],
            )
            for r in rows
        }

    def mark_read(self, chapter_id: str, read: bool = True) -> None:
        self._upsert(chapter_id, read=int(read))

    def mark_quiz(self, chapter_id: str, ok: bool = True) -> None:
        self._upsert(chapter_id, quiz_ok=int(ok))

    def mark_tests(self, chapter_id: str, ok: bool = True) -> None:
        self._upsert(chapter_id, tests_ok=int(ok))

    def record_quiz(self, chapter_id: str, score: float, passed: bool) -> None:
        # The best score and the pass never go backwards on a retry.
        current = self.status(chapter_id)
        self._upsert(
            chapter_id,
            quiz_best=max(current.quiz_best, score),
            quiz_ok=int(current.quiz_ok or passed),
        )

    def save_code(self, chapter_id: str, code: str) -> None:
        self._upsert(chapter_id, code=code)

    def record_tests(self, chapter_id: str, code: str, passed: bool) -> None:
        current = self.status(chapter_id)
        self._upsert(chapter_id, code=code, tests_ok=int(current.tests_ok or passed))
