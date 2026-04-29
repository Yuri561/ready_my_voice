"""Voice catalog endpoints."""
from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from ..config import VOICE_MAPPING, VOICE_META, settings


router = APIRouter(prefix="/api", tags=["voices"])


class Voice(BaseModel):
    name: str
    voice_id: str
    gender: str
    style: str


class VoiceList(BaseModel):
    voices: list[Voice]
    default: str


@router.get("/voices", response_model=VoiceList)
def list_voices() -> VoiceList:
    voices = [
        Voice(
            name=name,
            voice_id=vid,
            gender=VOICE_META.get(name, {}).get("gender", "Unknown"),
            style=VOICE_META.get(name, {}).get("style", ""),
        )
        for name, vid in VOICE_MAPPING.items()
    ]
    return VoiceList(voices=voices, default=settings.default_voice)
