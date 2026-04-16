import customtkinter as ctk
from tkinter import filedialog
import os
import time
from pathlib import Path

# =========================================================
# OPTIONAL PROJECT IMPORTS
# Falls back gracefully so the UI can run even without logic
# =========================================================
try:
    from utils.download_file import download_file
except Exception:
    def download_file(file_path, filedialog_module, text_widget=None):
        if not file_path:
            return
        save_path = filedialog_module.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("MP3 Files", "*.mp3"), ("All Files", "*.*")]
        )
        if save_path:
            try:
                with open(file_path, "rb") as src, open(save_path, "wb") as dst:
                    dst.write(src.read())
            except Exception as e:
                print(f"Download failed: {e}")

try:
    from utils.intro_txt import intro_txt, process_command
except Exception:
    def intro_txt(message, textbox):
        textbox.delete("1.0", "end")
        textbox.insert("1.0", message)

    def process_command(command, textbox):
        textbox.insert("end", f"\n\n[Command received] {command}")

try:
    from utils.voice_api import txt_to_speech, speak_text
except Exception:
    def txt_to_speech(text, textbox, voice_id):
        os.makedirs("audio_files", exist_ok=True)
        fake_path = os.path.join("audio_files", "sample_output.mp3")
        if not os.path.exists(fake_path):
            with open(fake_path, "wb") as f:
                f.write(b"")
        return fake_path

    def speak_text(text):
        print(f"Speaking: {text}")

try:
    from audio_files.audio_script import play_audio
except Exception:
    def play_audio(file_path):
        print(f"Playing: {file_path}")


# =========================================================
# CONFIG
# =========================================================
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
    "George": "JBFqnCBsd6RMkjVDRZzb"
}


