from pathlib import Path
from uuid import uuid4

import httpx

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from ..config import settings


router = APIRouter(
    prefix="/api",
    tags=["Ready My Voice"],
)


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

AUDIO_DIR = BASE_DIR / "generated_audio"

AUDIO_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ---------------------------------------------------------
# REQUEST MODEL
# ---------------------------------------------------------

class GenerateRequest(BaseModel):
    text: str = Field(
        min_length=1,
        max_length=10000,
    )

    # Real ElevenLabs voice ID coming from frontend
    voice_id: str

    # Optional — only used for logging/display
    voice_name: str | None = None

    stability: float = Field(
        default=0.5,
        ge=0,
        le=1,
    )

    similarity_boost: float = Field(
        default=0.75,
        ge=0,
        le=1,
    )


# ---------------------------------------------------------
# GET VOICES
#
# GET /api/voices
# ---------------------------------------------------------

@router.get("/voices")
async def get_voices():

    if not settings.ELEVENLABS_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="ELEVENLABS_API_KEY is not configured.",
        )

    url = "https://api.elevenlabs.io/v2/voices"

    headers = {
        "xi-api-key": settings.ELEVENLABS_API_KEY,
    }

    params = {
        "page_size": 100,
        "voice_type": "default",
    }

    try:
        async with httpx.AsyncClient(
            timeout=30.0
        ) as client:

            response = await client.get(
                url,
                headers=headers,
                params=params,
            )

    except httpx.RequestError as exc:

        raise HTTPException(
            status_code=502,
            detail="Could not connect to ElevenLabs.",
        ) from exc

    if response.status_code >= 400:

        try:
            error_data = response.json()
        except Exception:
            error_data = response.text

        raise HTTPException(
            status_code=response.status_code,
            detail=error_data,
        )

    data = response.json()

    voices = []

    for voice in data.get("voices", []):

        labels = voice.get("labels") or {}

        voice_id = voice.get("voice_id")

        name = voice.get("name")

        if not voice_id or not name:
            continue

        gender = (
            labels.get("gender")
            or "Unknown"
        )

        style = (
            labels.get("use_case")
            or labels.get("description")
            or labels.get("accent")
            or "General"
        )

        voices.append(
            {
                "name": name,
                "voice_id": voice_id,
                "gender": gender,
                "style": style,
            }
        )

    print()
    print("=" * 60)
    print("READY MY VOICE // VOICE CATALOG")
    print("VOICES RETURNED:", len(voices))
    print("=" * 60)

    return {
        "voices": voices,
        "count": len(voices),
    }


# ---------------------------------------------------------
# GET MEDIA
#
# GET /api/media
# ---------------------------------------------------------

@router.get("/media")
async def get_media():

    files = []

    if not AUDIO_DIR.exists():
        return files

    for filepath in sorted(
        AUDIO_DIR.glob("*.mp3"),
        key=lambda file: file.stat().st_mtime,
        reverse=True,
    ):

        files.append(
            {
                "filename": filepath.name,
                "url": f"/api/media/{filepath.name}",
                "size": filepath.stat().st_size,
            }
        )

    return files


# ---------------------------------------------------------
# SERVE MEDIA
#
# GET /api/media/{filename}
# ---------------------------------------------------------

@router.get("/media/{filename}")
async def serve_media(
    filename: str,
):

    safe_filename = Path(filename).name

    filepath = AUDIO_DIR / safe_filename

    if not filepath.exists():

        raise HTTPException(
            status_code=404,
            detail="Audio file not found.",
        )

    return FileResponse(
        filepath,
        media_type="audio/mpeg",
        filename=safe_filename,
    )


# ---------------------------------------------------------
# DELETE MEDIA
#
# DELETE /api/media/{filename}
# ---------------------------------------------------------

@router.delete("/media/{filename}")
async def delete_media(
    filename: str,
):

    safe_filename = Path(filename).name

    filepath = AUDIO_DIR / safe_filename

    if not filepath.exists():

        raise HTTPException(
            status_code=404,
            detail="Audio file not found.",
        )

    filepath.unlink()

    return {
        "success": True,
        "filename": safe_filename,
    }


# ---------------------------------------------------------
# GENERATE AUDIO
#
# POST /api/tts/generate
# ---------------------------------------------------------

@router.post("/tts/generate")
async def generate_voice(
    request: GenerateRequest,
):

    if not settings.ELEVENLABS_API_KEY:

        raise HTTPException(
            status_code=500,
            detail=(
                "ELEVENLABS_API_KEY "
                "is not configured."
            ),
        )

    text = request.text.strip()

    if not text:

        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty.",
        )

    voice_id = request.voice_id.strip()

    if not voice_id:

        raise HTTPException(
            status_code=400,
            detail="voice_id is required.",
        )

    voice_name = (
        request.voice_name
        or "Unknown"
    )

    print()
    print("=" * 60)
    print("READY MY VOICE // GENERATION")
    print("VOICE:", voice_name)
    print("VOICE ID:", voice_id)
    print("TEXT LENGTH:", len(text))
    print("=" * 60)

    url = (
        "https://api.elevenlabs.io/"
        f"v1/text-to-speech/{voice_id}"
    )

    headers = {
        "xi-api-key":
            settings.ELEVENLABS_API_KEY,

        "Content-Type":
            "application/json",

        "Accept":
            "audio/mpeg",
    }

    payload = {
        "text": text,

        "model_id":
            settings.ELEVENLABS_MODEL_ID,

        "voice_settings": {
            "stability":
                request.stability,

            "similarity_boost":
                request.similarity_boost,
        },
    }

    try:

        async with httpx.AsyncClient(
            timeout=120.0
        ) as client:

            response = await client.post(
                url,
                headers=headers,
                json=payload,
            )

    except httpx.RequestError as exc:

        print(
            "ELEVENLABS CONNECTION ERROR:",
            repr(exc),
        )

        raise HTTPException(
            status_code=502,
            detail=(
                "Could not connect "
                "to ElevenLabs."
            ),
        ) from exc

    print(
        "ELEVENLABS STATUS:",
        response.status_code,
    )

    if response.status_code >= 400:

        try:
            provider_error = response.json()
        except Exception:
            provider_error = response.text

        print(
            "ELEVENLABS ERROR:",
            provider_error,
        )

        raise HTTPException(
            status_code=response.status_code,
            detail={
                "voice":
                    voice_name,

                "voice_id":
                    voice_id,

                "elevenlabs":
                    provider_error,
            },
        )

    filename = (
        f"ready_my_voice_"
        f"{uuid4().hex[:12]}.mp3"
    )

    filepath = AUDIO_DIR / filename

    filepath.write_bytes(
        response.content
    )

    print(
        "SAVED:",
        filepath,
    )

    return {
        "success": True,

        "filename":
            filename,

        "voice":
            voice_name,

        "voice_id":
            voice_id,

        "url":
            f"/api/media/{filename}",
    }