import os
from typing import Optional
import pathspec
import tkinter as tk

class FileUtils:
    """
    Utility class for file operations in the FileWeave application.
    """

    def __init__(self, main_window: "MainWindow"):
        """
        Initializes the FileUtils class.

        Args:
            main_window: The main window instance.
        """
        self.main_window = main_window
        self.gitignore_spec: Optional[pathspec.PathSpec] = None

    def load_gitignore(self):
        """Loads the .gitignore file if present and enabled."""
        self.gitignore_spec = None
        if self.main_window.use_gitignore.get() and self.main_window.base_path:
            gitignore_path = os.path.join(self.main_window.base_path, '.gitignore')
            if os.path.exists(gitignore_path):
                try:
                    with open(gitignore_path, 'r', encoding='utf-8') as f:
                        spec = pathspec.PathSpec.from_lines('gitwildmatch', f)
                    self.gitignore_spec = spec
                except Exception:
                    pass

    def should_show_item(self, path: str, name: str) -> bool:
        """
        Determines whether an item should be shown in the treeview based on .gitignore and hidden file settings.

        Args:
            path: The path of the item.
            name: The name of the item.

        Returns:
            True if the item should be shown, False otherwise.
        """
        if name.startswith('.') and not self.main_window.show_hidden.get():
            return False

        if self.gitignore_spec and self.main_window.use_gitignore.get():
            full_path = os.path.join(path, name)
            relative_path = os.path.relpath(full_path, self.main_window.base_path)
            relative_path = relative_path.replace(os.sep, '/')
            if self.gitignore_spec.match_file(relative_path):
                return False

            if os.path.isdir(full_path):
                dir_pattern = relative_path + '/**'
                if self.gitignore_spec.match_file(dir_pattern):
                    return False

        return True

    def generate_output(self):
        """Generates the output text by concatenating selected files."""
        self.main_window.output_text.delete(1.0, tk.END)

        if not self.main_window.base_path:
            self.main_window.output_text.insert(tk.END, "No directory selected.\n")
            return

        for item_id in self.main_window.checked_items:
            # Use item_id directly as it's already the full path
            if os.path.isfile(item_id):
                try:
                    with open(item_id, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Extract relative path for display purposes
                    relative_path = os.path.relpath(item_id, self.main_window.base_path)

                    ext = os.path.splitext(item_id)[1].lower()
                    if ext in ['.py', '.java', '.js', '.cpp', '.c']:
                        language = ext[1:]
                    else:
                        language = 'text'

                    self.main_window.output_text.insert(tk.END, f"```{language}\n")
                    self.main_window.output_text.insert(
                        tk.END,
                        f"# {self.main_window.base_dir_name}/{relative_path}\n"
                    )
                    self.main_window.output_text.insert(tk.END, f"{content}\n")
                    self.main_window.output_text.insert(tk.END, "```\n\n")
                except Exception as e:
                    self.main_window.output_text.insert(
                        tk.END,
                        f"Error reading {relative_path}: {str(e)}\n\n"
                    )

        self.main_window.status_label.config(text="Output generated")

    def copy_to_clipboard(self):
        """Copies the output text to the clipboard."""
        self.main_window.root.clipboard_clear()
        self.main_window.root.clipboard_append(self.main_window.output_text.get(1.0, tk.END))
        self.main_window.status_label.config(text="Copied to clipboard")
