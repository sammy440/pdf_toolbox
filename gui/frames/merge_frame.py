import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from pdf_toolbox import merge as merge_mod


class MergeFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.files: list[Path] = []

        # File list
        self.listbox = tk.Listbox(self, height=8)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # Buttons
        self.add_btn = ttk.Button(self, text="Add PDFs…", command=self.add_files)
        self.remove_btn = ttk.Button(self, text="Remove Selected", command=self.remove_selected)
        self.up_btn = ttk.Button(self, text="Move Up", command=lambda: self.move_selected(-1))
        self.down_btn = ttk.Button(self, text="Move Down", command=lambda: self.move_selected(1))
        self.merge_btn = ttk.Button(self, text="Merge to…", command=self.merge_files)

        # Layout
        self.listbox.grid(row=0, column=0, rowspan=4, sticky="nsew", padx=(0, 4), pady=4)
        self.scrollbar.grid(row=0, column=1, rowspan=4, sticky="ns", pady=4)

        self.add_btn.grid(row=0, column=2, sticky="ew", pady=(4, 2))
        self.remove_btn.grid(row=1, column=2, sticky="ew", pady=2)
        self.up_btn.grid(row=2, column=2, sticky="ew", pady=2)
        self.down_btn.grid(row=3, column=2, sticky="ew", pady=2)
        self.merge_btn.grid(row=4, column=0, columnspan=3, sticky="ew", padx=4, pady=(2, 4))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def add_files(self):
        paths = filedialog.askopenfilenames(
            parent=self,
            title="Select PDF files to merge",
            filetypes=[("PDF files", "*.pdf")],
        )
        for p in paths:
            p_path = Path(p)
            if p_path not in self.files:
                self.files.append(p_path)
                self.listbox.insert(tk.END, str(p_path))

    def remove_selected(self):
        selection = list(self.listbox.curselection())
        if not selection:
            return
        for index in reversed(selection):
            self.listbox.delete(index)
            del self.files[index]

    def move_selected(self, direction: int):
        selection = list(self.listbox.curselection())
        if len(selection) != 1:
            return
        index = selection[0]
        new_index = index + direction
        if not (0 <= new_index < self.listbox.size()):
            return

        # Swap in internal list
        self.files[index], self.files[new_index] = self.files[new_index], self.files[index]

        # Swap in listbox
        text = self.listbox.get(index)
        self.listbox.delete(index)
        self.listbox.insert(new_index, text)
        self.listbox.selection_set(new_index)

    def merge_files(self):
        if not self.files:
            messagebox.showwarning("No files", "Please add at least one PDF file to merge.")
            return

        output_path = filedialog.asksaveasfilename(
            parent=self,
            title="Save merged PDF as…",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not output_path:
            return

        try:
            merge_mod.merge_files(self.files, output_path)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Merge failed", f"An error occurred while merging:\n{exc}")
            return

        messagebox.showinfo("Done", f"Merged PDF saved to:\n{output_path}")


