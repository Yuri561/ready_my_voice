import customtkinter as ctk


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