"""SQLite-backed state, cache, and observability storage."""

from __future__ import annotations

import json
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class CacheHit:
    cache_key: str
    response_text: str
    provider: str
    model: str
    similarity: float
    metadata: dict[str, Any]


class StateStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS runs (
                    id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    project_name TEXT NOT NULL,
                    tool_name TEXT NOT NULL,
                    provider TEXT,
                    model TEXT,
                    task_type TEXT,
                    mode TEXT,
                    cache_key TEXT,
                    cached INTEGER NOT NULL DEFAULT 0,
                    ok INTEGER NOT NULL DEFAULT 0,
                    elapsed_ms INTEGER,
                    estimated_input_tokens INTEGER,
                    estimated_output_tokens INTEGER,
                    estimated_cost REAL,
                    summary TEXT,
                    payload_json TEXT,
                    error TEXT
                );

                CREATE TABLE IF NOT EXISTS cache_entries (
                    cache_key TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    normalized_prompt TEXT NOT NULL,
                    task_type TEXT NOT NULL,
                    provider TEXT NOT NULL,
                    model TEXT NOT NULL,
                    response_text TEXT NOT NULL,
                    metadata_json TEXT NOT NULL
                );
                """
            )

    def record_run(self, payload: dict[str, Any]) -> str:
        run_id = payload.get("id") or str(uuid.uuid4())
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO runs (
                    id, created_at, project_name, tool_name, provider, model, task_type, mode,
                    cache_key, cached, ok, elapsed_ms, estimated_input_tokens, estimated_output_tokens,
                    estimated_cost, summary, payload_json, error
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run_id,
                    datetime.now(UTC).isoformat(),
                    payload.get("project_name", "orchestrator-mcp"),
                    payload.get("tool_name", "llm_ask"),
                    payload.get("provider"),
                    payload.get("model"),
                    payload.get("task_type"),
                    payload.get("mode"),
                    payload.get("cache_key"),
                    int(bool(payload.get("cached", False))),
                    int(bool(payload.get("ok", False))),
                    payload.get("elapsed_ms"),
                    payload.get("estimated_input_tokens"),
                    payload.get("estimated_output_tokens"),
                    payload.get("estimated_cost"),
                    payload.get("summary"),
                    json.dumps(payload, ensure_ascii=True),
                    payload.get("error"),
                ),
            )
        return run_id

    def record_cache_entry(
        self,
        cache_key: str,
        normalized_prompt: str,
        task_type: str,
        provider: str,
        model: str,
        response_text: str,
        metadata: dict[str, Any],
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO cache_entries (
                    cache_key, created_at, normalized_prompt, task_type, provider, model, response_text, metadata_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    cache_key,
                    datetime.now(UTC).isoformat(),
                    normalized_prompt,
                    task_type,
                    provider,
                    model,
                    response_text,
                    json.dumps(metadata, ensure_ascii=True),
                ),
            )

    def find_similar_cache(self, normalized_prompt: str, task_type: str, threshold: float) -> CacheHit | None:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT cache_key, normalized_prompt, provider, model, response_text, metadata_json
                FROM cache_entries
                WHERE task_type = ?
                ORDER BY created_at DESC
                LIMIT 100
                """,
                (task_type,),
            ).fetchall()
        best_hit: CacheHit | None = None
        for row in rows:
            similarity = SequenceMatcher(None, normalized_prompt, row["normalized_prompt"]).ratio()
            if similarity < threshold:
                continue
            candidate = CacheHit(
                cache_key=row["cache_key"],
                response_text=row["response_text"],
                provider=row["provider"],
                model=row["model"],
                similarity=similarity,
                metadata=json.loads(row["metadata_json"]),
            )
            if best_hit is None or candidate.similarity > best_hit.similarity:
                best_hit = candidate
        return best_hit

    def get_recent_runs(self, limit: int = 50) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, created_at, project_name, tool_name, provider, model, task_type, cached,
                       ok, elapsed_ms, estimated_cost, summary, error
                FROM runs
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]

    def get_model_stats(self) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT provider, model, COUNT(*) AS total_runs,
                       SUM(CASE WHEN ok = 1 THEN 1 ELSE 0 END) AS successful_runs,
                       AVG(CASE WHEN elapsed_ms IS NOT NULL THEN elapsed_ms ELSE NULL END) AS avg_elapsed_ms
                FROM runs
                WHERE model IS NOT NULL
                GROUP BY provider, model
                ORDER BY total_runs DESC, successful_runs DESC
                """
            ).fetchall()
        payload: list[dict[str, Any]] = []
        for row in rows:
            total = int(row["total_runs"] or 0)
            successful = int(row["successful_runs"] or 0)
            payload.append(
                {
                    "provider": row["provider"],
                    "model": row["model"],
                    "total_runs": total,
                    "successful_runs": successful,
                    "success_rate": round((successful / total) * 100, 2) if total else 0.0,
                    "avg_elapsed_ms": round(float(row["avg_elapsed_ms"] or 0.0), 2),
                }
            )
        return payload

    def get_project_costs(self) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT project_name,
                       COUNT(*) AS total_runs,
                       ROUND(SUM(COALESCE(estimated_cost, 0.0)), 6) AS total_cost
                FROM runs
                GROUP BY project_name
                ORDER BY total_cost DESC, total_runs DESC
                """
            ).fetchall()
        return [dict(row) for row in rows]

    def get_budget_status(self, project_name: str, daily_limit: float, weekly_limit: float) -> dict[str, float]:
        with self._connect() as conn:
            daily = conn.execute(
                """
                SELECT ROUND(SUM(COALESCE(estimated_cost, 0.0)), 6) AS total_cost
                FROM runs
                WHERE project_name = ? AND created_at >= datetime('now', '-1 day')
                """,
                (project_name,),
            ).fetchone()
            weekly = conn.execute(
                """
                SELECT ROUND(SUM(COALESCE(estimated_cost, 0.0)), 6) AS total_cost
                FROM runs
                WHERE project_name = ? AND created_at >= datetime('now', '-7 day')
                """,
                (project_name,),
            ).fetchone()
        daily_spent = float(daily["total_cost"] or 0.0)
        weekly_spent = float(weekly["total_cost"] or 0.0)
        return {
            "daily_spent": daily_spent,
            "weekly_spent": weekly_spent,
            "daily_remaining": max(daily_limit - daily_spent, 0.0),
            "weekly_remaining": max(weekly_limit - weekly_spent, 0.0),
        }

    def get_run(self, run_id: str) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute("SELECT payload_json FROM runs WHERE id = ?", (run_id,)).fetchone()
        if row is None:
            return None
        return json.loads(row["payload_json"])

