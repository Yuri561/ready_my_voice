"""FastAPI backend for the Ready My Voice Tauri app."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import health, media, tts, voices

app = FastAPI(
    title="Ready My Voice API",
    description="Backend API for the Ready My Voice Tauri app.",
    version="0.1.0",
)

# Tauri dev server origins. The Tauri webview uses the `tauri://localhost`
# (and `https://tauri.localhost` on Windows) origins in production, and the
# Vite dev server on port 1420 during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:1420",
        "http://127.0.0.1:1420",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "tauri://localhost",
        "https://tauri.localhost",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(voices.router)
app.include_router(tts.router)
app.include_router(media.router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Ready My Voice API", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )
