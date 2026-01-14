from tkinter import ttk


class StatusBar(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label = ttk.Label(self, text="Ready", anchor="w")
        self.label.pack(fill="x")

    def set(self, text: str) -> None:
        self.label.config(text=text)