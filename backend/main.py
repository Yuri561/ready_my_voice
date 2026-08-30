from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.tts import router as tts_router


app = FastAPI(
    title="Ready My Voice API",
    version="1.0.0",
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# ROUTERS
# ---------------------------------------------------------

app.include_router(tts_router)


# ---------------------------------------------------------
# ROOT
# ---------------------------------------------------------

@app.get("/")
async def root():
    return {
        "name": "Ready My Voice API",
        "status": "running",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
    }