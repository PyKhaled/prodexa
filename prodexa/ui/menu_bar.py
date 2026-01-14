import tkinter as tk
from tkinter import messagebox

from prodexa.ui.dialogs.about_dialog import AboutDialog
from prodexa.ui.dialogs.update_dialog import UpdateDialog
from prodexa.infrastructure.updater import check_for_update


class MenuBar(tk.Menu):
    def __init__(self, root: tk.Tk):
        super().__init__(root)
        self.root = root

        self._build_help_menu()
        root.config(menu=self)

    def _build_help_menu(self):
        help_menu = tk.Menu(self, tearoff=False)

        help_menu.add_command(
            label="Check for Updates",
            command=self.check_updates
        )

        help_menu.add_separator()

        help_menu.add_command(
            label="About Prodexa",
            command=self.show_about
        )

        self.add_cascade(label="Help", menu=help_menu)

    # ─────────────────────────────
    # Actions
    # ─────────────────────────────

    def show_about(self):
        AboutDialog(self.root)

    def check_updates(self):
        update = check_for_update()
        if update:
            UpdateDialog(self.root, update)
        else:
            messagebox.showinfo(
                "No Updates",
                "You are already using the latest version of Prodexa."
            )