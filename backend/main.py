# ------------------------------------------------------------------------------
# JockStack — FastAPI application
# ------------------------------------------------------------------------------
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.db import init_db
from routers import jocks

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


@app.get("/health")
def health():
    return {"status": "ok"}
