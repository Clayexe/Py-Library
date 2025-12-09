"""
Data management for the library application.
Handles loading, saving, and manipulating book data and application settings.
"""

import json
import os
from pathlib import Path


DB_FILE = "library_db.json"
SETTINGS_FILE = "settings.json"


def load_books():
    """Load books from the database file."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    with open(DB_FILE, "w") as f:
        json.dump([], f)
    return []


def save_books(books):
    """Save books to the database file."""
    with open(DB_FILE, "w") as f:
        json.dump(books, f, indent=2)


def load_settings():
    """Load application settings from file."""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            try:
                return json.load(f)
            except Exception:
                return {}
    return {}


def save_settings(settings):
    """Save application settings to file."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)


def add_book(books, title, author, year, genre, tags, cover_path=None):
    """
    Add a new book to the collection.
    
    Args:
        books: List of book dictionaries
        title: Book title
        author: Book author
        year: Publication year
        genre: Book genre
        tags: List of tag strings
        cover_path: Optional path to cover image file
    
    Returns:
        The new book dictionary or None if validation fails
    """
    if not title or not author or not year:
        return None

    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "tags": tags,
        "cover": cover_path
    }
    
    books.append(book)
    save_books(books)
    return book


def delete_books(books, to_delete_keys):
    """
    Delete books from the collection.
    
    Args:
        books: List of book dictionaries
        to_delete_keys: Set of tuples (title, author, year, genre) to delete
    
    Returns:
        Updated books list
    """
    new_books = []
    for b in books:
        key = (b.get("title", ""), b.get("author", ""), 
               b.get("year", ""), b.get("genre", ""))
        if key not in to_delete_keys:
            new_books.append(b)
    
    return new_books


def search_books(books, keyword):
    """Search books by title or author."""
    keyword = keyword.lower()
    return [b for b in books 
            if keyword in b.get("title", "").lower() 
            or keyword in b.get("author", "").lower()]


def sort_books(books, sort_choice):
    """
    Sort books by the specified criteria.
    
    Args:
        books: List of book dictionaries
        sort_choice: String indicating sort order (e.g., "Title (A→Z)")
    
    Returns:
        Sorted copy of books list
    """
    sorted_books = books.copy()
    
    sort_key_map = {
        "Title (A→Z)": lambda x: x["title"].lower(),
        "Title (Z→A)": lambda x: x["title"].lower(),
        "Author (A→Z)": lambda x: x["author"].lower(),
        "Author (Z→A)": lambda x: x["author"].lower(),
        "Year (Old→New)": lambda x: int(x["year"]) if x["year"].isdigit() else 0,
        "Year (New→Old)": lambda x: int(x["year"]) if x["year"].isdigit() else 0,
        "Genre (A→Z)": lambda x: x["genre"].lower(),
        "Genre (Z→A)": lambda x: x["genre"].lower(),
    }
    
    reverse = sort_choice.endswith("(Z→A)") or sort_choice.endswith("(New→Old)")
    
    if sort_choice in sort_key_map:
        sorted_books.sort(key=sort_key_map[sort_choice], reverse=reverse)
    
    return sorted_books


def filter_by_tag(books, tag):
    """Filter books by a specific tag."""
    if tag == "All":
        return books
    return [b for b in books if tag in b.get("tags", [])]


def get_all_tags(books):
    """Get all unique tags from the books collection."""
    tags = set()
    for b in books:
        for t in b.get("tags", []):
            tags.add(t)
    return sorted(tags)


def add_tag_to_books(books, book_keys, tag):
    """Add a tag to multiple books."""
    changed = 0
    for b in books:
        key = (b.get('title', ''), b.get('author', ''), 
               b.get('year', ''), b.get('genre', ''))
        if key in book_keys:
            tags = b.setdefault("tags", [])
            if tag not in tags:
                tags.append(tag)
                changed += 1
    return changed


def remove_tag_from_books(books, book_keys, tag):
    """Remove a tag from multiple books."""
    changed = 0
    for b in books:
        key = (b.get('title', ''), b.get('author', ''), 
               b.get('year', ''), b.get('genre', ''))
        if key in book_keys:
            tags = b.get("tags", [])
            if tag in tags:
                tags.remove(tag)
                changed += 1
    return changed


def copy_cover_file(source_path, dest_dir="covers"):
    """
    Copy a cover image file to the covers directory with a unique name.
    
    Args:
        source_path: Path to the source image file
        dest_dir: Destination directory name
    
    Returns:
        Destination path as POSIX string or None on failure
    """
    try:
        import shutil
        covers_dir = Path(dest_dir)
        covers_dir.mkdir(exist_ok=True)
        src = Path(source_path)
        dest_name = f"{int(src.stat().st_mtime)}_{src.name}"
        dest = covers_dir / dest_name
        shutil.copy(src, dest)
        return str(dest.as_posix())
    except Exception:
        return None
