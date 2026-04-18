import customtkinter as ctk
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

APP_NAME = "Ready My Voice"
WINDOW_SIZE = "1540x940"
MEDIA_FOLDER = "audio_files"

os.makedirs(MEDIA_FOLDER, exist_ok=True)

VOICE_MAPPING = {
    "Laura": "FGY2WhTYpPnrIDTdsKH5",
    "Saarah": "EXAVITQu4vr4xnSDxMaL",
    "Roger": "CwhRBWXzGAHq8TQ4Fs17",
    "Charlie": "IKne3meq5aSn9XLyUdCD",
    "George": "JBFqnCBsd6RMkjVDRZzb",
    "Default": "FGY2WhTYpPnrIDTdsKH5"
}

