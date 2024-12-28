import os
from typing import Dict, List, Set

from fileweave.constants import ICONS

class TreeViewUtils:
    """
    Utility class for managing the Treeview widget in the FileWeave application.
    """

    def __init__(self, main_window: "MainWindow"):
        """
        Initializes the TreeViewUtils class.

        Args:
            main_window: The main window instance.
        """
        self.main_window = main_window

    def get_opened_children(self, item: str) -> List[str]:
        """
        Recursively gets all opened children of an item in the treeview.

        Args:
            item: The item ID.

        Returns:
            A list of opened item IDs.
        """
        opened = []
        if self.main_window.tree.item(item)['open']:
            opened.append(item)
            for child in self.main_window.tree.get_children(item):
                opened.extend(self.get_opened_children(child))
        return opened

    def save_tree_state(self) -> Dict:
        """
        Saves the current state of opened folders and checked items in the treeview.

        Returns:
            A dictionary containing the saved state.
        """
        state = {
            'opened': [],
            'checked_paths': []
        }

        def _save_open_state(item):
            if self.main_window.tree.item(item)['open']:
                state['opened'].append(self.main_window.tree.item(item)['text'])
                for child in self.main_window.tree.get_children(item):
                    _save_open_state(child)

        for item in self.main_window.tree.get_children(''):
            _save_open_state(item)

        for item in self.main_window.checked_items:
            if os.path.exists(item):
                state['checked_paths'].append(item)

        return state

    def restore_tree_state(self, state: Dict):
        """
        Restores the saved state of opened folders and checked items in the treeview.

        Args:
            state: The saved state dictionary.
        """
        def _restore_state(item):
            item_text = self.main_window.tree.item(item)['text']
            if item_text in state['opened']:
                self.main_window.tree.item(item, open=True)
            if item in state['checked_paths']:
                self.main_window.tree.item(item, tags=('checked',))
                self.main_window.checked_items.add(item)
            for child in self.main_window.tree.get_children(item):
                _restore_state(child)

        for item in self.main_window.tree.get_children(''):
            _restore_state(item)

    def refresh_tree(self):
        """Refreshes the treeview, reloading its contents."""
        if self.main_window.base_path:
            state = self.save_tree_state()
            self.main_window.tree.delete(*self.main_window.tree.get_children())
            self.main_window.checked_items.clear()
            self.main_window.file_utils.load_gitignore()
            self.populate_tree('', self.main_window.base_path)
            self.restore_tree_state(state)
            self.update_status()

    def toggle_check(self, event):
        """
        Toggles the check state of an item in the treeview.

        Args:
            event: The event object.
        """
        item = self.main_window.tree.identify('item', event.x, event.y)
        if item and os.path.isfile(item):
            if item in self.main_window.checked_items:
                self.main_window.tree.item(item, tags=())
                self.main_window.checked_items.remove(item)
            else:
                self.main_window.tree.item(item, tags=('checked',))
                self.main_window.checked_items.add(item)
            self.update_status()

    def update_status(self):
        """Updates the status label with the number of selected files."""
        num_selected = len(self.main_window.checked_items)
        self.main_window.status_label.config(
            text=f"{num_selected} file{'s' if num_selected != 1 else ''} selected"
        )

    def populate_tree(self, parent: str, path: str):
        """
        Populates the treeview with the contents of a directory.

        Args:
            parent: The parent item ID.
            path: The path of the directory to populate.
        """
        for item in sorted(os.listdir(path)):
            if not self.main_window.file_utils.should_show_item(path, item):
                continue

            item_path = os.path.join(path, item)

            if os.path.isfile(item_path):
                ext = os.path.splitext(item)[1].lower()
                icon = ICONS.get(ext, ICONS['file'])
                if item.upper() in ['README.MD', 'LICENSE', '.GITIGNORE']:
                    icon = ICONS.get(item.upper(), icon)
            else:
                icon = ICONS['folder']

            node = self.main_window.tree.insert(
                parent,
                'end',
                item_path,
                text=f"{icon} {item}",
                tags=('file',) if os.path.isfile(item_path) else ('folder',)
            )

            if os.path.isdir(item_path):
                self.populate_tree(node, item_path)
