import customtkinter as ctk


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