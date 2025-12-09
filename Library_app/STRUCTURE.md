# Library Collection - Project Structure

## Overview
The Library Collection application has been reorganized from a monolithic script into a well-organized Python package with separation of concerns.

## Directory Structure

```
Library_app/
└── library_modern/          # Main package
    ├── __init__.py          # Package initialization (exports LibraryApp)
    ├── __main__.py          # Entry point for running as module
    ├── data.py              # Data management & business logic
    └── ui.py                # GUI components using customtkinter
```

## Module Descriptions

### `__init__.py`
Package initialization file that exports the main `LibraryApp` class for easy importing.

### `__main__.py`
Entry point that allows running the package as a module:
```bash
python -m Library_app.library_modern
```

### `data.py`
**Data management and business logic module**

Core functionality includes:
- `load_books()` - Load books from JSON database
- `save_books(books)` - Persist books to file
- `load_settings()` - Load application settings
- `save_settings(settings)` - Persist settings
- `search_books(books, keyword)` - Search by title/author
- `sort_books(books, sort_choice)` - Sort by various criteria
- `filter_by_tag(books, tag)` - Filter by tag
- `get_all_tags(books)` - Extract unique tags
- `add_tag_to_books(books, book_keys, tag)` - Bulk tag addition
- `remove_tag_from_books(books, book_keys, tag)` - Bulk tag removal
- `copy_cover_file(source_path)` - Copy and store cover images

### `ui.py`
**User interface component using customtkinter**

Contains:
- `LibraryApp` - Main application window class
- UI building methods organized by section:
  - `_build_left_panel()` - Book input form
  - `_build_search_controls()` - Search functionality
  - `_build_theme_controls()` - Dark/light mode selector
  - `_build_sort_controls()` - Sorting and filtering
  - `_build_main_area()` - Table and details display
  - `_build_delete_button()` - Delete interface
  - `_build_bulk_actions()` - Multi-select operations

- Action methods:
  - `add_book()` - Add new book
  - `search_books()` - Execute search
  - `apply_sort()` - Apply sorting
  - `apply_tag_filter()` - Filter by tag
  - `bulk_add_tag()` - Add tag to selected
  - `bulk_remove_tag()` - Remove tag from selected
  - `export_selected()` - Export to CSV
  - `delete_selected()` - Delete books
  - And more...

## Benefits of This Organization

1. **Separation of Concerns**: Data logic is separate from UI code
2. **Reusability**: Data functions can be used independently
3. **Testability**: Each module can be tested in isolation
4. **Maintainability**: Code is organized logically and easier to navigate
5. **Scalability**: Easy to add new features without cluttering the codebase
6. **Documentation**: Each module and function is well-documented with docstrings

## Running the Application

### Option 1: Direct module execution
```bash
python -m Library_app.library_modern
```

### Option 2: Using the launcher
```bash
python run_library_modern.py
```

### Option 3: Direct import
```python
from Library_app.library_modern import LibraryApp
app = LibraryApp()
app.mainloop()
```

## Data Files

The application uses the following files in the workspace root:
- `library_db.json` - Stores all book records
- `settings.json` - Stores user preferences (theme, etc.)
- `covers/` - Directory storing book cover images

## Dependencies

- `customtkinter` - Modern tkinter replacement
- `PIL/Pillow` - Image processing for cover thumbnails
- Standard library: json, csv, os, pathlib, tkinter
