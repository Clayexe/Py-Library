"""
Main entry point for the Library Collection application.
"""

from .ui import LibraryApp


if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
