import customtkinter as ctk


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