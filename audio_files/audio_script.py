from playsound3 import playsound

def play_audio(file_path):
    try:
        playsound(file_path)
    except Exception as e:
        print(f"Playback error: {e}")