import tkinter as tk

from prodexa.ui.main_window import MainWindow
from prodexa.ui.menu_bar import MenuBar
from prodexa.infrastructure.updater import check_for_update
from prodexa.ui.dialogs.update_dialog import UpdateDialog


def run_app() -> None:
    root = tk.Tk()
    root.title("Prodexa")
    root.geometry("900x600")
    root.minsize(800, 500)

    # Improve appearance on Windows
    try:
        root.tk.call("tk", "scaling", 1.2)
    except Exception:
        pass

    # Menu bar
    MenuBar(root)

    MainWindow(root)

    # Background update check
    root.after(1500, lambda: _check_updates(root))

    root.mainloop()


def _check_updates(root: tk.Tk) -> None:
    try:
        update = check_for_update()
        if update:
            UpdateDialog(root, update)
    except Exception:
        # Never crash UI due to network issues
        pass