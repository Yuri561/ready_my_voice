import customtkinter as ctk


def build_studio_view(self):
    frame = ctk.CTkFrame(self.view_host, fg_color="transparent")
    frame.grid_columnconfigure(0, weight=4)
    frame.grid_columnconfigure(1, weight=2)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_rowconfigure(2, weight=1)

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
        values=list(self.VOICE_MAPPING.keys()) if hasattr(self, "VOICE_MAPPING") else ["Laura", "Saarah", "Roger", "Charlie", "George"],
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