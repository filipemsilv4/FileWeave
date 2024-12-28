import tkinter as tk

from fileweave.ui.main_window import MainWindow

class FileWeaveApp:
    """
    Main application class for FileWeave.
    """

    def __init__(self, root: tk.Tk):
        """
        Initializes the FileWeave application.

        Args:
            root: The root Tkinter window.
        """
        self.root = root
        self.main_window = MainWindow(self.root)

    def run(self):
        """
        Runs the main application loop.
        """
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileWeaveApp(root)
    app.run()
