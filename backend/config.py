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
    "Laura": "FGY2WhTYpPnrIDTdsKH5",
    "Saarah": "EXAVITQu4vr4xnSDxMaL",
    "Roger": "CwhRBWXzGAHq8TQ4Fs17",
    "Charlie": "IKne3meq5aSn9XLyUdCD",
    "George": "JBFqnCBsd6RMkjVDRZzb",
}

# Optional per-voice metadata for the frontend UI.
VOICE_META: dict[str, dict[str, str]] = {
    "Laura":   {"gender": "Female", "style": "Balanced / modern / premium"},
    "Saarah":  {"gender": "Female", "style": "Soft / elegant / clean"},
    "Roger":   {"gender": "Male",   "style": "Deep / strong / corporate"},
    "Charlie": {"gender": "Male",   "style": "Bright / quick / friendly"},
    "George":  {"gender": "Male",   "style": "Calm / mature / narrative"},
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
