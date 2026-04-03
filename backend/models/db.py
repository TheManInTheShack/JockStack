# ------------------------------------------------------------------------------
# JockStack — SQLite database layer
# One table: runs. Each row is one stack generation event.
# ------------------------------------------------------------------------------
import json
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone


DB_PATH = os.environ.get("JOCKSTACK_DB_PATH", "../data/jockstack.db")


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS runs (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp           TEXT    NOT NULL,
                stack_size          INTEGER NOT NULL,
                jocks_json          TEXT    NOT NULL,
                max_name_length     INTEGER NOT NULL,
                avg_name_length     REAL    NOT NULL,
                much_variant_count  INTEGER NOT NULL,
                longest_name        TEXT    NOT NULL
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_runs_timestamp  ON runs(timestamp)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_runs_stack_size ON runs(stack_size)")


# ------------------------------------------------------------------------------
# Write
# ------------------------------------------------------------------------------

def save_run(stack_size: int, jocks: list[dict]) -> int:
    """
    Persist one run. jocks is a list of {"size": int, "name": str} dicts,
    sorted by size ascending. Returns the new run id.
    """
    names = [j["name"] for j in jocks]
    lengths = [len(n) for n in names]
    max_name_length = max(lengths) if lengths else 0
    avg_name_length = sum(lengths) / len(lengths) if lengths else 0.0
    much_variant_count = sum(1 for n in names if "Much-" in n)
    longest_name = max(names, key=len) if names else ""

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO runs
                (timestamp, stack_size, jocks_json,
                 max_name_length, avg_name_length,
                 much_variant_count, longest_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                stack_size,
                json.dumps(jocks),
                max_name_length,
                avg_name_length,
                much_variant_count,
                longest_name,
            ),
        )
        return cur.lastrowid


# ------------------------------------------------------------------------------
# Read — stats queries
# ------------------------------------------------------------------------------

def get_summary() -> dict:
    with get_conn() as conn:
        row = conn.execute("""
            SELECT
                COUNT(*)                    AS total_runs,
                COALESCE(SUM(stack_size),0) AS total_jocks,
                COALESCE(AVG(stack_size),0) AS avg_stack_size,
                COALESCE(SUM(much_variant_count),0) AS total_much_variants
            FROM runs
        """).fetchone()

        # Most common stack size
        mode_row = conn.execute("""
            SELECT stack_size
            FROM runs
            GROUP BY stack_size
            ORDER BY COUNT(*) DESC
            LIMIT 1
        """).fetchone()

    return {
        "total_runs": row["total_runs"],
        "total_jocks_generated": row["total_jocks"],
        "avg_stack_size": round(row["avg_stack_size"], 2),
        "most_common_stack_size": mode_row["stack_size"] if mode_row else None,
        "total_much_variants": row["total_much_variants"],
    }


def get_recent_runs(limit: int = 100) -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT id, timestamp, stack_size, much_variant_count, max_name_length
            FROM runs
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()
    return [dict(r) for r in rows]


def get_distribution() -> list[dict]:
    """Count of runs grouped by stack_size."""
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT stack_size, COUNT(*) AS run_count
            FROM runs
            GROUP BY stack_size
            ORDER BY stack_size
        """).fetchall()
    return [dict(r) for r in rows]


def get_name_length_by_size() -> list[dict]:
    """Average name length grouped by stack_size bucket."""
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT stack_size, AVG(avg_name_length) AS avg_name_length
            FROM runs
            GROUP BY stack_size
            ORDER BY stack_size
        """).fetchall()
    return [{"stack_size": r["stack_size"], "avg_name_length": round(r["avg_name_length"], 2)}
            for r in rows]
