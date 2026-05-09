from fastapi import APIRouter
from dotenv import load_dotenv
from pydantic import BaseModel
import os
from elevenlabs.client import ElevenLabs
from pathlib import Path

load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)


router = APIRouter(prefix="/api", tags=["intro"])

class IntroReq(BaseModel):
    text: str
    voice_id: str | None = None

#grabbing user's homedirectory yp
saved_path = Path.home()






@router.post("/intro")
def generate_intro_voice(payload:IntroReq):
    text = payload.text
    voice_id = payload.voice_id or os.getenv("INTRO_VOICE_ID")
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id="eleven_v3",
    )
    with open(saved_path, "wb") as f:
        f.write(audio)
    return {"message": "Intro voice generated and played successfully.",
            "saved_file": audio
            }