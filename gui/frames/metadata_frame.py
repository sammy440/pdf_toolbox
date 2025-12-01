import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from pdf_toolbox import metadata as metadata_mod


class MetadataFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.input_path: Path | None = None
        self.file_label_var = tk.StringVar(value="No file selected")

        self.choose_btn = ttk.Button(self, text="Choose PDF…", command=self.choose_file)
        self.file_label = ttk.Label(self, textvariable=self.file_label_var)

        self.tree = ttk.Treeview(self, columns=("value",), show="headings")
        self.tree.heading("value", text="Value")
        self.tree["displaycolumns"] = ("value",)

        self.tree.column("value", width=300, anchor="w")

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.config(yscrollcommand=self.scrollbar.set)

        # Layout
        self.choose_btn.grid(row=0, column=0, sticky="w", padx=4, pady=(4, 2))
        self.file_label.grid(row=0, column=1, sticky="w", padx=4, pady=(4, 2))

        self.tree.grid(row=1, column=0, sticky="nsew", padx=(4, 0), pady=(0, 4))
        self.scrollbar.grid(row=1, column=1, sticky="ns", padx=(0, 4), pady=(0, 4))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def choose_file(self):
        path = filedialog.askopenfilename(
            parent=self,
            title="Select PDF to inspect metadata",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not path:
            return
        self.input_path = Path(path)
        self.file_label_var.set(str(self.input_path))
        self.load_metadata()

    def load_metadata(self):
        if not self.input_path:
            return
        try:
            meta = metadata_mod.read_metadata(self.input_path)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Error", f"Failed to read metadata:\n{exc}")
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        for key, value in meta.items():
            self.tree.insert("", tk.END, values=(f"{key}: {value}",))


