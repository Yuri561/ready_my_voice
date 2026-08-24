"""Application configuration loaded from environment variables."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

# Load backend/.env (if present)
load_dotenv(Path(__file__).resolve().parent / ".env")

# Project root is the parent of the backend/ folder. The existing Python app
# stores audio under <project_root>/audio_files, and we share that folder so
# both apps see the same media vault.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MEDIA_FOLDER = PROJECT_ROOT / "audio_files"


# Maps the friendly name shown in the UI to the ElevenLabs voice id.
# Mirrors VOICE_MAPPING from the existing Python app's config.py.
VOICE_MAPPING: dict[str, str] = {
   
  "Liam": "TX3LPaxmHKxFdv7VOQHJ",
  "Rachel": "21m00Tcm4TlvDq8ikWAM",
  "Bella": "EXAVITQu4vr4xnSDxMaL",
  "Antoni": "ErXwobaYiN019PkySvjV",
  "Elli": "MF3mGyEYCl7XYWbV9V6O",
  "Josh": "TxGEqnHWrfWFTfGW9XjX",
  "Arnold": "VR6AewLTigWG4xSOukaG",
  "Adam": "pNInz6obpgDQGcFmaJgB",
  "Sam": "yoZ06aMxZJJ28mfd3POQ",
  "Nicole": "piTKgcLEGmPE4e6mEKli",
  "Domi": "AZnzlk1XvdvUeBnXmlld",
  "Fin": "D38z5RcWu1voky8WS1ja",
  "Thomas": "GBv7mTt0atIp3Br8iCZE",
  "Emily": "LcfcDJNUP1GQjkzn1xUU",
  "Callum": "N2lVS1w4EtoT3dr4eOWO"

}

# Optional per-voice metadata for the frontend UI.
VOICE_META: dict[str, dict[str, str]] = {
            "Liam": {
        "gender": "Male",
        "style": "Smooth / cinematic / storyteller"
        },

        "Rachel": {
        "gender": "Female",
        "style": "Natural / warm / conversational"
        },

        "Bella": {
        "gender": "Female",
        "style": "Soft / emotional / expressive"
        },

        "Antoni": {
        "gender": "Male",
        "style": "Deep / confident / cinematic"
        },

        "Elli": {
        "gender": "Female",
        "style": "Relaxed / modern / friendly"
        },

        "Josh": {
        "gender": "Male",
        "style": "Energetic / creator / engaging"
        },

        "Arnold": {
        "gender": "Male",
        "style": "Powerful / dramatic / trailer"
        },

        "Adam": {
        "gender": "Male",
        "style": "Professional / balanced / narrator"
        },

        "Sam": {
        "gender": "Male",
        "style": "Young / casual / podcast"
        },

        "Nicole": {
        "gender": "Female",
        "style": "Elegant / luxury / smooth"
        },

        "Domi": {
        "gender": "Female",
        "style": "Strong / cinematic / emotional"
        },

        "Fin": {
        "gender": "Male",
        "style": "Youthful / upbeat / modern"
        },

        "Thomas": {
        "gender": "Male",
        "style": "Narrative / calm / documentary"
        },

        "Emily": {
        "gender": "Female",
        "style": "Bright / clean / commercial"
        },

        "Callum": {
        "gender": "Male",
        "style": "Deep / gritty / cinematic"

        }
}

@dataclass(frozen=True)
class Settings:
    host: str = os.getenv("RMV_HOST", "127.0.0.1")
    port: int = int(os.getenv("RMV_PORT", "8000"))
    reload: bool = os.getenv("RMV_RELOAD", "1") == "1"

    elevenlabs_api_key: str | None = os.getenv("ELEVENLABS_API_KEY")
    elevenlabs_model: str = os.getenv("ELEVENLABS_MODEL", "eleven_multilingual_v2")
    elevenlabs_output_format: str = os.getenv(
        "ELEVENLABS_OUTPUT_FORMAT", "mp3_44100_128"
    )

    media_folder: Path = field(
        default_factory=lambda: Path(
            os.getenv("RMV_MEDIA_FOLDER", str(DEFAULT_MEDIA_FOLDER))
        )
    )

    default_voice: str = os.getenv("RMV_DEFAULT_VOICE", "Laura")


settings = Settings()
settings.media_folder.mkdir(parents=True, exist_ok=True)
