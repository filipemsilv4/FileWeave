import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import sys
from typing import Optional

class FileViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FileWeave")
        self.root.geometry("1000x700")

        # MacOS weirdness
        if sys.platform == "darwin":
            self.root.createcommand('tk::mac::ReopenApplication', self.root.lift)

        self.base_path: Optional[str] = None
        self.base_dir_name: Optional[str] = None
        self.checked_items = set()

        self.setup_icons()
        self.setup_styles()
        self.setup_ui()
        self.setup_bindings()
        self.setup_menu()

    def setup_icons(self):
        # Emojis as icons - universal enough
        self.icons = {
            'folder': '📁',
            'file': '📄',
            '.py': '🐍',
            '.js': '☕',
            '.json': '🔧',
            '.md': '📘',
            '.txt': '📝',
            '.yml': '⚙️',
            '.yaml': '⚙️',
            '.html': '🌐',
            '.css': '🎨',
            '.gitignore': '👁️',
            'LICENSE': '⚖️',
            'README': '📖',
        }

    def setup_styles(self):
        style = ttk.Style()

        if sys.platform == "darwin":
            style.configure(".", font=("SF Pro", 13))
            style.configure("Title.TLabel", font=("SF Pro", 24, "bold"))
            style.configure("Subtitle.TLabel", font=("SF Pro", 13))
        else:
            font_name = "Segoe UI" if sys.platform == "win32" else "Ubuntu"
            style.configure(".", font=(font_name, 10))
            style.configure("Title.TLabel", font=(font_name, 18, "bold"))
            style.configure("Subtitle.TLabel", font=(font_name, 10))

        style.configure("Custom.Treeview",
                        rowheight=25,
                        padding=4)
        style.configure("Custom.Treeview.Heading",
                        padding=4)

    def setup_ui(self):
        # Main frame to hold everything
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # -----------------------
        # Header alone at the top
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        main_frame.rowconfigure(0, weight=0)

        title = ttk.Label(header_frame, text="FileWeave", style="Title.TLabel")
        title.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        subtitle = ttk.Label(
            header_frame,
            text="Select files to combine for AI analysis",
            style="Subtitle.TLabel"
        )
        subtitle.grid(row=1, column=0, sticky=tk.W, pady=(0, 20))

        # -----------------------
        # Content frame below header, side by side (left = directory stuff, right = output)
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        main_frame.rowconfigure(1, weight=1)
        content_frame.columnconfigure(0, weight=2)  # left side bigger
        content_frame.columnconfigure(1, weight=1)  # right side smaller
        content_frame.rowconfigure(0, weight=1)

        # Left frame for directory selection + file tree
        left_frame = ttk.Frame(content_frame, padding="10")
        left_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Right frame for output text
        right_frame = ttk.Frame(content_frame, padding="10")
        right_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Directory stuff on the left
        self.dir_label = ttk.Label(
            left_frame,
            text="No directory selected",
            style="Subtitle.TLabel"
        )
        self.dir_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))

        select_btn = ttk.Button(
            left_frame,
            text="Select Directory",
            command=self.select_directory,
            padding=10
        )
        select_btn.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))

        # Tree frame with scroll
        tree_frame = ttk.Frame(left_frame)
        tree_frame.grid(row=2, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        left_frame.rowconfigure(2, weight=1)
        left_frame.columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            tree_frame,
            selectmode="extended",
            style="Custom.Treeview",
            show="tree"
        )
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        # Action buttons under the tree
        buttons_frame = ttk.Frame(left_frame)
        buttons_frame.grid(row=3, column=0, pady=10, sticky=tk.W)

        self.generate_btn = ttk.Button(
            buttons_frame,
            text="Generate Output",
            command=self.generate_output,
            padding=10
        )
        self.generate_btn.pack(side=tk.LEFT, padx=5)

        self.copy_btn = ttk.Button(
            buttons_frame,
            text="Copy to Clipboard",
            command=self.copy_to_clipboard,
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

        # Output text on the right
        self.output_text = tk.Text(
            right_frame,
            height=15,
            wrap=tk.NONE,
            font=("SF Mono" if sys.platform == "darwin" else "Consolas", 12)
        )
        self.output_text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Scrollbars for output text
        text_vsb = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        text_hsb = ttk.Scrollbar(right_frame, orient=tk.HORIZONTAL, command=self.output_text.xview)
        self.output_text.configure(yscrollcommand=text_vsb.set, xscrollcommand=text_hsb.set)

        text_vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        text_hsb.grid(row=1, column=0, sticky=(tk.E, tk.W))

        right_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)

    def setup_bindings(self):
        # Keyboard shortcuts
        open_shortcut = '<Command-o>' if sys.platform == "darwin" else '<Control-o>'
        copy_shortcut = '<Command-c>' if sys.platform == "darwin" else '<Control-c>'
        self.root.bind(open_shortcut, lambda e: self.select_directory())
        self.root.bind(copy_shortcut, lambda e: self.copy_to_clipboard())

        # Bind for toggling check
        self.tree.bind('<Button-1>', self.toggle_check)

    def setup_menu(self):
        menubar = tk.Menu(self.root)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(
            label="Open Directory...",
            command=self.select_directory,
            accelerator="⌘O" if sys.platform == "darwin" else "Ctrl+O"
        )
        file_menu.add_command(
            label="Copy Output",
            command=self.copy_to_clipboard,
            accelerator="⌘C" if sys.platform == "darwin" else "Ctrl+C"
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
        about_window = tk.Toplevel(self.root)
        about_window.title("About FileWeave")
        about_window.geometry("400x200")
        about_window.resizable(False, False)

        about_frame = ttk.Frame(about_window, padding="20")
        about_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(
            about_frame,
            text="FileWeave",
            style="Title.TLabel"
        ).grid(row=0, column=0, pady=(0, 10))

        ttk.Label(
            about_frame,
            text="A smart file concatenator for AI analysis",
            style="Subtitle.TLabel"
        ).grid(row=1, column=0, pady=(0, 20))

        ttk.Label(
            about_frame,
            text="Version 0.1.0",
            style="Subtitle.TLabel"
        ).grid(row=2, column=0)

    def toggle_check(self, event):
        item = self.tree.identify('item', event.x, event.y)
        if item:
            if item in self.checked_items:
                self.tree.item(item, tags=())
                self.checked_items.remove(item)
            else:
                self.tree.item(item, tags=('checked',))
                self.checked_items.add(item)
            self.update_status()

    def update_status(self):
        num_selected = len(self.checked_items)
        self.status_label.config(
            text=f"{num_selected} file{'s' if num_selected != 1 else ''} selected"
        )

    def select_directory(self):
        self.base_path = filedialog.askdirectory()
        if self.base_path:
            self.base_dir_name = os.path.basename(self.base_path)
            self.dir_label.config(text=f"Selected: {self.base_dir_name}")
            self.tree.delete(*self.tree.get_children())
            self.checked_items.clear()
            self.populate_tree('', self.base_path)
            self.update_status()

    def populate_tree(self, parent, path):
        # Sort dir items to avoid random crap
        for item in sorted(os.listdir(path)):
            item_path = os.path.join(path, item)

            # Determine icon
            if os.path.isfile(item_path):
                ext = os.path.splitext(item)[1].lower()
                icon = self.icons.get(ext, self.icons['file'])
                if item.upper() in ['README.MD', 'LICENSE', '.GITIGNORE']:
                    icon = self.icons.get(item.upper(), icon)
            else:
                icon = self.icons['folder']

            node = self.tree.insert(
                parent,
                'end',
                item_path,
                text=f"{icon} {item}",
                tags=()
            )

            # Recursively populate subdirectories
            if os.path.isdir(item_path):
                self.populate_tree(node, item_path)

    def generate_output(self):
        self.output_text.delete(1.0, tk.END)

        if not self.base_path:
            self.output_text.insert(tk.END, "No directory selected, genius.\n")
            return

        for item_id in self.checked_items:
            if os.path.isfile(item_id):
                relative_path = os.path.relpath(item_id, self.base_path)
                try:
                    with open(item_id, 'r', encoding='utf-8') as f:
                        content = f.read()

                    ext = os.path.splitext(item_id)[1].lower()
                    if ext in ['.py', '.java', '.js', '.cpp', '.c']:
                        language = ext[1:]
                    else:
                        language = 'text'

                    self.output_text.insert(tk.END, f"```{language}\n")
                    self.output_text.insert(tk.END, f"# {self.base_dir_name}/{relative_path}\n")
                    self.output_text.insert(tk.END, f"{content}\n")
                    self.output_text.insert(tk.END, "```\n\n")
                except Exception as e:
                    self.output_text.insert(tk.END, f"Error reading {relative_path}: {str(e)}\n\n")

        self.status_label.config(text="Output generated")

    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.output_text.get(1.0, tk.END))
        self.status_label.config(text="Copied to clipboard")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileViewerApp(root)
    root.mainloop()