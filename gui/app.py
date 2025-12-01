import tkinter as tk
from tkinter import ttk

from .frames.merge_frame import MergeFrame
from .frames.split_frame import SplitFrame
from .frames.extract_frame import ExtractFrame
from .frames.watermark_frame import WatermarkFrame
from .frames.img2pdf_frame import ImagesToPdfFrame
from .frames.metadata_frame import MetadataFrame


class PdfToolboxApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Automation Toolbox")
        self.geometry("900x600")

        # On some platforms themed widgets look better
        try:
            self.style = ttk.Style(self)
            if "clam" in self.style.theme_names():
                self.style.theme_use("clam")
        except Exception:  # noqa: BLE001
            pass

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        self.merge_frame = MergeFrame(notebook)
        self.split_frame = SplitFrame(notebook)
        self.extract_frame = ExtractFrame(notebook)
        self.watermark_frame = WatermarkFrame(notebook)
        self.img2pdf_frame = ImagesToPdfFrame(notebook)
        self.metadata_frame = MetadataFrame(notebook)

        notebook.add(self.merge_frame, text="Merge")
        notebook.add(self.split_frame, text="Split")
        notebook.add(self.extract_frame, text="Extract Text")
        notebook.add(self.watermark_frame, text="Watermark")
        notebook.add(self.img2pdf_frame, text="Images → PDF")
        notebook.add(self.metadata_frame, text="Metadata")


def run():
    app = PdfToolboxApp()
    app.mainloop()


