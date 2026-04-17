import customtkinter as ctk
from config import VOICE_MAPPING


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