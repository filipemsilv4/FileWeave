import tkinter as tk
from tkinter import ttk

from fileweave.constants import APP_TITLE, VERSION

class AboutDialog:
    """
    About dialog class for the FileWeave application.
    """

    def __init__(self, root: tk.Tk):
        """
        Initializes the About dialog.

        Args:
            root: The root Tkinter window.
        """
        self.root = root
        self.about_window = tk.Toplevel(self.root)
        self.about_window.title(f"About {APP_TITLE}")
        self.about_window.geometry("400x200")
        self.about_window.resizable(False, False)

        about_frame = ttk.Frame(self.about_window, padding="20")
        about_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(
            about_frame,
            text=APP_TITLE,
            style="Title.TLabel"
        ).grid(row=0, column=0, pady=(0, 10))

        ttk.Label(
            about_frame,
            text="A smart file concatenator for AI analysis",
            style="Subtitle.TLabel"
        ).grid(row=1, column=0, pady=(0, 20))

        ttk.Label(
            about_frame,
            text=f"Version {VERSION}",
            style="Subtitle.TLabel"
        ).grid(row=2, column=0)
