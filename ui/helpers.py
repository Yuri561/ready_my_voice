import customtkinter as ctk


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
    return row


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