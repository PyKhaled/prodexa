import tkinter as tk
from tkinter import ttk
from prodexa.__version__ import __version__


class AboutDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("About Prodexa")
        self.resizable(False, False)

        ttk.Label(
            self,
            text="Prodexa",
            font=("TkDefaultFont", 14, "bold")
        ).pack(padx=20, pady=(20, 5))

        ttk.Label(
            self,
            text=f"Version {__version__}"
        ).pack(pady=5)

        ttk.Label(
            self,
            text="Open-source product intelligence tool"
        ).pack(pady=(0, 20))

        ttk.Button(self, text="Close", command=self.destroy).pack(pady=(0, 20))