"""
UI components for the library application.
Implements the main LibraryApp class using customtkinter.
"""

import csv
from pathlib import Path
from tkinter import ttk, messagebox, filedialog, simpledialog

try:
    import customtkinter as ctk
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    import tkinter as ctk

from .data import (
    load_books, save_books, load_settings, save_settings,
    search_books, sort_books, filter_by_tag, get_all_tags,
    add_tag_to_books, remove_tag_from_books, copy_cover_file
)


class LibraryApp(ctk.CTk):
    """Main application window for the library collection manager."""
    
    WINDOW_TITLE = "📚 Library Collection"
    WINDOW_GEOMETRY = "900x550"
    
    def __init__(self):
        super().__init__()
        
        self.title(self.WINDOW_TITLE)
        self.geometry(self.WINDOW_GEOMETRY)
        
        # Load data
        self.books = load_books()
        self._settings = load_settings()
        self.current_cover_path = None
        self._image_refs = {}
        
        # Set appearance from settings
        ctk.set_appearance_mode(self._settings.get("appearance_mode", "dark"))
        
        # Build UI
        self._build_ui()
        self.load_table()
    
    def _build_ui(self):
        """Build the user interface."""
        self._build_left_panel()
        self._build_search_controls()
        self._build_theme_controls()
        self._build_sort_controls()
        self._build_main_area()
        self._build_delete_button()
        self._build_bulk_actions()
    
    def _build_left_panel(self):
        """Build the left input panel."""
        left_frame = ctk.CTkFrame(self, width=260, corner_radius=15)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        ctk.CTkLabel(left_frame, text="Add Book", font=("Arial", 20, "bold")).pack(pady=10)
        
        self.title_var = ctk.CTkEntry(left_frame, placeholder_text="Title")
        self.title_var.pack(pady=10, fill="x")
        
        self.author_var = ctk.CTkEntry(left_frame, placeholder_text="Author")
        self.author_var.pack(pady=10, fill="x")
        
        self.year_var = ctk.CTkEntry(left_frame, placeholder_text="Year")
        self.year_var.pack(pady=10, fill="x")
        
        self.genre_var = ctk.CTkEntry(left_frame, placeholder_text="Genre")
        self.genre_var.pack(pady=10, fill="x")
        
        self.tags_var = ctk.CTkEntry(left_frame, placeholder_text="Tags (comma-separated)")
        self.tags_var.pack(pady=6, fill="x")
        
        ctk.CTkButton(left_frame, text="Upload Cover", command=self.upload_cover).pack(pady=6, fill="x")
        ctk.CTkButton(left_frame, text="Add Book", command=self.add_book).pack(pady=20, fill="x")
    
    def _build_search_controls(self):
        """Build the search bar."""
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill="x", padx=10, pady=5)
        
        self.search_var = ctk.CTkEntry(search_frame, placeholder_text="Search books...")
        self.search_var.pack(side="left", fill="x", expand=True, padx=5, pady=8)
        
        ctk.CTkButton(search_frame, text="Search", width=100, command=self.search_books).pack(side="left", padx=5)
        ctk.CTkButton(search_frame, text="Show All", width=100, command=self.load_table).pack(side="left", padx=5)
    
    def _build_theme_controls(self):
        """Build the theme controls."""
        theme_frame = ctk.CTkFrame(self)
        theme_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(theme_frame, text="Theme:", font=("Arial", 14)).pack(side="left", padx=6)
        
        self.appearance_var = ctk.CTkComboBox(
            theme_frame,
            values=["dark", "light", "system"],
            width=150,
            command=self.change_appearance_mode
        )
        self.appearance_var.set(self._settings.get("appearance_mode", "dark"))
        self.appearance_var.pack(side="left", padx=6)
    
    def _build_sort_controls(self):
        """Build the sorting and filtering controls."""
        sort_frame = ctk.CTkFrame(self)
        sort_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(sort_frame, text="Sort by:", font=("Arial", 14)).pack(side="left", padx=6)
        
        self.sort_var = ctk.CTkComboBox(
            sort_frame,
            values=[
                "Title (A→Z)", "Title (Z→A)",
                "Author (A→Z)", "Author (Z→A)",
                "Year (Old→New)", "Year (New→Old)",
                "Genre (A→Z)", "Genre (Z→A)"
            ],
            width=200,
            command=self.apply_sort
        )
        self.sort_var.pack(side="left", padx=5)
        
        self.tag_filter_var = ctk.CTkComboBox(
            sort_frame,
            values=["All"],
            width=150,
            command=self.apply_tag_filter
        )
        self.tag_filter_var.set("All")
        self.tag_filter_var.pack(side="left", padx=8)
    
    def _build_main_area(self):
        """Build the main table and details area."""
        main_area = ctk.CTkFrame(self)
        main_area.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Table
        table_frame = ctk.CTkFrame(main_area, corner_radius=15)
        table_frame.pack(side="left", fill="both", expand=True, padx=(0, 8), pady=0)
        
        columns = ("Title", "Author", "Year", "Genre")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="extended")
        
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=150)
        
        self.table.pack(fill="both", expand=True, padx=5, pady=5)
        self.table.bind("<<TreeviewSelect>>", self.on_select)
        
        # Details panel
        details_frame = ctk.CTkFrame(main_area, width=240, corner_radius=10)
        details_frame.pack(side="right", fill="y", padx=(8, 0), pady=0)
        
        ctk.CTkLabel(details_frame, text="Details", font=("Arial", 16, "bold")).pack(pady=8)
        
        self.detail_title = ctk.CTkLabel(details_frame, text="Title: -")
        self.detail_title.pack(anchor="w", padx=8, pady=4)
        
        self.detail_author = ctk.CTkLabel(details_frame, text="Author: -")
        self.detail_author.pack(anchor="w", padx=8, pady=4)
        
        self.detail_year = ctk.CTkLabel(details_frame, text="Year: -")
        self.detail_year.pack(anchor="w", padx=8, pady=4)
        
        self.detail_genre = ctk.CTkLabel(details_frame, text="Genre: -")
        self.detail_genre.pack(anchor="w", padx=8, pady=4)
        
        self.detail_tags = ctk.CTkLabel(details_frame, text="Tags: -")
        self.detail_tags.pack(anchor="w", padx=8, pady=4)
        
        self.cover_label = ctk.CTkLabel(details_frame, text="No cover", width=200, height=200)
        self.cover_label.pack(padx=8, pady=8)
    
    def _build_delete_button(self):
        """Build the delete button."""
        ctk.CTkButton(self, text="Delete Selected", command=self.delete_selected, fg_color="red").pack(pady=5)
    
    def _build_bulk_actions(self):
        """Build bulk action buttons."""
        bulk_frame = ctk.CTkFrame(self)
        bulk_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(bulk_frame, text="Select All", width=120, command=self.select_all).pack(side="left", padx=4)
        ctk.CTkButton(bulk_frame, text="Clear Selection", width=120, command=self.clear_selection).pack(side="left", padx=4)
        ctk.CTkButton(bulk_frame, text="Export Selected", width=140, command=self.export_selected).pack(side="left", padx=4)
        ctk.CTkButton(bulk_frame, text="Add Tag to Selected", width=180, command=self.bulk_add_tag).pack(side="left", padx=4)
        ctk.CTkButton(bulk_frame, text="Remove Tag from Selected", width=200, command=self.bulk_remove_tag).pack(side="left", padx=4)
    
    def add_book(self):
        """Add a new book to the collection."""
        title = self.title_var.get().strip()
        author = self.author_var.get().strip()
        year = self.year_var.get().strip()
        genre = self.genre_var.get().strip()
        tags_text = self.tags_var.get().strip()
        tags = [t.strip() for t in tags_text.split(',') if t.strip()] if tags_text else []
        
        if not title or not author or not year:
            messagebox.showwarning("Missing Info", "Title, Author, and Year are required.")
            return
        
        cover_path = None
        if self.current_cover_path:
            cover_path = copy_cover_file(self.current_cover_path)
        
        book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "tags": tags,
            "cover": cover_path
        }
        
        self.books.append(book)
        save_books(self.books)
        self.load_table()
        
        # Clear inputs
        self.title_var.delete(0, "end")
        self.author_var.delete(0, "end")
        self.year_var.delete(0, "end")
        self.genre_var.delete(0, "end")
        self.tags_var.delete(0, "end")
        self.current_cover_path = None
        
        self.update_tag_filter_values()
    
    def load_table(self, filtered=None):
        """Load and display books in the table."""
        for row in self.table.get_children():
            self.table.delete(row)
        
        books_to_show = filtered if filtered else self.books
        for b in books_to_show:
            title = b.get("title", "")
            author = b.get("author", "")
            year = b.get("year", "")
            genre = b.get("genre", "")
            self.table.insert("", "end", values=(title, author, year, genre))
    
    def search_books(self):
        """Search books by title or author."""
        keyword = self.search_var.get()
        results = search_books(self.books, keyword)
        self.load_table(filtered=results)
    
    def apply_sort(self, _):
        """Apply sorting to the table."""
        choice = self.sort_var.get()
        sorted_books = sort_books(self.books, choice)
        self.load_table(filtered=sorted_books)
    
    def upload_cover(self):
        """Open file dialog to upload a cover image."""
        path = filedialog.askopenfilename(
            title="Select cover image",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"), ("All files", "*")]
        )
        if path:
            self.current_cover_path = path
            messagebox.showinfo("Cover Selected", f"Selected cover: {Path(path).name}")
    
    def update_tag_filter_values(self):
        """Update the tag filter dropdown with all available tags."""
        tags = get_all_tags(self.books)
        vals = ["All"] + tags
        self.tag_filter_var.configure(values=vals)
        if self.tag_filter_var.get() not in vals:
            self.tag_filter_var.set("All")
    
    def select_all(self):
        """Select all rows in the table."""
        items = self.table.get_children()
        if items:
            self.table.selection_set(items)
            self.on_select()
    
    def clear_selection(self):
        """Clear the current selection."""
        self.table.selection_remove(self.table.selection())
        self.on_select()
    
    def export_selected(self):
        """Export selected books to a CSV file."""
        sel = self.table.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Select one or more books to export.")
            return
        
        path = filedialog.asksaveasfilename(
            title="Export CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not path:
            return
        
        selected_keys = [tuple(self.table.item(i, "values")) for i in sel]
        rows = [b for b in self.books
                if (b.get("title", ""), b.get("author", ""), 
                    b.get("year", ""), b.get("genre", "")) in selected_keys]
        
        try:
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["title", "author", "year", "genre", "tags", "cover"])
                writer.writeheader()
                for r in rows:
                    writer.writerow({
                        "title": r.get("title", ""),
                        "author": r.get("author", ""),
                        "year": r.get("year", ""),
                        "genre": r.get("genre", ""),
                        "tags": ",".join(r.get("tags", [])),
                        "cover": r.get("cover", "")
                    })
            messagebox.showinfo("Exported", f"Exported {len(rows)} book(s) to {path}")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))
    
    def bulk_add_tag(self):
        """Add a tag to all selected books."""
        sel = self.table.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Select one or more books.")
            return
        
        tag = simpledialog.askstring("Add Tag", "Tag to add to selected books:")
        if not tag:
            return
        
        tag = tag.strip()
        book_keys = {tuple(self.table.item(i, "values")) for i in sel}
        changed = add_tag_to_books(self.books, book_keys, tag)
        
        if changed:
            save_books(self.books)
            self.update_tag_filter_values()
            self.load_table()
        
        messagebox.showinfo("Tag Added", f"Added tag '{tag}' to {changed} book(s)")
    
    def bulk_remove_tag(self):
        """Remove a tag from all selected books."""
        sel = self.table.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Select one or more books.")
            return
        
        tag = simpledialog.askstring("Remove Tag", "Tag to remove from selected books:")
        if not tag:
            return
        
        tag = tag.strip()
        book_keys = {tuple(self.table.item(i, "values")) for i in sel}
        changed = remove_tag_from_books(self.books, book_keys, tag)
        
        if changed:
            save_books(self.books)
            self.update_tag_filter_values()
            self.load_table()
        
        messagebox.showinfo("Tag Removed", f"Removed tag '{tag}' from {changed} book(s)")
    
    def apply_tag_filter(self, _):
        """Filter the table by selected tag."""
        choice = self.tag_filter_var.get()
        filtered = filter_by_tag(self.books, choice)
        self.load_table(filtered=filtered)
    
    def on_select(self, event=None):
        """Update the details panel when a book is selected."""
        sel = self.table.selection()
        if not sel:
            return
        
        if len(sel) > 1:
            self.detail_title.configure(text=f"Selected: {len(sel)} items")
            self.detail_author.configure(text="Author: -")
            self.detail_year.configure(text="Year: -")
            self.detail_genre.configure(text="Genre: -")
            self.detail_tags.configure(text="Tags: -")
            self.cover_label.configure(text="Multiple selection")
            return
        
        vals = self.table.item(sel[0], "values")
        b = next((x for x in self.books 
                  if (x.get('title', ''), x.get('author', ''), 
                      x.get('year', ''), x.get('genre', '')) == tuple(vals)), None)
        
        if not b:
            return
        
        self.detail_title.configure(text=f"Title: {b.get('title', '-')}")
        self.detail_author.configure(text=f"Author: {b.get('author', '-')}")
        self.detail_year.configure(text=f"Year: {b.get('year', '-')}")
        self.detail_genre.configure(text=f"Genre: {b.get('genre', '-')}")
        self.detail_tags.configure(text=f"Tags: {', '.join(b.get('tags', [])) or '-'}")
        
        cover = b.get("cover")
        if cover and Path(cover).exists() and PIL_AVAILABLE:
            try:
                img = Image.open(cover)
                img.thumbnail((200, 200))
                photo = ImageTk.PhotoImage(img)
                self._image_refs['cover'] = photo
                self.cover_label.configure(image=photo, text="")
            except Exception:
                self.cover_label.configure(text="[error loading image]")
        elif cover and Path(cover).exists():
            self.cover_label.configure(text=f"Cover: {Path(cover).name}")
        else:
            self.cover_label.configure(text="No cover")
    
    def change_appearance_mode(self, choice):
        """Change the appearance mode and save the setting."""
        try:
            ctk.set_appearance_mode(choice)
            ctk.set_appearance_mode(ctk.get_appearance_mode())
        except Exception:
            ctk.set_appearance_mode("dark")
        
        settings = load_settings()
        settings["appearance_mode"] = choice
        save_settings(settings)
    
    def delete_selected(self):
        """Delete the selected books."""
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Select one or more books to delete.")
            return
        
        if not messagebox.askyesno("Confirm Delete", f"Delete {len(selected)} selected book(s)?"):
            return
        
        to_remove = {tuple(self.table.item(i, "values")) for i in selected}
        self.books = [b for b in self.books
                      if (b.get("title", ""), b.get("author", ""),
                          b.get("year", ""), b.get("genre", "")) not in to_remove]
        
        save_books(self.books)
        self.load_table()
        self.update_tag_filter_values()
