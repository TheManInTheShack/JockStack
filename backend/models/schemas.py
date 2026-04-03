# ------------------------------------------------------------------------------
# JockStack — Pydantic request/response models
# ------------------------------------------------------------------------------
from typing import Optional
from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    num_jocks: int = Field(ge=1, le=1000)


class JockEntry(BaseModel):
    size: int
    name: str


class RunStats(BaseModel):
    max_name_length: int
    avg_name_length: float
    much_variant_count: int
    longest_name: str


class GenerateResponse(BaseModel):
    run_id: int
    num_jocks: int
    jocks: list[JockEntry]   # sorted by size ascending
    stats: RunStats


class StatsSummary(BaseModel):
    total_runs: int
    total_jocks_generated: int
    avg_stack_size: float
    most_common_stack_size: Optional[int]
    total_much_variants: int


class RunSummary(BaseModel):
    run_id: int
    timestamp: str
    stack_size: int
    much_variant_count: int
    max_name_length: int
