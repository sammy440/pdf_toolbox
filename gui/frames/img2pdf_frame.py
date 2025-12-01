import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from pdf_toolbox import images_to_pdf as img2pdf_mod


class ImagesToPdfFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.files: list[Path] = []

        self.listbox = tk.Listbox(self, height=8)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.add_btn = ttk.Button(self, text="Add images…", command=self.add_files)
        self.remove_btn = ttk.Button(self, text="Remove Selected", command=self.remove_selected)
        self.convert_btn = ttk.Button(self, text="Convert to PDF…", command=self.convert)

        self.listbox.grid(row=0, column=0, rowspan=3, sticky="nsew", padx=(0, 4), pady=4)
        self.scrollbar.grid(row=0, column=1, rowspan=3, sticky="ns", pady=4)

        self.add_btn.grid(row=0, column=2, sticky="ew", pady=(4, 2))
        self.remove_btn.grid(row=1, column=2, sticky="ew", pady=2)
        self.convert_btn.grid(row=2, column=2, sticky="ew", pady=(2, 4))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def add_files(self):
        paths = filedialog.askopenfilenames(
            parent=self,
            title="Select images to convert",
            filetypes=[
                ("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.gif"),
                ("All files", "*.*"),
            ],
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

    def convert(self):
        if not self.files:
            messagebox.showwarning("No images", "Please add at least one image.")
            return

        output_path = filedialog.asksaveasfilename(
            parent=self,
            title="Save PDF as…",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not output_path:
            return

        try:
            img2pdf_mod.images_to_pdf(self.files, output_path)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Conversion failed", f"An error occurred while converting:\n{exc}")
            return

        messagebox.showinfo("Done", f"PDF saved to:\n{output_path}")


