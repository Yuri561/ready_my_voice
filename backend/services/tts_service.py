"""ElevenLabs text-to-speech service."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from elevenlabs.client import ElevenLabs
from fastapi import HTTPException, status

from ..config import settings, VOICE_MAPPING


_client: ElevenLabs | None = None


def _get_client() -> ElevenLabs:
    global _client
    if not settings.elevenlabs_api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "ELEVENLABS_API_KEY is not set. Add it to backend/.env "
                "(see backend/.env.example)."
            ),
        )
    if _client is None:
        _client = ElevenLabs(api_key=settings.elevenlabs_api_key)
    return _client


def resolve_voice_id(voice: str | None) -> str:
    """Accept either a friendly voice name or a raw ElevenLabs voice id."""
    if not voice:
        return VOICE_MAPPING[settings.default_voice]
    if voice in VOICE_MAPPING:
        return VOICE_MAPPING[voice]
    # Treat as raw voice id.
    return voice


def synthesize_to_file(text: str, voice: str | None = None) -> Path:
    """Generate audio for `text` and save it as a timestamped mp3.

    Returns the absolute path of the saved file.
    """
    if not text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Script text is required.",
        )

    client = _get_client()
    voice_id = resolve_voice_id(voice)

    try:
        response = client.text_to_speech.convert(
            voice_id=voice_id,
            output_format=settings.elevenlabs_output_format,
            text=text,
            model_id=settings.elevenlabs_model,
        )
    except Exception as exc:  # ElevenLabs SDK raises various subclasses
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"ElevenLabs request failed: {exc}",
        ) from exc

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = settings.media_folder / f"output_{timestamp}.mp3"

    with open(file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    return file_path
