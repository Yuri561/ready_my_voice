import customtkinter as ctk


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