import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from pdf_toolbox import watermark as watermark_mod


class WatermarkFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.input_path: Path | None = None
        self.watermark_path: Path | None = None

        self.input_label_var = tk.StringVar(value="No base PDF selected")
        self.watermark_label_var = tk.StringVar(value="No watermark PDF selected")

        self.choose_input_btn = ttk.Button(self, text="Choose base PDF…", command=self.choose_input)
        self.input_label = ttk.Label(self, textvariable=self.input_label_var)

        self.choose_watermark_btn = ttk.Button(
            self,
            text="Choose watermark PDF…",
            command=self.choose_watermark,
        )
        self.watermark_label = ttk.Label(self, textvariable=self.watermark_label_var)

        self.apply_btn = ttk.Button(self, text="Apply watermark…", command=self.apply_watermark)

        # Layout
        self.choose_input_btn.grid(row=0, column=0, sticky="w", padx=4, pady=(4, 2))
        self.input_label.grid(row=0, column=1, sticky="w", padx=4, pady=(4, 2))

        self.choose_watermark_btn.grid(row=1, column=0, sticky="w", padx=4, pady=2)
        self.watermark_label.grid(row=1, column=1, sticky="w", padx=4, pady=2)

        self.apply_btn.grid(row=2, column=0, columnspan=2, sticky="ew", padx=4, pady=(2, 4))

        self.columnconfigure(1, weight=1)

    def choose_input(self):
        path = filedialog.askopenfilename(
            parent=self,
            title="Select PDF to watermark",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not path:
            return
        self.input_path = Path(path)
        self.input_label_var.set(str(self.input_path))

    def choose_watermark(self):
        path = filedialog.askopenfilename(
            parent=self,
            title="Select watermark PDF (first page used)",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not path:
            return
        self.watermark_path = Path(path)
        self.watermark_label_var.set(str(self.watermark_path))

    def apply_watermark(self):
        if not self.input_path:
            messagebox.showwarning("No base PDF", "Please choose the base PDF.")
            return
        if not self.watermark_path:
            messagebox.showwarning("No watermark PDF", "Please choose a watermark PDF.")
            return

        output_path = filedialog.asksaveasfilename(
            parent=self,
            title="Save watermarked PDF as…",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not output_path:
            return

        try:
            watermark_mod.apply_watermark(self.input_path, self.watermark_path, output_path)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Watermark failed", f"An error occurred while watermarking:\n{exc}")
            return

        messagebox.showinfo("Done", f"Watermarked PDF saved to:\n{output_path}")


