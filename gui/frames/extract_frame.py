import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from pdf_toolbox import extract_text as extract_mod


class ExtractFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.input_path: Path | None = None

        self.file_label_var = tk.StringVar(value="No file selected")

        self.choose_btn = ttk.Button(self, text="Choose PDF…", command=self.choose_file)
        self.file_label = ttk.Label(self, textvariable=self.file_label_var)

        self.range_label = ttk.Label(self, text="Page range (e.g. 1-5 or leave blank for all):")
        self.range_entry = ttk.Entry(self)

        self.extract_btn = ttk.Button(self, text="Extract", command=self.extract_text)

        self.text_widget = tk.Text(self, wrap="word", height=15)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.text_widget.yview)
        self.text_widget.config(yscrollcommand=self.scrollbar.set)

        # Layout
        self.choose_btn.grid(row=0, column=0, sticky="w", padx=4, pady=(4, 2))
        self.file_label.grid(row=0, column=1, sticky="w", padx=4, pady=(4, 2))

        self.range_label.grid(row=1, column=0, sticky="w", padx=4, pady=2)
        self.range_entry.grid(row=1, column=1, sticky="ew", padx=4, pady=2)
        self.extract_btn.grid(row=2, column=0, columnspan=2, sticky="ew", padx=4, pady=(2, 4))

        self.text_widget.grid(row=3, column=0, columnspan=1, sticky="nsew", padx=(4, 0), pady=(0, 4))
        self.scrollbar.grid(row=3, column=1, sticky="ns", padx=(0, 4), pady=(0, 4))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

    def choose_file(self):
        path = filedialog.askopenfilename(
            parent=self,
            title="Select PDF to extract text from",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not path:
            return
        self.input_path = Path(path)
        self.file_label_var.set(str(self.input_path))

    def _parse_range(self, text: str):
        if not text:
            return None, None
        if "-" in text:
            start_str, end_str = text.split("-", 1)
            return int(start_str or 1), int(end_str or start_str)
        page = int(text)
        return page, page

    def extract_text(self):
        if not self.input_path:
            messagebox.showwarning("No file", "Please choose a PDF first.")
            return

        range_text = self.range_entry.get().strip()
        try:
            start_page, end_page = self._parse_range(range_text)
        except ValueError:
            messagebox.showerror("Invalid range", "Could not parse the page range you entered.")
            return

        try:
            text = extract_mod.extract_text(self.input_path, start_page, end_page)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Extract failed", f"An error occurred while extracting:\n{exc}")
            return

        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert("1.0", text)


