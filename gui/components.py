"""
Reusable Tkinter components for the PDF toolbox GUI.
"""

import tkinter as tk
from tkinter import ttk


class LabeledEntry(ttk.Frame):
    def __init__(self, master, label: str, **kwargs):
        super().__init__(master)
        self.label_widget = ttk.Label(self, text=label)
        self.entry_var = tk.StringVar()
        self.entry_widget = ttk.Entry(self, textvariable=self.entry_var, **kwargs)

        self.label_widget.grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.entry_widget.grid(row=0, column=1, sticky="ew")
        self.columnconfigure(1, weight=1)

    def get(self) -> str:
        return self.entry_var.get()

    def set(self, value: str) -> None:
        self.entry_var.set(value)


