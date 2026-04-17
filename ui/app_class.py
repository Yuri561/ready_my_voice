import customtkinter as ctk
from tkinter import filedialog
import os
import time
from pathlib import Path

from config import APP_NAME, WINDOW_SIZE, MEDIA_FOLDER, VOICE_MAPPING
from utils.download_file import download_file
from utils.intro_txt import intro_txt, process_command
from utils.voice_api import txt_to_speech, speak_text
from audio_files.audio_script import play_audio

from ui.shell import build_shell
from ui.sidebar import build_sidebar
from ui.topbar import build_topbar
from ui.helpers import (
    make_sidebar_stat,
    make_small_metric,
    make_slider_row,
    setting_row,
)
from ui.views.studio import build_studio_view
from ui.views.projects import build_projects_view
from ui.views.media import build_media_view
from ui.views.voices import build_voices_view
from ui.views.settings import build_settings_view


class ReadyMyVoiceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        self.geometry(WINDOW_SIZE)
        self.minsize(1360, 860)
        self.configure(fg_color="#050816")

        self.current_audio_path = None
        self.current_voice_name = "Laura"
        self.processing = False
        self.views = {}
        self.nav_buttons = {}
        self.recent_activity = []
        self.waveform_bars = []
        self.template_buttons = {}
        self.project_cards = []
        self.VOICE_MAPPING = VOICE_MAPPING

        self.build_shell()
        self.build_sidebar()
        self.build_topbar()
        self.build_main_views()

        self.show_view("studio")
        self.after(350, self.load_intro)
        self.after(800, lambda: self.add_activity("Workspace initialized."))
        self.after(1000, self.animate_waveform)
        self.after(1000, self.update_clock)

    build_shell = build_shell
    build_sidebar = build_sidebar
    build_topbar = build_topbar

    make_sidebar_stat = make_sidebar_stat
    make_small_metric = make_small_metric
    make_slider_row = make_slider_row
    setting_row = setting_row

    build_studio_view = build_studio_view
    build_projects_view = build_projects_view
    build_media_view = build_media_view
    build_voices_view = build_voices_view
    build_settings_view = build_settings_view

    def build_main_views(self):
        self.view_host = ctk.CTkFrame(self.main, fg_color="transparent")
        self.view_host.grid(row=0, column=0, sticky="nsew", padx=18, pady=18)
        self.view_host.grid_rowconfigure(0, weight=1)
        self.view_host.grid_columnconfigure(0, weight=1)

        self.views["studio"] = self.build_studio_view()
        self.views["projects"] = self.build_projects_view()
        self.views["media"] = self.build_media_view()
        self.views["voices"] = self.build_voices_view()
        self.views["settings"] = self.build_settings_view()

    def show_view(self, name):
        for view in self.views.values():
            view.grid_forget()

        self.views[name].grid(row=0, column=0, sticky="nsew")

        for key, btn in self.nav_buttons.items():
            if key == name:
                btn.configure(fg_color="#4D7FFF", hover_color="#3E6AE0")
            else:
                btn.configure(fg_color="#0D172B", hover_color="#162540")

        self.add_activity(f"Switched to {name.title()} view.")

    def set_status(self, text, color="#67F2AF"):
        self.status_chip.configure(text=text, text_color=color)
        self.side_status.configure(text=text)

        if color == "#67F2AF":
            self.status_chip.configure(fg_color="#10281D")
        elif color == "#FFD16B":
            self.status_chip.configure(fg_color="#31270F")
        elif color == "#FF98AE":
            self.status_chip.configure(fg_color="#351621")
        else:
            self.status_chip.configure(fg_color="#182542")

    def update_clock(self):
        self.clock_label.configure(text=time.strftime("%H:%M:%S"))
        self.after(1000, self.update_clock)

    def animate_waveform(self):
        if self.waveform_bars:
            values = [18, 38, 52, 26, 62, 34, 74, 29, 68, 33, 57, 24]
            t = int(time.time() * 3)
            for i, bar in enumerate(self.waveform_bars):
                new_h = values[(i + t) % len(values)]
                bar.configure(height=new_h)
        self.after(240, self.animate_waveform)

    def add_activity(self, message):
        stamp = time.strftime("%H:%M:%S")
        line = f"[{stamp}] {message}"
        self.recent_activity.append(line)
        if len(self.recent_activity) > 120:
            self.recent_activity.pop(0)

        if hasattr(self, "activity_box") and self.activity_box.winfo_exists():
            self.activity_box.insert("end", line + "\n")
            self.activity_box.see("end")

    def get_media_count(self):
        return len([f for f in os.listdir(MEDIA_FOLDER) if f.lower().endswith(".mp3")])

    def change_voice(self, selected):
        self.current_voice_name = selected
        self.side_voice.configure(text=selected)
        self.add_activity(f"Voice changed to {selected}.")
        self.refresh_voice_lab()

    def select_voice(self, voice_name):
        self.current_voice_name = voice_name
        self.side_voice.configure(text=voice_name)
        if hasattr(self, "voice_selector"):
            self.voice_selector.set(voice_name)
        self.refresh_voice_lab()
        self.add_activity(f"{voice_name} selected in Voice Lab.")
        self.show_view("studio")

    def refresh_voice_lab(self):
        if not hasattr(self, "voice_lab_buttons"):
            return
        for name, btn in self.voice_lab_buttons.items():
            if name == self.current_voice_name:
                btn.configure(text="Selected", fg_color="#4D7FFF", hover_color="#3E6AE0")
            else:
                btn.configure(text="Select Voice", fg_color="#14213D", hover_color="#1C2D4F")

    def load_template_text(self, text):
        self.script_box.delete("1.0", "end")
        self.script_box.insert("1.0", text)
        self.add_activity("Template loaded into script canvas.")
        self.set_status("Template loaded", "#79A8FF")

    def load_project_template(self, title):
        templates = {
            "Brand Launch": "Introducing a new standard in design, performance, and innovation.",
            "Podcast Intro": "Welcome back to the show — today we’re diving into what real growth looks like.",
            "YouTube Narration": "Today we’re breaking down the exact system that changed everything.",
            "Cinematic Trailer": "In a world driven by ambition, one voice rises above the noise.",
            "Course Module": "In this lesson, you’ll learn the principles behind clear, structured execution.",
            "Product Demo": "This product was built to make complex work feel simple and powerful."
        }
        self.show_view("studio")
        self.load_template_text(templates.get(title, "Start writing here..."))
        self.add_activity(f"Project template opened: {title}")

    def open_project_stub(self, title):
        self.add_activity(f"Opened project preview: {title}")
        self.set_status("Project opened", "#79A8FF")

    def clear_script(self):
        self.script_box.delete("1.0", "end")
        self.add_activity("Script cleared.")
        self.set_status("Canvas cleared", "#79A8FF")

    def insert_demo_text(self):
        demo = (
            "Welcome to Ready My Voice.\n\n"
            "This interface is designed for premium narration, powerful marketing reads, "
            "cinematic storytelling, and clean professional voice output. Type your idea, "
            "shape the tone, and generate something that actually sounds expensive."
        )
        self.script_box.delete("1.0", "end")
        self.script_box.insert("1.0", demo)
        self.add_activity("Demo script inserted.")
        self.set_status("Demo loaded", "#79A8FF")

    def handle_enter(self, event=None):
        try:
            command = self.script_box.get("end-2l linestart", "end-1c").strip()
            if command:
                process_command(command, self.script_box)
                self.add_activity(f"Processed command: {command}")
        except Exception as e:
            self.add_activity(f"Command error: {e}")
        return "break"

    def generate_audio(self):
        if self.processing:
            return

        text = self.script_box.get("1.0", "end-1c").strip()
        if not text:
            self.set_status("No script", "#FF98AE")
            self.add_activity("Generate blocked. Script box is empty.")
            return

        voice_id = VOICE_MAPPING.get(self.current_voice_name)

        self.processing = True
        self.set_status("Generating...", "#FFD16B")
        self.add_activity(f"Generating with {self.current_voice_name} voice.")

        try:
            saved = txt_to_speech(text, self.script_box, voice_id)
            if saved:
                self.current_audio_path = saved
                self.side_output.configure(text=Path(saved).name)
                self.set_status("Audio ready", "#67F2AF")
                self.add_activity(f"Audio generated: {Path(saved).name}")
                self.refresh_media_view()

                if hasattr(self, "autoplay_switch") and self.autoplay_switch.get() == 1:
                    self.after(250, self.play_current_audio)
            else:
                self.set_status("Generation failed", "#FF98AE")
                self.add_activity("Generator returned no file.")
        except Exception as e:
            self.set_status("Generation failed", "#FF98AE")
            self.add_activity(f"Generation error: {e}")
        finally:
            self.processing = False

    def play_current_audio(self):
        if not self.current_audio_path:
            self.set_status("No output", "#FF98AE")
            self.add_activity("Preview blocked. No output selected.")
            return
        try:
            play_audio(self.current_audio_path)
            self.set_status("Playing", "#79A8FF")
            self.add_activity(f"Playing {Path(self.current_audio_path).name}.")
        except Exception as e:
            self.set_status("Play failed", "#FF98AE")
            self.add_activity(f"Playback error: {e}")

    def export_current_audio(self):
        if not self.current_audio_path:
            self.set_status("Nothing to export", "#FF98AE")
            self.add_activity("Export blocked. No file selected.")
            return
        try:
            download_file(self.current_audio_path, filedialog, self.script_box)
            self.set_status("Exported", "#67F2AF")
            self.add_activity(f"Exported {Path(self.current_audio_path).name}.")
        except Exception as e:
            self.set_status("Export failed", "#FF98AE")
            self.add_activity(f"Export error: {e}")

    def use_media_file(self, filename):
        self.current_audio_path = os.path.join(MEDIA_FOLDER, filename)
        self.side_output.configure(text=filename)
        self.set_status("Asset selected", "#79A8FF")
        self.add_activity(f"Selected output: {filename}")

    def delete_media_file(self, filename):
        path = os.path.join(MEDIA_FOLDER, filename)
        try:
            if self.current_audio_path == path:
                self.current_audio_path = None
                self.side_output.configure(text="None")
            os.remove(path)
            self.refresh_media_view()
            self.add_activity(f"Deleted media file: {filename}")
            self.set_status("Deleted", "#67F2AF")
        except Exception as e:
            self.set_status("Delete failed", "#FF98AE")
            self.add_activity(f"Delete error: {e}")

    def refresh_media_view(self):
        if not hasattr(self, "media_scroll") or not self.media_scroll.winfo_exists():
            return

        for widget in self.media_scroll.winfo_children():
            widget.destroy()

        files = sorted(
            [f for f in os.listdir(MEDIA_FOLDER) if f.lower().endswith(".mp3")],
            reverse=True
        )

        if not files:
            empty = ctk.CTkFrame(
                self.media_scroll,
                fg_color="#0F1A31",
                corner_radius=20,
                border_width=1,
                border_color="#1D2E52"
            )
            empty.pack(fill="x", padx=14, pady=14)

            ctk.CTkLabel(
                empty,
                text="No audio assets yet",
                font=("Helvetica", 20, "bold"),
                text_color="#FFFFFF"
            ).pack(anchor="w", padx=18, pady=(18, 4))

            ctk.CTkLabel(
                empty,
                text="Generate something in Studio and it will land here.",
                font=("Helvetica", 13),
                text_color="#8EA0C5"
            ).pack(anchor="w", padx=18, pady=(0, 18))
            return

        for filename in files:
            card = ctk.CTkFrame(
                self.media_scroll,
                fg_color="#0F1A31",
                corner_radius=20,
                border_width=1,
                border_color="#1D2E52"
            )
            card.pack(fill="x", padx=14, pady=10)

            left = ctk.CTkFrame(card, fg_color="transparent")
            left.pack(side="left", fill="both", expand=True, padx=16, pady=16)

            ctk.CTkLabel(
                left,
                text="🎧  " + filename,
                font=("Helvetica", 16, "bold"),
                text_color="#FFFFFF"
            ).pack(anchor="w")

            ctk.CTkLabel(
                left,
                text=f"Stored in {MEDIA_FOLDER}",
                font=("Helvetica", 12),
                text_color="#8EA0C5"
            ).pack(anchor="w", pady=(4, 0))

            right = ctk.CTkFrame(card, fg_color="transparent")
            right.pack(side="right", padx=14, pady=14)

            ctk.CTkButton(
                right,
                text="Use",
                width=70,
                height=38,
                corner_radius=12,
                fg_color="#14213D",
                hover_color="#1C2D4F",
                font=("Helvetica", 13, "bold"),
                command=lambda f=filename: self.use_media_file(f)
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                right,
                text="Play",
                width=70,
                height=38,
                corner_radius=12,
                fg_color="#14213D",
                hover_color="#1C2D4F",
                font=("Helvetica", 13, "bold"),
                command=lambda f=filename: play_audio(os.path.join(MEDIA_FOLDER, f))
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                right,
                text="Delete",
                width=76,
                height=38,
                corner_radius=12,
                fg_color="#241420",
                hover_color="#351B2D",
                text_color="#FFB7C3",
                font=("Helvetica", 13, "bold"),
                command=lambda f=filename: self.delete_media_file(f)
            ).pack(side="left", padx=5)

    def change_appearance(self, mode):
        ctk.set_appearance_mode(mode)
        self.add_activity(f"Appearance changed to {mode} mode.")

    def load_intro(self):
        message = (
            "Welcome to Ready My Voice.\n\n"
            "• Start in Studio to write or paste a script.\n"
            "• Choose your voice and tuning profile.\n"
            "• Generate, preview, and export polished audio.\n"
            "• Keep every output in Media Vault.\n"
            "• Explore presets in Voice Lab.\n"
            "• Organize bigger ideas inside Projects."
        )
        intro_txt(message, self.script_box)

        try:
            if hasattr(self, "voice_intro_switch") and self.voice_intro_switch.get() == 1:
                speak_text("Welcome to Ready My Voice.")
        except Exception:
            pass