import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import sys
from typing import Optional
import pathspec

class FileViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FileWeave")
        self.root.geometry("1000x700")
        self.show_hidden = tk.BooleanVar(value=False)
        self.use_gitignore = tk.BooleanVar(value=True)
        self.gitignore_spec = None

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

        # Configure Treeview
        style.configure("Custom.Treeview",
                        rowheight=25,
                        padding=4)
        style.configure("Custom.Treeview.Heading",
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

    def setup_ui(self):
        # Main frame to hold everything
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Header setup...
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

        # Create PanedWindow
        self.paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        self.paned_window.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Left frame
        left_frame = ttk.Frame(self.paned_window, padding="10")
        right_frame = ttk.Frame(self.paned_window, padding="10")

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

        self.gitignore_check = ttk.Checkbutton(
            self.options_frame,
            text="Respect .gitignore",
            variable=self.use_gitignore,
            command=self.refresh_tree
        )
        self.gitignore_check.pack(side=tk.LEFT, padx=5)

        self.hidden_check = ttk.Checkbutton(
            self.options_frame,
            text="Show hidden files",
            variable=self.show_hidden,
            command=self.refresh_tree
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

        # Output text on the right (in a frame with scrollbars)
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
        
        # Add frames to paned window
        self.paned_window.add(left_frame, weight=1)
        self.paned_window.add(right_frame, weight=1)

        # Schedule the minimum size calculation after all widgets are rendered
        self.root.after(100, lambda: self.set_minimum_pane_size(left_frame))
      
    def set_minimum_pane_size(self, left_frame):
        """Calculate and set the minimum size for the left pane based on widgets"""
        # Force geometry update
        self.root.update_idletasks()
        
        # Get the required width of the options frame
        min_width = self.options_frame.winfo_reqwidth()
        
        # Add padding for safety
        min_width += 40  # Ajuste este valor conforme necessário
        
        # Store minimum width for sash movement check
        self.min_pane_width = min_width
        
        # Set initial sash position
        self.paned_window.sashpos(0, min_width)
        
        # Bind sash movement
        self.paned_window.bind('<ButtonRelease-1>', self.check_sash_position)

    def check_sash_position(self, event):
        """Ensure the sash doesn't go below minimum width"""
        sash_pos = self.paned_window.sashpos(0)
        if sash_pos < self.min_pane_width:
            self.paned_window.sashpos(0, self.min_pane_width)

    def load_gitignore(self):
        self.gitignore_spec = None
        if self.use_gitignore.get() and self.base_path:
            gitignore_path = os.path.join(self.base_path, '.gitignore')
            if os.path.exists(gitignore_path):
                try:
                    with open(gitignore_path, 'r', encoding='utf-8') as f:
                        spec = pathspec.PathSpec.from_lines('gitwildmatch', f)
                    self.gitignore_spec = spec
                except Exception:
                    pass

    def get_opened_children(self, item):
        """Recursively get all opened children"""
        opened = []
        if self.tree.item(item)['open']:
            opened.append(item)
            for child in self.tree.get_children(item):
                opened.extend(self.get_opened_children(child))
        return opened

    def save_tree_state(self):
        """Save the current state of opened folders and checked items"""
        state = {
            'opened': [],
            'checked_paths': []  # Mudado de checked_texts para checked_paths
        }
        
        def _save_open_state(item):
            if self.tree.item(item)['open']:
                state['opened'].append(self.tree.item(item)['text'])
                for child in self.tree.get_children(item):
                    _save_open_state(child)
        
        # Save opened state
        for item in self.tree.get_children(''):
            _save_open_state(item)
        
        # Save checked items using full paths
        for item in self.checked_items:
            if os.path.exists(item):  # Garante que o caminho ainda existe
                state['checked_paths'].append(item)
        
        return state

    def restore_tree_state(self, state):
        """Restore the saved state of opened folders and checked items"""
        def _restore_state(item):
            item_text = self.tree.item(item)['text']
            if item_text in state['opened']:
                self.tree.item(item, open=True)
            if item in state['checked_paths']:  # Compara o caminho completo
                self.tree.item(item, tags=('checked',))
                self.checked_items.add(item)
            for child in self.tree.get_children(item):
                _restore_state(child)
        
        for item in self.tree.get_children(''):
            _restore_state(item)

    def refresh_tree(self):
        if self.base_path:
            # Save current state
            state = self.save_tree_state()
            
            self.tree.delete(*self.tree.get_children())
            self.checked_items.clear()
            self.load_gitignore()
            self.populate_tree('', self.base_path)
            
            # Restore state
            self.restore_tree_state(state)
            
            self.update_status()

    def should_show_item(self, path, name):
        # Check if it's a hidden file
        if name.startswith('.') and not self.show_hidden.get():
            return False

        # Check gitignore rules
        if self.gitignore_spec and self.use_gitignore.get():
            full_path = os.path.join(path, name)
            relative_path = os.path.relpath(full_path, self.base_path)
            
            # Normalize path for Windows
            relative_path = relative_path.replace(os.sep, '/')
            
            if self.gitignore_spec.match_file(relative_path):
                return False
            
            # Special case for directories
            if os.path.isdir(full_path):
                # Check if any pattern matches directory/**
                dir_pattern = relative_path + '/**'
                if self.gitignore_spec.match_file(dir_pattern):
                    return False

        return True

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
        if item and os.path.isfile(item):  # Only toggle files, not directories
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
            self.load_gitignore()
            self.populate_tree('', self.base_path)
            self.update_status()

    def populate_tree(self, parent, path):
        # Sort dir items to avoid random crap
        for item in sorted(os.listdir(path)):
            if not self.should_show_item(path, item):
                continue
                
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
                tags=('file',) if os.path.isfile(item_path) else ('folder',)
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