import os
from pathlib import Path

from dotenv import load_dotenv


# ReadyMyVoice/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

ENV_FILE = PROJECT_ROOT / ".env"


load_dotenv(
    dotenv_path=ENV_FILE
)


class Settings:
    def __init__(self):
        self.ELEVENLABS_API_KEY = os.getenv(
            "ELEVENLABS_API_KEY",
            ""
        )

        self.ELEVENLABS_MODEL_ID = os.getenv(
            "ELEVENLABS_MODEL_ID",
            "eleven_multilingual_v2"
        )


settings = Settings()


print(
    "ENV file:",
    ENV_FILE
)

print(
    "ENV exists:",
    ENV_FILE.exists()
)

print(
    "ElevenLabs API key loaded:",
    bool(settings.ELEVENLABS_API_KEY)
)

print(
    "ElevenLabs model:",
    settings.ELEVENLABS_MODEL_ID
)