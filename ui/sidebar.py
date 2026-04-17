import customtkinter as ctk


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
    