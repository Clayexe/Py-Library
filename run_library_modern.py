"""
Entry point for the Library Collection application.
Launches the Library_app.library_modern package.
"""

import sys
from pathlib import Path

# Add the workspace to the path so we can import Library_app
workspace_dir = Path(__file__).parent
sys.path.insert(0, str(workspace_dir))

from Library_app.library_modern.ui import LibraryApp


if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
