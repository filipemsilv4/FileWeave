import tkinter as tk
from tkinter import ttk

from fileweave.ui.about_dialog import AboutDialog
from fileweave.constants import APP_TITLE

class MenuBar:
    """
    Menu bar class for the FileWeave application.
    """

    def __init__(self, root: tk.Tk, main_window: "MainWindow"):
        """
        Initializes the menu bar.

        Args:
            root: The root Tkinter window.
            main_window: The main window instance.
        """
        self.root = root
        self.main_window = main_window

        menubar = tk.Menu(self.root)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(
            label="Open Directory...",
            command=self.main_window.select_directory,
            accelerator="⌘O" if tk.TkVersion >= 8.6 else "Ctrl+O"
        )
        file_menu.add_command(
            label="Copy Output",
            command=self.main_window.file_utils.copy_to_clipboard,
            accelerator="⌘C" if tk.TkVersion >= 8.6 else "Ctrl+C"
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def show_about(self):
        """
        Displays the About dialog.
        """
        AboutDialog(self.root)
