# ------------------------------------------------------------------------------
# JockStack — /api/stats endpoints
# All endpoints are read-only queries against the runs table.
# ------------------------------------------------------------------------------
from fastapi import APIRouter, Query
from models.schemas import StatsSummary, RunSummary
from models import db

router = APIRouter()


@router.get("/stats/summary", response_model=StatsSummary)
def summary():
    return db.get_summary()


@router.get("/stats/runs", response_model=list[RunSummary])
def recent_runs(limit: int = Query(default=100, ge=1, le=1000)):
    rows = db.get_recent_runs(limit=limit)
    return [
        RunSummary(
            run_id=r["id"],
            timestamp=r["timestamp"],
            stack_size=r["stack_size"],
            much_variant_count=r["much_variant_count"],
            max_name_length=r["max_name_length"],
        )
        for r in rows
    ]


@router.get("/stats/distribution")
def distribution():
    """Count of runs grouped by stack_size — histogram data."""
    return db.get_distribution()


@router.get("/stats/name_lengths")
def name_lengths():
    """Average name length per stack_size — scatter/line data."""
    return db.get_name_length_by_size()
