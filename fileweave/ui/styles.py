import tkinter as tk
from tkinter import ttk
import sys

class StyleManager:
    """
    Manages the styles for the FileWeave application.
    """

    def __init__(self, root: tk.Tk):
        """
        Initializes the StyleManager.

        Args:
            root: The root Tkinter window.
        """
        self.root = root
        self.style = ttk.Style()

    def setup_styles(self):
        """Configures the styles for the application."""
        if sys.platform == "darwin":
            self.style.configure(".", font=("SF Pro", 13))
            self.style.configure("Title.TLabel", font=("SF Pro", 24, "bold"))
            self.style.configure("Subtitle.TLabel", font=("SF Pro", 13))
        else:
            font_name = "Segoe UI" if sys.platform == "win32" else "Ubuntu"
            self.style.configure(".", font=(font_name, 10))
            self.style.configure("Title.TLabel", font=(font_name, 18, "bold"))
            self.style.configure("Subtitle.TLabel", font=(font_name, 10))

        # Configure Treeview
        self.style.configure("Custom.Treeview",
                        rowheight=25,
                        padding=4)
        self.style.configure("Custom.Treeview.Heading",
                        padding=4)

        # Configure specific styles for files and folders
        self.checkbox_images = {
            'unchecked': tk.PhotoImage(width=13, height=13),
            'checked': tk.PhotoImage(width=13, height=13)
        }

        # Create checkmark in the image
        self.checkbox_images['checked'].put(('black',), to=(3, 6, 9, 7))
        self.checkbox_images['checked'].put(('black',), to=(2, 7, 3, 8))
        self.checkbox_images['checked'].put(('black',), to=(9, 2, 10, 6))