# =========================================================
# APP
# =========================================================
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

        self.build_shell()
        self.build_sidebar()
        self.build_topbar()
        self.build_main_views()

        self.show_view("studio")
        self.after(350, self.load_intro)
        self.after(800, lambda: self.add_activity("Workspace initialized."))
        self.after(1000, self.animate_waveform)
        self.after(1000, self.update_clock)

    # =====================================================
    # SHELL
    # =====================================================
    def build_shell(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.sidebar = ctk.CTkFrame(
            self,
            width=260,
            corner_radius=0,
            fg_color="#08101F",
            border_width=1,
            border_color="#16233E"
        )
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.topbar = ctk.CTkFrame(
            self,
            height=82,
            corner_radius=0,
            fg_color="#070D1A",
            border_width=1,
            border_color="#16233E"
        )
        self.topbar.grid(row=0, column=1, sticky="nsew")

        self.main = ctk.CTkFrame(
            self,
            fg_color="#050816",
            corner_radius=0
        )
        self.main.grid(row=1, column=1, sticky="nsew")
        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_columnconfigure(0, weight=1)

    def build_sidebar(self):
        brand = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand.pack(fill="x", padx=18, pady=(18, 12))

        ctk.CTkLabel(
            brand,
            text="READY MY",
            font=("Helvetica", 28, "bold"),
            text_color="#F6F8FF"
        ).pack(anchor="w")

        ctk.CTkLabel(
            brand,
            text="VOICE",
            font=("Helvetica", 32, "bold"),
            text_color="#79A8FF"
        ).pack(anchor="w")

        ctk.CTkLabel(
            brand,
            text="Premium AI voice workspace",
            font=("Helvetica", 12),
            text_color="#8495BA"
        ).pack(anchor="w", pady=(6, 0))

        nav = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav.pack(fill="x", padx=14, pady=(10, 8))

        items = [
            ("studio", "🎙  Studio"),
            ("projects", "🗂  Projects"),
            ("media", "🎧  Media Vault"),
            ("voices", "🧠  Voice Lab"),
            ("settings", "⚙️  Settings"),
        ]

        for key, label in items:
            btn = ctk.CTkButton(
                nav,
                text=label,
                anchor="w",
                height=46,
                corner_radius=14,
                fg_color="#0D172B",
                hover_color="#162540",
                text_color="#E4EBFF",
                font=("Helvetica", 15, "bold"),
                command=lambda k=key: self.show_view(k)
            )
            btn.pack(fill="x", pady=6)
            self.nav_buttons[key] = btn

        quick = ctk.CTkFrame(
            self.sidebar,
            fg_color="#0D172B",
            corner_radius=20,
            border_width=1,
            border_color="#1D2E51"
        )
        quick.pack(fill="x", padx=16, pady=(18, 10))

        ctk.CTkLabel(
            quick,
            text="Quick Launch",
            font=("Helvetica", 16, "bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w", padx=14, pady=(14, 8))

        ctk.CTkButton(
            quick,
            text="⚡ Generate",
            height=42,
            corner_radius=12,
            fg_color="#4D7FFF",
            hover_color="#3E6AE0",
            font=("Helvetica", 14, "bold"),
            command=self.generate_audio
        ).pack(fill="x", padx=12, pady=6)

        ctk.CTkButton(
            quick,
            text="▶ Preview",
            height=42,
            corner_radius=12,
            fg_color="#13203B",
            hover_color="#1B2D50",
            font=("Helvetica", 14, "bold"),
            command=self.play_current_audio
        ).pack(fill="x", padx=12, pady=6)

        ctk.CTkButton(
            quick,
            text="⬇ Export",
            height=42,
            corner_radius=12,
            fg_color="#13203B",
            hover_color="#1B2D50",
            font=("Helvetica", 14, "bold"),
            command=self.export_current_audio
        ).pack(fill="x", padx=12, pady=(6, 14))

        insight = ctk.CTkFrame(
            self.sidebar,
            fg_color="#0B1426",
            corner_radius=20,
            border_width=1,
            border_color="#1A2A47"
        )
        insight.pack(fill="x", padx=16, pady=(6, 10))

        ctk.CTkLabel(
            insight,
            text="Live Snapshot",
            font=("Helvetica", 16, "bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w", padx=14, pady=(14, 8))

        self.side_voice = self.make_sidebar_stat(insight, "Selected Voice", self.current_voice_name)
        self.side_status = self.make_sidebar_stat(insight, "Engine", "Ready")
        self.side_output = self.make_sidebar_stat(insight, "Output", "None")

        ctk.CTkLabel(
            self.sidebar,
            text="Craft narration, ads, intros, and cinematic reads\nfrom one premium workspace.",
            justify="left",
            font=("Helvetica", 12),
            text_color="#7E8FB3"
        ).pack(anchor="w", padx=20, pady=(8, 0))

        bottom = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        bottom.pack(side="bottom", fill="x", padx=16, pady=16)

        ctk.CTkButton(
            bottom,
            text="✕ Exit",
            height=44,
            corner_radius=14,
            fg_color="#211224",
            hover_color="#321A37",
            text_color="#FFB7C3",
            font=("Helvetica", 14, "bold"),
            command=self.destroy
        ).pack(fill="x")

    def build_topbar(self):
        self.topbar.grid_columnconfigure(0, weight=1)

        left = ctk.CTkFrame(self.topbar, fg_color="transparent")
        left.grid(row=0, column=0, sticky="w", padx=24, pady=14)

        ctk.CTkLabel(
            left,
            text="Ready My Voice",
            font=("Helvetica", 26, "bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w")

        ctk.CTkLabel(
            left,
            text="A flagship interface for premium voice creation.",
            font=("Helvetica", 12),
            text_color="#8696BA"
        ).pack(anchor="w", pady=(2, 0))

        right = ctk.CTkFrame(self.topbar, fg_color="transparent")
        right.grid(row=0, column=1, sticky="e", padx=24, pady=14)

        self.clock_label = ctk.CTkLabel(
            right,
            text="--:--:--",
            font=("Helvetica", 13, "bold"),
            text_color="#AAB5D0"
        )
        self.clock_label.pack(side="right", padx=(10, 0))

        self.status_chip = ctk.CTkLabel(
            right,
            text="Ready",
            width=120,
            height=34,
            corner_radius=999,
            fg_color="#10281D",
            text_color="#67F2AF",
            font=("Helvetica", 13, "bold")
        )
        self.status_chip.pack(side="right")

    def make_sidebar_stat(self, parent, title, value):
        box = ctk.CTkFrame(parent, fg_color="#101D36", corner_radius=12)
        box.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            box,
            text=title,
            font=("Helvetica", 11),
            text_color="#8193B7"
        ).pack(anchor="w", padx=10, pady=(8, 0))

        val = ctk.CTkLabel(
            box,
            text=value,
            font=("Helvetica", 14, "bold"),
            text_color="#F5F8FF"
        )
        val.pack(anchor="w", padx=10, pady=(2, 8))
        return val

    # =====================================================
    # VIEWS
    # =====================================================
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

    def build_studio_view(self):
        frame = ctk.CTkFrame(self.view_host, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=4)
        frame.grid_columnconfigure(1, weight=2)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)

        # HERO
        hero = ctk.CTkFrame(
            frame,
            fg_color="#0A1327",
            corner_radius=28,
            border_width=1,
            border_color="#18284A"
        )
        hero.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 16))
        hero.grid_columnconfigure(0, weight=3)
        hero.grid_columnconfigure(1, weight=2)

        hero_left = ctk.CTkFrame(hero, fg_color="transparent")
        hero_left.grid(row=0, column=0, sticky="nsew", padx=22, pady=22)

        ctk.CTkLabel(
            hero_left,
            text="Build voice that feels expensive.",
            font=("Helvetica", 34, "bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w")

        ctk.CTkLabel(
            hero_left,
            text="Write, shape, preview, and manage your entire audio workflow in one cinematic workspace.",
            font=("Helvetica", 14),
            text_color="#8FA1C7",
            wraplength=620,
            justify="left"
        ).pack(anchor="w", pady=(8, 16))

        hero_actions = ctk.CTkFrame(hero_left, fg_color="transparent")
        hero_actions.pack(anchor="w")

        ctk.CTkButton(
            hero_actions,
            text="⚡ Generate Now",
            height=46,
            width=170,
            corner_radius=14,
            fg_color="#4D7FFF",
            hover_color="#3E6AE0",
            font=("Helvetica", 14, "bold"),
            command=self.generate_audio
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            hero_actions,
            text="🎧 Open Vault",
            height=46,
            width=150,
            corner_radius=14,
            fg_color="#14213D",
            hover_color="#1C2D4F",
            font=("Helvetica", 14, "bold"),
            command=lambda: self.show_view("media")
        ).pack(side="left")

        hero_right = ctk.CTkFrame(
            hero,
            fg_color="#0E1A33",
            corner_radius=22,
            border_width=1,
            border_color="#1C2D50"
        )
        hero_right.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)

        ctk.CTkLabel(
            hero_right,
            text="Live Stage",
            font=("Helvetica", 18, "bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w", padx=16, pady=(16, 4))

        ctk.CTkLabel(
            hero_right,
            text="Animated visualizer zone",
            font=("Helvetica", 12),
            text_color="#8EA0C5"
        ).pack(anchor="w", padx=16, pady=(0, 10))

        self.wave_wrap = ctk.CTkFrame(hero_right, fg_color="#0A1327", corner_radius=18)
        self.wave_wrap.pack(fill="x", padx=16, pady=(0, 14), ipady=18)

        bars = ctk.CTkFrame(self.wave_wrap, fg_color="transparent")
        bars.pack(expand=True)

        self.waveform_bars.clear()
        default_heights = [20, 35, 50, 28, 60, 40, 72, 38, 65, 30, 55, 25]
        for h in default_heights:
            bar = ctk.CTkFrame(
                bars,
                width=10,
                height=h,
                corner_radius=6,
                fg_color="#75A3FF"
            )
            bar.pack(side="left", padx=4, pady=6)
            self.waveform_bars.append(bar)

        stats_row = ctk.CTkFrame(hero_right, fg_color="transparent")
        stats_row.pack(fill="x", padx=16, pady=(0, 16))

        self.make_small_metric(stats_row, "Voice", self.current_voice_name).pack(side="left", padx=(0, 8))
        self.make_small_metric(stats_row, "Outputs", str(self.get_media_count())).pack(side="left", padx=8)
        self.make_small_metric(stats_row, "Mode", "Studio").pack(side="left", padx=8)

        # LEFT COLUMN BIG EDITOR
        editor_panel = ctk.CTkFrame(
            frame,
            fg_color="#0A1122",
            corner_radius=24,
            border_width=1,
            border_color="#18284A"
        )
        editor_panel.grid(row=1, column=0, rowspan=2, sticky="nsew", padx=(0, 10))

        editor_panel.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(
            editor_panel,
            text="Script Canvas",
            font=("Helvetica", 24, "bold"),
            text_color="#FFFFFF"
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(18, 4))

        ctk.CTkLabel(
            editor_panel,
            text="Turn raw ideas into polished narration, ads, intros, and dramatic reads.",
            font=("Helvetica", 13),
            text_color="#8496BC"
        ).grid(row=1, column=0, sticky="w", padx=20, pady=(0, 12))

        tool_row = ctk.CTkFrame(editor_panel, fg_color="transparent")
        tool_row.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 12))

        self.voice_selector = ctk.CTkComboBox(
            tool_row,
            values=list(VOICE_MAPPING.keys()),
            width=180,
            height=42,
            corner_radius=12,
            fg_color="#111C35",
            border_color="#21345B",
            button_color="#4D7FFF",
            button_hover_color="#3E6AE0",
            command=self.change_voice
        )
        self.voice_selector.set(self.current_voice_name)
        self.voice_selector.pack(side="left", padx=(0, 10))

        self.mode_selector = ctk.CTkSegmentedButton(
            tool_row,
            values=["Standard", "Story", "Ad", "Cinematic"],
            height=40,
            corner_radius=12,
            fg_color="#111C35",
            selected_color="#4D7FFF",
            selected_hover_color="#3E6AE0",
            unselected_color="#111C35",
            unselected_hover_color="#162542"
        )
        self.mode_selector.set("Standard")
        self.mode_selector.pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            tool_row,
            text="Insert Demo",
            height=42,
            corner_radius=12,
            fg_color="#14213D",
            hover_color="#1C2D4F",
            font=("Helvetica", 13, "bold"),
            command=self.insert_demo_text
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            tool_row,
            text="Clear",
            height=42,
            corner_radius=12,
            fg_color="#14213D",
            hover_color="#1C2D4F",
            font=("Helvetica", 13, "bold"),
            command=self.clear_script
        ).pack(side="left")

        self.script_box = ctk.CTkTextbox(
            editor_panel,
            fg_color="#08101E",
            border_width=1,
            border_color="#1A2A4A",
            corner_radius=18,
            text_color="#E8EEFF",
            font=("Helvetica", 15)
        )
        self.script_box.grid(row=3, column=0, sticky="nsew", padx=18, pady=(0, 18))
        self.script_box.bind("<Return>", self.handle_enter)

        # RIGHT TOP CONTROLS
        controls_panel = ctk.CTkFrame(
            frame,
            fg_color="#0A1122",
            corner_radius=24,
            border_width=1,
            border_color="#18284A"
        )
        controls_panel.grid(row=1, column=1, sticky="nsew", padx=(10, 0), pady=(0, 10))

        ctk.CTkLabel(
            controls_panel,
            text="Voice Tuning",
            font=("Helvetica", 22, "bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w", padx=18, pady=(18, 10))

        self.make_slider_row(controls_panel, "Stability", 0.74)
        self.make_slider_row(controls_panel, "Warmth", 0.62)
        self.make_slider_row(controls_panel, "Clarity", 0.86)
        self.make_slider_row(controls_panel, "Energy", 0.55)

        action_box = ctk.CTkFrame(
            controls_panel,
            fg_color="#101A31",
            corner_radius=18,
            border_width=1,
            border_color="#1C2D50"
        )
        action_box.pack(fill="x", padx=16, pady=(8, 16))

        ctk.CTkButton(
            action_box,
            text="⚡ Generate Audio",
            height=48,
            corner_radius=14,
            fg_color="#4D7FFF",
            hover_color="#3E6AE0",
            font=("Helvetica", 15, "bold"),
            command=self.generate_audio
        ).pack(fill="x", padx=14, pady=(14, 8))

        button_row = ctk.CTkFrame(action_box, fg_color="transparent")
        button_row.pack(fill="x", padx=14, pady=(0, 14))

        ctk.CTkButton(
            button_row,
            text="▶ Preview",
            height=42,
            corner_radius=12,
            fg_color="#14213D",
            hover_color="#1C2D4F",
            font=("Helvetica", 13, "bold"),
            command=self.play_current_audio
        ).pack(side="left", fill="x", expand=True, padx=(0, 6))

        ctk.CTkButton(
            button_row,
            text="⬇ Export",
            height=42,
            corner_radius=12,
            fg_color="#14213D",
            hover_color="#1C2D4F",
            font=("Helvetica", 13, "bold"),
            command=self.export_current_audio
        ).pack(side="left", fill="x", expand=True, padx=(6, 0))

        # RIGHT BOTTOM FEED + TEMPLATES
        lower_right = ctk.CTkFrame(
            frame,
            fg_color="#0A1122",
            corner_radius=24,
            border_width=1,
            border_color="#18284A"
        )
        lower_right.grid(row=2, column=1, sticky="nsew", padx=(10, 0), pady=(10, 0))
        lower_right.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            lower_right,
            text="Prompt Starters",
            font=("Helvetica", 20, "bold"),
            text_color="#FFFFFF"
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(18, 10))

        template_row = ctk.CTkFrame(lower_right, fg_color="transparent")
        template_row.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 12))

        templates = {
            "Ad": "Introducing the future of sound. Clean, bold, unforgettable.",
            "Narration": "In a world shaped by innovation, every voice carries a story.",
            "YouTube": "What’s up everybody, welcome back — today we’re taking this to the next level.",
            "Podcast": "Welcome back to the show. Today we’re diving into the mindset behind growth."
        }

        for name, text in templates.items():
            btn = ctk.CTkButton(
                template_row,
                text=name,
                height=38,
                corner_radius=12,
                fg_color="#14213D",
                hover_color="#1C2D4F",
                font=("Helvetica", 12, "bold"),
                command=lambda t=text: self.load_template_text(t)
            )
            btn.pack(side="left", padx=4, expand=True, fill="x")

        ctk.CTkLabel(
            lower_right,
            text="System Feed",
            font=("Helvetica", 16, "bold"),
            text_color="#FFFFFF"
        ).grid(row=2, column=0, sticky="w", padx=18, pady=(0, 6))

        self.activity_box = ctk.CTkTextbox(
            lower_right,
            fg_color="#08101E",
            border_width=1,
            border_color="#1A2A4A",
            corner_radius=16,
            text_color="#DBE5FF",
            font=("Consolas", 13)
        )
        self.activity_box.grid(row=3, column=0, sticky="nsew", padx=16, pady=(0, 16))

        return frame

    def build_projects_view(self):
        frame = ctk.CTkFrame(self.view_host, fg_color="transparent")
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(
            frame,
            fg_color="#0A1122",
            corner_radius=24,
            border_width=1,
            border_color="#18284A"
        )
        header.grid(row=0, column=0, sticky="ew", pady=(0, 16))

        ctk.CTkLabel(
            header,
            text="Projects",
            font=("Helvetica", 26, "bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w", padx=20, pady=(18, 4))

        ctk.CTkLabel(
            header,
            text="A visual home for your scripts, ads, episode drafts, brand voice kits, and launches.",
            font=("Helvetica", 13),
            text_color="#8799BF"
        ).pack(anchor="w", padx=20, pady=(0, 16))

        body = ctk.CTkScrollableFrame(
            frame,
            fg_color="#0A1122",
            corner_radius=24,
            border_width=1,
            border_color="#18284A"
        )
        body.grid(row=1, column=0, sticky="nsew")

        sample_projects = [
            ("Brand Launch", "Commercial voice package", "12 assets"),
            ("Podcast Intro", "Warm host opening", "4 assets"),
            ("YouTube Narration", "Explainer project", "9 assets"),
            ("Cinematic Trailer", "High-drama voice direction", "3 assets"),
            ("Course Module", "Educational narration", "16 assets"),
            ("Product Demo", "Tech voice presentation", "7 assets"),
        ]

        grid = ctk.CTkFrame(body, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=8, pady=8)
        grid.grid_columnconfigure((0, 1, 2), weight=1)

        row = 0
        col = 0
        for title, subtitle, count in sample_projects:
            card = ctk.CTkFrame(
                grid,
                fg_color="#0F1A31",
                corner_radius=20,
                border_width=1,
                border_color="#1D2E52"
            )
            card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)

            ctk.CTkLabel(
                card,
                text=title,
                font=("Helvetica", 18, "bold"),
                text_color="#FFFFFF"
            ).pack(anchor="w", padx=16, pady=(16, 4))

            ctk.CTkLabel(
                card,
                text=subtitle,
                font=("Helvetica", 12),
                text_color="#8EA0C5"
            ).pack(anchor="w", padx=16)

            ctk.CTkLabel(
                card,
                text=count,
                font=("Helvetica", 12, "bold"),
                text_color="#79A8FF"
            ).pack(anchor="w", padx=16, pady=(8, 14))

            row_btns = ctk.CTkFrame(card, fg_color="transparent")
            row_btns.pack(fill="x", padx=14, pady=(0, 14))

            ctk.CTkButton(
                row_btns,
                text="Open",
                height=38,
                corner_radius=12,
                fg_color="#4D7FFF",
                hover_color="#3E6AE0",
                font=("Helvetica", 13, "bold"),
                command=lambda t=title: self.open_project_stub(t)
            ).pack(side="left", fill="x", expand=True, padx=(0, 5))

            ctk.CTkButton(
                row_btns,
                text="Use Template",
                height=38,
                corner_radius=12,
                fg_color="#14213D",
                hover_color="#1C2D4F",
                font=("Helvetica", 13, "bold"),
                command=lambda t=title: self.load_project_template(t)
            ).pack(side="left", fill="x", expand=True, padx=(5, 0))

            col += 1
            if col > 2:
                col = 0
                row += 1

        return frame

    def build_media_view(self):
        frame = ctk.CTkFrame(self.view_host, fg_color="transparent")
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(
            frame,
            fg_color="#0A1122",
            corner_radius=24,
            border_width=1,
            border_color="#18284A"
        )
        header.grid(row=0, column=0, sticky="ew", pady=(0, 16))

        ctk.CTkLabel(
            header,
            text="Media Vault",
            font=("Helvetica", 26, "bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w", padx=20, pady=(18, 4))

        ctk.CTkLabel(
            header,
            text="Your outputs live here like polished studio assets.",
            font=("Helvetica", 13),
            text_color="#8799BF"
        ).pack(anchor="w", padx=20, pady=(0, 12))

        actions = ctk.CTkFrame(header, fg_color="transparent")
        actions.pack(fill="x", padx=18, pady=(0, 16))

        ctk.CTkButton(
            actions,
            text="Refresh",
            height=40,
            corner_radius=12,
            fg_color="#14213D",
            hover_color="#1C2D4F",
            font=("Helvetica", 13, "bold"),
            command=self.refresh_media_view
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            actions,
            text="Back to Studio",
            height=40,
            corner_radius=12,
            fg_color="#4D7FFF",
            hover_color="#3E6AE0",
            font=("Helvetica", 13, "bold"),
            command=lambda: self.show_view("studio")
        ).pack(side="left")

        self.media_scroll = ctk.CTkScrollableFrame(
            frame,
            fg_color="#0A1122",
            corner_radius=24,
            border_width=1,
            border_color="#18284A"
        )
        self.media_scroll.grid(row=1, column=0, sticky="nsew")

        self.refresh_media_view()
        return frame

    def build_voices_view(self):
        frame = ctk.CTkFrame(self.view_host, fg_color="transparent")
        frame.grid_columnconfigure((0, 1), weight=1)

        left = ctk.CTkFrame(
            frame,
            fg_color="#0A1122",
            corner_radius=24,
            border_width=1,
            border_color="#18284A"
        )
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        right = ctk.CTkFrame(
            frame,
            fg_color="#0A1122",
            corner_radius=24,
            border_width=1,
            border_color="#18284A"
        )
        right.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(
            left,
            text="Voice Lab",
            font=("Helvetica", 26, "bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w", padx=20, pady=(18, 8))

        ctk.CTkLabel(
            left,
            text="Choose the personality before you hit generate.",
            font=("Helvetica", 13),
            text_color="#8799BF"
        ).pack(anchor="w", padx=20, pady=(0, 14))

        voice_meta = {
            "Laura": "Balanced / modern / premium",
            "Saarah": "Soft / elegant / clean",
            "Roger": "Deep / strong / corporate",
            "Charlie": "Bright / quick / friendly",
            "George": "Calm / mature / narrative"
        }

        grid = ctk.CTkFrame(left, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        grid.grid_columnconfigure((0, 1), weight=1)

        self.voice_lab_buttons = {}
        row = 0
        col = 0
        for name in VOICE_MAPPING:
            card = ctk.CTkFrame(
                grid,
                fg_color="#0F1A31",
                corner_radius=20,
                border_width=1,
                border_color="#1D2E52"
            )
            card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)

            ctk.CTkLabel(
                card,
                text=name,
                font=("Helvetica", 18, "bold"),
                text_color="#FFFFFF"
            ).pack(anchor="w", padx=16, pady=(16, 4))

            ctk.CTkLabel(
                card,
                text=voice_meta.get(name, "Voice profile"),
                font=("Helvetica", 12),
                text_color="#8EA0C5"
            ).pack(anchor="w", padx=16)

            btn = ctk.CTkButton(
                card,
                text="Select Voice",
                height=40,
                corner_radius=12,
                fg_color="#14213D",
                hover_color="#1C2D4F",
                font=("Helvetica", 13, "bold"),
                command=lambda n=name: self.select_voice(n)
            )
            btn.pack(fill="x", padx=14, pady=14)
            self.voice_lab_buttons[name] = btn

            col += 1
            if col > 1:
                col = 0
                row += 1

        ctk.CTkLabel(
            right,
            text="Character Builder",
            font=("Helvetica", 26, "bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w", padx=20, pady=(18, 10))

        self.make_slider_row(right, "Warmth", 0.66)
        self.make_slider_row(right, "Depth", 0.77)
        self.make_slider_row(right, "Brightness", 0.48)
        self.make_slider_row(right, "Breath", 0.24)
        self.make_slider_row(right, "Presence", 0.80)

        ctk.CTkLabel(
            right,
            text="Voice Mood",
            font=("Helvetica", 14, "bold"),
            text_color="#DCE5FF"
        ).pack(anchor="w", padx=18, pady=(12, 8))

        self.voice_mood = ctk.CTkSegmentedButton(
            right,
            values=["Luxury", "Tech", "Cinema", "Friendly"],
            height=42,
            corner_radius=12,
            fg_color="#111C35",
            selected_color="#4D7FFF",
            selected_hover_color="#3E6AE0",
            unselected_color="#111C35",
            unselected_hover_color="#162542"
        )
        self.voice_mood.set("Tech")
        self.voice_mood.pack(fill="x", padx=18, pady=(0, 18))

        ctk.CTkButton(
            right,
            text="Use In Studio",
            height=46,
            corner_radius=14,
            fg_color="#4D7FFF",
            hover_color="#3E6AE0",
            font=("Helvetica", 14, "bold"),
            command=lambda: self.show_view("studio")
        ).pack(fill="x", padx=18, pady=(0, 18))

        self.refresh_voice_lab()
        return frame

    def build_settings_view(self):
        frame = ctk.CTkFrame(self.view_host, fg_color="transparent")
        frame.grid_columnconfigure((0, 1), weight=1)

        left = ctk.CTkFrame(
            frame,
            fg_color="#0A1122",
            corner_radius=24,
            border_width=1,
            border_color="#18284A"
        )
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        right = ctk.CTkFrame(
            frame,
            fg_color="#0A1122",
            corner_radius=24,
            border_width=1,
            border_color="#18284A"
        )
        right.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(
            left,
            text="Workspace Settings",
            font=("Helvetica", 26, "bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w", padx=20, pady=(18, 10))

        self.appearance_menu = ctk.CTkOptionMenu(
            left,
            values=["dark", "light", "system"],
            command=self.change_appearance
        )
        self.appearance_menu.set("dark")
        self.setting_row(left, "Appearance", self.appearance_menu)

        self.autoplay_switch = ctk.CTkSwitch(left, text="")
        self.autoplay_switch.select()
        self.setting_row(left, "Autoplay After Generate", self.autoplay_switch)

        self.voice_intro_switch = ctk.CTkSwitch(left, text="")
        self.voice_intro_switch.select()
        self.setting_row(left, "Spoken Intro", self.voice_intro_switch)

        self.startup_entry = ctk.CTkEntry(left, placeholder_text="Optional startup command...")
        self.setting_row(left, "Startup Prompt", self.startup_entry)

        ctk.CTkButton(
            left,
            text="Save Preferences",
            height=44,
            corner_radius=14,
            fg_color="#4D7FFF",
            hover_color="#3E6AE0",
            font=("Helvetica", 14, "bold"),
            command=lambda: self.add_activity("Preferences saved.")
        ).pack(fill="x", padx=18, pady=16)

        ctk.CTkLabel(
            right,
            text="About This Interface",
            font=("Helvetica", 26, "bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w", padx=20, pady=(18, 10))

        about = ctk.CTkTextbox(
            right,
            fg_color="#08101E",
            border_width=1,
            border_color="#1A2A4A",
            corner_radius=16,
            text_color="#DCE5FF",
            font=("Helvetica", 14)
        )
        about.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        about.insert(
            "1.0",
            "Ready My Voice\n\n"
            "This version is designed like a premium product UI:\n"
            "• cinematic hero stage\n"
            "• live waveform zone\n"
            "• script canvas\n"
            "• voice tuning controls\n"
            "• projects hub\n"
            "• media vault\n"
            "• voice lab\n\n"
            "You can keep evolving this into a real commercial-grade voice studio with project saving, waveform syncing, user accounts, cloud storage, or script intelligence."
        )
        about.configure(state="disabled")

        return frame

    # =====================================================
    # UI HELPERS
    # =====================================================
    def make_small_metric(self, parent, title, value):
        box = ctk.CTkFrame(
            parent,
            fg_color="#111C35",
            corner_radius=14,
            border_width=1,
            border_color="#21345B"
        )
        wrap = ctk.CTkFrame(box, fg_color="transparent")
        wrap.pack(padx=12, pady=10)

        ctk.CTkLabel(
            wrap,
            text=title,
            font=("Helvetica", 11),
            text_color="#8497BC"
        ).pack(anchor="w")

        ctk.CTkLabel(
            wrap,
            text=value,
            font=("Helvetica", 16, "bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w")
        return box

    def make_slider_row(self, parent, label, default):
        row = ctk.CTkFrame(
            parent,
            fg_color="#101A31",
            corner_radius=16,
            border_width=1,
            border_color="#1C2D50"
        )
        row.pack(fill="x", padx=16, pady=7)

        top = ctk.CTkFrame(row, fg_color="transparent")
        top.pack(fill="x", padx=12, pady=(10, 4))

        value_label = ctk.CTkLabel(
            top,
            text=f"{int(default * 100)}%",
            font=("Helvetica", 12, "bold"),
            text_color="#AAB8D8"
        )
        value_label.pack(side="right")

        ctk.CTkLabel(
            top,
            text=label,
            font=("Helvetica", 13, "bold"),
            text_color="#E5ECFF"
        ).pack(side="left")

        slider = ctk.CTkSlider(
            row,
            from_=0,
            to=1,
            number_of_steps=100,
            progress_color="#4D7FFF",
            button_color="#8CB1FF",
            button_hover_color="#9BB9FF"
        )
        slider.pack(fill="x", padx=12, pady=(0, 12))
        slider.set(default)

        def update_value(v):
            value_label.configure(text=f"{int(float(v) * 100)}%")
        slider.configure(command=update_value)

    def setting_row(self, parent, title, widget):
        row = ctk.CTkFrame(
            parent,
            fg_color="#101A31",
            corner_radius=16,
            border_width=1,
            border_color="#1C2D50"
        )
        row.pack(fill="x", padx=18, pady=8)

        ctk.CTkLabel(
            row,
            text=title,
            font=("Helvetica", 13, "bold"),
            text_color="#E5ECFF"
        ).pack(side="left", padx=12, pady=12)

        widget.pack(in_=row, side="right", padx=12, pady=10)

    # =====================================================
    # STATE / BEHAVIOR
    # =====================================================
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


if __name__ == "__main__":
    app = ReadyMyVoiceApp()
    app.mainloop()