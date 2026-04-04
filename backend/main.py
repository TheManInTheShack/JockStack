# ------------------------------------------------------------------------------
# JockStack — FastAPI application
# ------------------------------------------------------------------------------
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from models.db import init_db
from routers import jocks, stats

app = FastAPI(title="JockStack")


@app.on_event("startup")
def startup():
    init_db()


# Allow requests from the Godot HTML5 frontend on the same origin.
# In production Nginx handles this; CORS middleware covers local dev.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jocks.router, prefix="/api")
app.include_router(stats.router, prefix="/api")


@app.get("/stats", response_class=HTMLResponse)
def stats_page():
    from stats_page import render_stats_page
    return render_stats_page()


@app.get("/health")
def health():
    return {"status": "ok"}
