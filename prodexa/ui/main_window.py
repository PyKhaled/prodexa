import tkinter as tk
from tkinter import ttk


class MainWindow(ttk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.create_header()
        self.create_url_input()
        self.create_tabs()
        self.create_status_bar()

    # ─────────────────────────────
    # Header
    # ─────────────────────────────
    def create_header(self) -> None:
        header = ttk.Frame(self)
        header.pack(fill="x", padx=12, pady=(12, 6))

        title = ttk.Label(
            header,
            text="Prodexa",
            font=("TkDefaultFont", 16, "bold")
        )
        title.pack(side="left")

        subtitle = ttk.Label(
            header,
            text="Product intelligence made simple",
            foreground="gray"
        )
        subtitle.pack(side="left", padx=(10, 0))

    # ─────────────────────────────
    # URL Input
    # ─────────────────────────────
    def create_url_input(self) -> None:
        bar = ttk.Frame(self)
        bar.pack(fill="x", padx=12, pady=6)

        ttk.Label(bar, text="Product URL").pack(side="left")

        self.url_entry = ttk.Entry(bar)
        self.url_entry.pack(side="left", fill="x", expand=True, padx=8)

        extract_btn = ttk.Button(
            bar,
            text="Extract",
            command=self.on_extract
        )
        extract_btn.pack(side="left")

    # ─────────────────────────────
    # Tabs
    # ─────────────────────────────
    def create_tabs(self) -> None:
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True, padx=12, pady=6)

        self.tab_overview = self._add_tab("Overview")
        self.tab_details = self._add_tab("Details")
        self.tab_pricing = self._add_tab("Pricing")
        self.tab_raw = self._add_tab("Raw JSON")

        ttk.Label(self.tab_overview, text="Overview data will appear here").pack(
            padx=10, pady=10
        )
        ttk.Label(self.tab_details, text="Product details will appear here").pack(
            padx=10, pady=10
        )
        ttk.Label(self.tab_pricing, text="Pricing data will appear here").pack(
            padx=10, pady=10
        )
        ttk.Label(self.tab_raw, text="Raw extracted JSON will appear here").pack(
            padx=10, pady=10
        )

    def _add_tab(self, title: str) -> ttk.Frame:
        frame = ttk.Frame(self.tabs)
        self.tabs.add(frame, text=title)
        return frame

    # ─────────────────────────────
    # Status Bar
    # ─────────────────────────────
    def create_status_bar(self) -> None:
        self.status = ttk.Label(
            self,
            text="Status: Ready",
            anchor="w"
        )
        self.status.pack(fill="x", padx=12, pady=(0, 8))

    # ─────────────────────────────
    # Actions
    # ─────────────────────────────
    def on_extract(self) -> None:
        url = self.url_entry.get().strip()

        if not url:
            self.set_status("Please enter a product URL")
            return

        self.set_status("Extracting product data...")
        # TODO: call extraction service (threaded)

    def set_status(self, message: str) -> None:
        self.status.config(text=f"Status: {message}")