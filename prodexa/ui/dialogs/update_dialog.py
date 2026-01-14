import tkinter as tk
from tkinter import ttk


class UpdateDialog(tk.Toplevel):
    def __init__(self, master, update_info):
        super().__init__(master)
        self.title("Update Available")
        self.resizable(False, False)

        self.update_info = update_info

        ttk.Label(
            self,
            text=f"Prodexa {update_info['version']} is available",
            font=("TkDefaultFont", 12, "bold")
        ).pack(padx=20, pady=(20, 10))

        ttk.Label(
            self,
            text="A newer version of Prodexa is available.\nWould you like to download it now?"
        ).pack(padx=20, pady=10)

        btns = ttk.Frame(self)
        btns.pack(pady=(0, 20))

        ttk.Button(btns, text="Later", command=self.destroy).pack(
            side="left", padx=5
        )

        ttk.Button(
            btns,
            text="Download",
            command=self.download
        ).pack(side="left", padx=5)

    def download(self):
        import prodexa.infrastructure.updater as updater
        updater.open_download(self.update_info["url"])
        self.destroy()
