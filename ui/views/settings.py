import customtkinter as ctk


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