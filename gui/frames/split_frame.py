import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from pdf_toolbox import split as split_mod


class SplitFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.input_path: Path | None = None

        self.file_label_var = tk.StringVar(value="No file selected")

        # Widgets
        self.choose_btn = ttk.Button(self, text="Choose PDF…", command=self.choose_file)
        self.file_label = ttk.Label(self, textvariable=self.file_label_var)

        self.ranges_label = ttk.Label(
            self,
            text="Page ranges (e.g. 1-3,4-4,5-10):",
        )
        self.ranges_entry = ttk.Entry(self)
        self.split_btn = ttk.Button(self, text="Split", command=self.split_file)

        # Layout
        self.choose_btn.grid(row=0, column=0, sticky="w", padx=4, pady=(4, 2))
        self.file_label.grid(row=0, column=1, sticky="w", padx=4, pady=(4, 2))

        self.ranges_label.grid(row=1, column=0, sticky="w", padx=4, pady=2)
        self.ranges_entry.grid(row=1, column=1, sticky="ew", padx=4, pady=2)
        self.split_btn.grid(row=2, column=0, columnspan=2, sticky="ew", padx=4, pady=(2, 4))

        self.columnconfigure(1, weight=1)

    def choose_file(self):
        path = filedialog.askopenfilename(
            parent=self,
            title="Select PDF to split",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not path:
            return
        self.input_path = Path(path)
        self.file_label_var.set(str(self.input_path))

    def _parse_ranges(self, text: str):
        ranges = []
        for part in text.split(","):
            part = part.strip()
            if not part:
                continue
            if "-" in part:
                start_str, end_str = part.split("-", 1)
                ranges.append((int(start_str), int(end_str)))
            else:
                page = int(part)
                ranges.append((page, page))
        return ranges

    def split_file(self):
        if not self.input_path:
            messagebox.showwarning("No file", "Please choose a PDF first.")
            return

        ranges_text = self.ranges_entry.get().strip()
        if not ranges_text:
            messagebox.showwarning("No ranges", "Please enter at least one page range.")
            return

        output_dir = filedialog.askdirectory(
            parent=self,
            title="Select output folder for split PDFs",
        )
        if not output_dir:
            return

        try:
            ranges = self._parse_ranges(ranges_text)
        except ValueError:
            messagebox.showerror("Invalid ranges", "Could not parse the page ranges you entered.")
            return

        try:
            results = split_mod.split_by_ranges(self.input_path, ranges, output_dir)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Split failed", f"An error occurred while splitting:\n{exc}")
            return

        if not results:
            messagebox.showinfo("Done", "No pages produced.")
        else:
            messagebox.showinfo(
                "Done",
                f"Created {len(results)} file(s) in:\n{output_dir}",
            )


