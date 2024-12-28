import tkinter as tk
from tkinter import ttk, filedialog
import os
from typing import Optional, Set
import sys

from fileweave.utils.file_utils import FileUtils
from fileweave.utils.treeview_utils import TreeViewUtils
from fileweave.ui.menu_bar import MenuBar
from fileweave.ui.styles import StyleManager
from fileweave.constants import APP_TITLE, INITIAL_GEOMETRY

class MainWindow:
    """
    Main window class for the FileWeave application.
    """

    def __init__(self, root: tk.Tk):
        """
        Initializes the main window.

        Args:
            root: The root Tkinter window.
        """
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(INITIAL_GEOMETRY)

        # MacOS weirdness
        if sys.platform == "darwin":
            self.root.createcommand('tk::mac::ReopenApplication', self.root.lift)

        self.base_path: Optional[str] = None
        self.base_dir_name: Optional[str] = None
        self.checked_items: Set[str] = set()

        self.style_manager = StyleManager(self.root)
        self.file_utils = FileUtils(self)
        self.treeview_utils = TreeViewUtils(self)

        self.setup_ui()
        self.menu_bar = MenuBar(self.root, self)
        self.setup_bindings()

    def setup_ui(self):
        """Sets up the user interface elements."""
        self.style_manager.setup_styles()

        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Header setup
        self.setup_header(main_frame)

        # PanedWindow
        self.paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        self.paned_window.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Left and right frames
        left_frame = ttk.Frame(self.paned_window, padding="10")
        right_frame = ttk.Frame(self.paned_window, padding="10")

        # Setup left frame
        self.setup_left_frame(left_frame)

        # Setup right frame
        self.setup_right_frame(right_frame)

        # Add frames to paned window
        self.paned_window.add(left_frame, weight=1)
        self.paned_window.add(right_frame, weight=1)

        # Schedule the minimum size calculation
        self.root.after(100, lambda: self.set_minimum_pane_size(left_frame))

    def setup_header(self, parent_frame: ttk.Frame):
        """
        Sets up the header section of the main window.

        Args:
            parent_frame: The parent frame for the header.
        """
        header_frame = ttk.Frame(parent_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        parent_frame.rowconfigure(0, weight=0)

        title = ttk.Label(
            header_frame,
            text=APP_TITLE,
            style="Title.TLabel"
        )
        title.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        subtitle = ttk.Label(
            header_frame,
            text="Select files to combine for AI analysis",
            style="Subtitle.TLabel"
        )
        subtitle.grid(row=1, column=0, sticky=tk.W, pady=(0, 20))

    def setup_left_frame(self, left_frame: ttk.Frame):
        """
        Sets up the left frame containing directory selection and treeview.

        Args:
            left_frame: The left frame to be set up.
        """
        # Directory label
        self.dir_label = ttk.Label(
            left_frame,
            text="No directory selected",
            style="Subtitle.TLabel"
        )
        self.dir_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))

        # Options frame with button and checkboxes
        self.options_frame = ttk.Frame(left_frame)
        self.options_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        left_frame.columnconfigure(0, weight=1)

        select_btn = ttk.Button(
            self.options_frame,
            text="Select Directory",
            command=self.select_directory,
            padding=10
        )
        select_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.use_gitignore = tk.BooleanVar(value=True)
        self.gitignore_check = ttk.Checkbutton(
            self.options_frame,
            text="Respect .gitignore",
            variable=self.use_gitignore,
            command=self.treeview_utils.refresh_tree
        )
        self.gitignore_check.pack(side=tk.LEFT, padx=5)

        self.show_hidden = tk.BooleanVar(value=False)
        self.hidden_check = ttk.Checkbutton(
            self.options_frame,
            text="Show hidden files",
            variable=self.show_hidden,
            command=self.treeview_utils.refresh_tree
        )
        self.hidden_check.pack(side=tk.LEFT, padx=5)

        # Tree frame with scroll
        tree_frame = ttk.Frame(left_frame)
        tree_frame.grid(row=2, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        left_frame.rowconfigure(2, weight=1)

        self.tree = ttk.Treeview(
            tree_frame,
            selectmode="none",
            style="Custom.Treeview",
            show="tree"
        )
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        # Configure tag for checked items
        self.tree.tag_configure('checked', background='#e8e8e8')

        # Action buttons under the tree
        buttons_frame = ttk.Frame(left_frame)
        buttons_frame.grid(row=3, column=0, pady=10, sticky=(tk.W, tk.E))

        self.generate_btn = ttk.Button(
            buttons_frame,
            text="Generate Output",
            command=self.file_utils.generate_output,
            padding=10
        )
        self.generate_btn.pack(side=tk.LEFT, padx=5)

        self.copy_btn = ttk.Button(
            buttons_frame,
            text="Copy to Clipboard",
            command=self.file_utils.copy_to_clipboard,
            padding=10
        )
        self.copy_btn.pack(side=tk.LEFT, padx=5)

        # Status label at the bottom of left side
        self.status_label = ttk.Label(
            left_frame,
            text="Ready",
            style="Subtitle.TLabel"
        )
        self.status_label.grid(row=4, column=0, sticky=tk.W, pady=(5, 0))

    def setup_right_frame(self, right_frame: ttk.Frame):
        """
        Sets up the right frame containing the output text area.

        Args:
            right_frame: The right frame to be set up.
        """
        text_frame = ttk.Frame(right_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        right_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)

        self.output_text = tk.Text(
            text_frame,
            wrap=tk.NONE,
            font=("SF Mono" if sys.platform == "darwin" else "Consolas", 12)
        )

        # Scrollbars for output text
        text_vsb = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        text_hsb = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=self.output_text.xview)
        self.output_text.configure(yscrollcommand=text_vsb.set, xscrollcommand=text_hsb.set)

        # Grid configuration for text and scrollbars
        self.output_text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        text_vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        text_hsb.grid(row=1, column=0, sticky=(tk.E, tk.W))

        text_frame.rowconfigure(0, weight=1)
        text_frame.columnconfigure(0, weight=1)

    def set_minimum_pane_size(self, left_frame: ttk.Frame):
        """
        Calculates and sets the minimum size for the left pane based on widgets.

        Args:
            left_frame: The left frame.
        """
        self.root.update_idletasks()
        min_width = self.options_frame.winfo_reqwidth() + 40
        self.min_pane_width = min_width
        self.paned_window.sashpos(0, min_width)
        self.paned_window.bind('<ButtonRelease-1>', self.check_sash_position)

    def check_sash_position(self, event):
        """
        Ensures the sash doesn't go below the minimum width.

        Args:
            event: The event object.
        """
        sash_pos = self.paned_window.sashpos(0)
        if sash_pos < self.min_pane_width:
            self.paned_window.sashpos(0, self.min_pane_width)

    def setup_bindings(self):
        """Sets up keyboard shortcuts and event bindings."""
        open_shortcut = '<Command-o>' if sys.platform == "darwin" else '<Control-o>'
        copy_shortcut = '<Command-c>' if sys.platform == "darwin" else '<Control-c>'
        self.root.bind(open_shortcut, lambda e: self.select_directory())
        self.root.bind(copy_shortcut, lambda e: self.file_utils.copy_to_clipboard())
        self.tree.bind('<Button-1>', self.treeview_utils.toggle_check)

    def select_directory(self):
        """Opens a directory selection dialog and populates the treeview."""
        self.base_path = filedialog.askdirectory()
        if self.base_path:
            self.base_dir_name = os.path.basename(self.base_path)
            self.dir_label.config(text=f"Selected: {self.base_dir_name}")
            self.tree.delete(*self.tree.get_children())
            self.checked_items.clear()
            self.file_utils.load_gitignore()
            self.treeview_utils.populate_tree('', self.base_path)
            self.treeview_utils.update_status()
