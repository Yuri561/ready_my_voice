"""Text-to-speech endpoints."""
from __future__ import annotations

from pydantic import BaseModel, Field

from fastapi import APIRouter

from ..services.tts_service import synthesize_to_file


router = APIRouter(prefix="/api/tts", tags=["tts"])


class GenerateRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Script text to synthesize.")
    voice: str | None = Field(
        default=None,
        description="Friendly voice name (e.g. 'Laura') or raw ElevenLabs voice_id.",
    )


class GenerateResponse(BaseModel):
    filename: str
    url: str
    voice: str | None


@router.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest) -> GenerateResponse:
    file_path = synthesize_to_file(req.text, req.voice)
    filename = file_path.name
    return GenerateResponse(
        filename=filename,
        url=f"/api/media/{filename}",
        voice=req.voice,
    )
