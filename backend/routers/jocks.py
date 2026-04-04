# ------------------------------------------------------------------------------
# JockStack — /api/generate endpoint
# ------------------------------------------------------------------------------
from fastapi import APIRouter
from models.schemas import GenerateRequest, GenerateResponse, JockEntry, RunStats
from models.db import save_run
from jockstack import stack_jocks

router = APIRouter()


@router.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    # Run the algorithm — returns list in generation order (the display order)
    raw = stack_jocks(req.num_jocks)
    jocks = [JockEntry(size=r["size"], name=r["name"]) for r in raw]

    # Derive per-run stats
    names = [j.name for j in jocks]
    lengths = [len(n) for n in names]
    stats = RunStats(
        max_name_length=max(lengths) if lengths else 0,
        avg_name_length=round(sum(lengths) / len(lengths), 2) if lengths else 0.0,
        much_variant_count=sum(1 for n in names if "Much-" in n),
        longest_name=max(names, key=len) if names else "",
    )

    # Persist
    run_id = save_run(
        stack_size=req.num_jocks,
        jocks=[j.model_dump() for j in jocks],
    )

    return GenerateResponse(
        run_id=run_id,
        num_jocks=req.num_jocks,
        jocks=jocks,
        stats=stats,
    )
