import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os
import subprocess
import importlib
import sqlite3
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_struct.Bsearch import BinarySearchTree
from data_struct.BookDictionary import BookDictionary
from data_struct.linkedList import BookLinkedList
from data_struct.queue import LibrarySystem
from data_struct.Stacks import ActivityStack
from data_struct.graph import Graphs
from database.sqlite import SQLiteService

class ModernStyle:
    # Color scheme
    PRIMARY = "#2196F3"  # Blue
    SECONDARY = "#FFC107"  # Amber
    SUCCESS = "#4CAF50"  # Green
    DANGER = "#F44336"  # Red
    WARNING = "#FF9800"  # Orange
    INFO = "#00BCD4"  # Cyan
    LIGHT = "#F5F5F5"  # Light Gray
    DARK = "#212121"  # Dark Gray
    
    # Styles
    BUTTON_STYLE = {
        "background": PRIMARY,
        "foreground": "white",
        "font": ("Helvetica", 10),
        "padx": 15,
        "pady": 5,
        "relief": "flat",
        "borderwidth": 0
    }
    
    DANGER_BUTTON = BUTTON_STYLE.copy()
    DANGER_BUTTON["background"] = DANGER
    
    SUCCESS_BUTTON = BUTTON_STYLE.copy()
    SUCCESS_BUTTON["background"] = SUCCESS
    
    WARNING_BUTTON = BUTTON_STYLE.copy()
    WARNING_BUTTON["background"] = WARNING
    
    ENTRY_STYLE = {
        "font": ("Helvetica", 10),
        "relief": "solid",
        "borderwidth": 1
    }
    
    HEADING_STYLE = {
        "font": ("Helvetica", 12, "bold"),
        "foreground": DARK
    }

    LIGHT = "#f5f5f5"
    DARK = "#333333"
    PRIMARY = "#2196f3"
    SUCCESS = "#4caf50"
    WARNING = "#ff9800"
    DANGER = "#f44336"
    INFO = "#00bcd4"

    BUTTON_STYLE = {
        "bg": LIGHT,
        "fg": DARK,
        "font": ("Helvetica", 10),
        "relief": tk.RAISED,
        "cursor": "hand2"
    }

    SUCCESS_BUTTON = {
        **BUTTON_STYLE,
        "bg": SUCCESS,
        "fg": LIGHT
    }

    WARNING_BUTTON = {
        **BUTTON_STYLE,
        "bg": WARNING,
        "fg": LIGHT
    }

    DANGER_BUTTON = {
        **BUTTON_STYLE,
        "bg": DANGER,
        "fg": LIGHT
    }

    INFO_BUTTON = {
        **BUTTON_STYLE,
        "bg": INFO,
        "fg": LIGHT
    }

class IntegratedLibraryGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📚 Library Management System")
        self.geometry("1400x900")
        self.configure(bg=ModernStyle.LIGHT)
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure("Modern.TButton",
                           font=("Helvetica", 10),
                           padding=5)
        self.style.configure("Modern.TEntry",
                           padding=5)
        self.style.configure("Modern.TLabel",
                           font=("Helvetica", 10))
        self.style.configure("Title.TLabel",
                           font=("Helvetica", 14, "bold"))
        
        # Initialize all data structures
        self.bst = BinarySearchTree(log_fn=self._log)
        self.book_dict = BookDictionary()
        self.linked_list = BookLinkedList()
        self.queue_system = LibrarySystem()
        self.activity_stack = ActivityStack()
        self.book_graph = Graphs()  # Initialize graph
        self.storage = self._init_database()

        # Create main interface
        self.create_main_interface()

        # Load existing data
        self._load_existing_data()

    def _init_database(self):
        """Initialize database with proper book schema"""
        storage = SQLiteService("integrated_library.db")
        # Create books table if not exists
        storage.conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isbn TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                status TEXT DEFAULT 'Available'
            )
        """)
        storage.conn.commit()
        return storage

    def _log(self, msg):
        """Enhanced logging with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {msg}"
        self.log_text.insert(tk.END, log_msg + "\n")
        self.log_text.see(tk.END)

    def create_main_interface(self):
        """Create the main tabbed interface"""
        # Create header
        header = ttk.Frame(self)
        header.pack(fill=tk.X, padx=20, pady=10)
        
        title = ttk.Label(header, 
                         text="Library Management System",
                         style="Title.TLabel")
        title.pack(side=tk.LEFT)
        
        # Create notebook with modern styling
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Create tabs
        self.create_book_management_tab()
        self.create_search_operations_tab()
        self.create_checkout_system_tab()
        self.create_data_structures_tab()

    def create_book_management_tab(self):
        """Main book management operations"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📚 Books")

        # Input section with modern styling
        input_frame = ttk.LabelFrame(frame, text="Add/Edit Book", padding=15)
        input_frame.pack(fill=tk.X, padx=20, pady=10)

        # Grid layout for inputs
        grid = ttk.Frame(input_frame)
        grid.pack(fill=tk.X, pady=10)

        # ISBN input
        ttk.Label(grid, text="ISBN:", style="Modern.TLabel").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.isbn_var = tk.StringVar()
        isbn_entry = ttk.Entry(grid, textvariable=self.isbn_var, width=30, style="Modern.TEntry")
        isbn_entry.grid(row=0, column=1, padx=5, pady=5)

        # Title input
        ttk.Label(grid, text="Title:", style="Modern.TLabel").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.title_var = tk.StringVar()
        title_entry = ttk.Entry(grid, textvariable=self.title_var, width=40, style="Modern.TEntry")
        title_entry.grid(row=0, column=3, padx=5, pady=5)

        # Author input
        ttk.Label(grid, text="Author:", style="Modern.TLabel").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.author_var = tk.StringVar()
        author_entry = ttk.Entry(grid, textvariable=self.author_var, width=40, style="Modern.TEntry")
        author_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        # Button frame with modern styling
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(pady=10)

        # Modern styled buttons
        add_btn = tk.Button(button_frame, text="Add Book", **ModernStyle.SUCCESS_BUTTON)
        add_btn.pack(side=tk.LEFT, padx=5)
        add_btn.config(command=self.add_book)

        update_btn = tk.Button(button_frame, text="Update Book", **ModernStyle.WARNING_BUTTON)
        update_btn.pack(side=tk.LEFT, padx=5)
        update_btn.config(command=self.update_book)

        delete_btn = tk.Button(button_frame, text="Delete Book", **ModernStyle.DANGER_BUTTON)
        delete_btn.pack(side=tk.LEFT, padx=5)
        delete_btn.config(command=self.delete_book)

        clear_btn = tk.Button(button_frame, text="Clear Fields", **ModernStyle.BUTTON_STYLE)
        clear_btn.pack(side=tk.LEFT, padx=5)
        clear_btn.config(command=self.clear_fields)

        # Books display with modern styling
        display_frame = ttk.LabelFrame(frame, text="Book Collection", padding=15)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Configure modern Treeview
        style = ttk.Style()
        style.configure("Modern.Treeview",
                       background=ModernStyle.LIGHT,
                       foreground=ModernStyle.DARK,
                       rowheight=25,
                       fieldbackground=ModernStyle.LIGHT)
        style.configure("Modern.Treeview.Heading",
                       font=('Helvetica', 10, 'bold'))

        # Treeview for books
        columns = ("ISBN", "Title", "Author", "Status")
        self.books_tree = ttk.Treeview(display_frame, columns=columns, show="headings",
                                      height=15, style="Modern.Treeview")

        for col in columns:
            self.books_tree.heading(col, text=col)
            self.books_tree.column(col, width=150)

        # Modern scrollbar
        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL,
                                command=self.books_tree.yview)
        self.books_tree.configure(yscrollcommand=scrollbar.set)

        self.books_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind selection event
        self.books_tree.bind('<<TreeviewSelect>>', self.books_tree_select)

        # Modern status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(frame, textvariable=self.status_var,
                             style="Modern.TLabel", padding=5)
        status_bar.pack(fill=tk.X, padx=20, pady=5)

        # Similar Books Section
        similar_frame = ttk.LabelFrame(input_frame, text="Similar Books", padding=10)
        similar_frame.pack(fill=tk.X, pady=10)

        # Dropdown for selecting similar books
        ttk.Label(similar_frame, text="Connect with:").pack(side=tk.LEFT, padx=5)
        self.similar_var = tk.StringVar()
        self.similar_combo = ttk.Combobox(similar_frame, textvariable=self.similar_var, width=30)
        self.similar_combo.pack(side=tk.LEFT, padx=5)
        # Bind selection event
        self.similar_combo.bind('<<ComboboxSelected>>', self.on_book_selected)
        
        connect_btn = tk.Button(similar_frame, text="Connect Books", 
                              command=self.connect_similar_books,
                              **ModernStyle.INFO_BUTTON)
        connect_btn.pack(side=tk.LEFT, padx=5)

        # Recommendations Section
        recommendations_frame = ttk.LabelFrame(input_frame, text="Book Recommendations", padding=10)
        recommendations_frame.pack(fill=tk.X, pady=10)
        
        self.recommendations_text = tk.Text(recommendations_frame, height=5, width=40)
        self.recommendations_text.pack(fill=tk.X, pady=5)

    def create_search_operations_tab(self):
        """Search operations using different data structures"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔍 Search")

        # Search controls with modern styling
        search_frame = ttk.LabelFrame(frame, text="Search Options", padding=15)
        search_frame.pack(fill=tk.X, padx=20, pady=10)

        # Search input grid
        grid = ttk.Frame(search_frame)
        grid.pack(fill=tk.X, pady=10)

        ttk.Label(grid, text="Search Term:", style="Modern.TLabel").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(grid, textvariable=self.search_var, width=40, style="Modern.TEntry")
        search_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(grid, text="Search By:", style="Modern.TLabel").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.search_type = ttk.Combobox(grid, values=["ISBN", "Title", "Author"], width=15, style="Modern.TCombobox")
        self.search_type.grid(row=0, column=3, padx=5, pady=5)
        self.search_type.set("Title")

        # Search buttons with modern styling
        button_frame = ttk.Frame(search_frame)
        button_frame.pack(pady=10)

        bst_btn = tk.Button(button_frame, text="BST Search", **ModernStyle.BUTTON_STYLE)
        bst_btn.pack(side=tk.LEFT, padx=5)
        bst_btn.config(command=self.bst_search)

        dict_btn = tk.Button(button_frame, text="Dictionary Search", **ModernStyle.BUTTON_STYLE)
        dict_btn.pack(side=tk.LEFT, padx=5)
        dict_btn.config(command=self.dict_search)

        linked_btn = tk.Button(button_frame, text="Linked List Search", **ModernStyle.BUTTON_STYLE)
        linked_btn.pack(side=tk.LEFT, padx=5)
        linked_btn.config(command=self.linked_search)

        # Search results with modern styling
        results_frame = ttk.LabelFrame(frame, text="Search Results", padding=15)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.search_results = scrolledtext.ScrolledText(
            results_frame, 
            height=20, 
            wrap=tk.WORD,
            font=("Helvetica", 10),
            bg=ModernStyle.LIGHT,
            relief="solid",
            borderwidth=1
        )
        self.search_results.pack(fill=tk.BOTH, expand=True)

    def create_checkout_system_tab(self):
        """Checkout system using queue"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📋 Checkout")

        # Checkout controls with modern styling
        checkout_frame = ttk.LabelFrame(frame, text="Checkout/Return Books", padding=15)
        checkout_frame.pack(fill=tk.X, padx=20, pady=10)

        # Input grid
        grid = ttk.Frame(checkout_frame)
        grid.pack(fill=tk.X, pady=10)

        # ISBN input with tooltip
        isbn_frame = ttk.Frame(grid)
        isbn_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
        ttk.Label(isbn_frame, text="ISBN:", style="Modern.TLabel").pack(side=tk.LEFT)
        isbn_tooltip = ttk.Label(isbn_frame, text="ℹ️", cursor="question_arrow")
        isbn_tooltip.pack(side=tk.LEFT, padx=2)
        self.create_tooltip(isbn_tooltip, "Enter the 13-digit ISBN number of the book")
        
        self.checkout_book_var = tk.StringVar()
        checkout_entry = ttk.Entry(grid, textvariable=self.checkout_book_var, width=30, style="Modern.TEntry")
        checkout_entry.grid(row=0, column=2, padx=5, pady=5)

        # Username input with tooltip
        username_frame = ttk.Frame(grid)
        username_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
        ttk.Label(username_frame, text="Username:", style="Modern.TLabel").pack(side=tk.LEFT)
        username_tooltip = ttk.Label(username_frame, text="ℹ️", cursor="question_arrow")
        username_tooltip.pack(side=tk.LEFT, padx=2)
        self.create_tooltip(username_tooltip, "Enter the borrower's username (e.g., 'john_smith')")

        self.user_var = tk.StringVar()
        user_entry = ttk.Entry(grid, textvariable=self.user_var, width=30, style="Modern.TEntry")
        user_entry.grid(row=1, column=2, padx=5, pady=5)

        # Example label
        ttk.Label(grid, text="Example: john_smith", foreground="gray", style="Modern.TLabel").grid(
            row=2, column=2, padx=5, sticky=tk.W)

        # Checkout buttons with modern styling
        button_frame = ttk.Frame(checkout_frame)
        button_frame.pack(pady=10)

        checkout_btn = tk.Button(button_frame, text="Checkout Book", **ModernStyle.SUCCESS_BUTTON)
        checkout_btn.pack(side=tk.LEFT, padx=5)
        checkout_btn.config(command=self.checkout_book)

        return_btn = tk.Button(button_frame, text="Return Book", **ModernStyle.WARNING_BUTTON)
        return_btn.pack(side=tk.LEFT, padx=5)
        return_btn.config(command=self.return_book)

        # Queue display
        queue_frame = ttk.LabelFrame(frame, text="Current Checkouts and Waitlist", padding=15)
        queue_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.queue_display = scrolledtext.ScrolledText(
            queue_frame,
            height=15,
            wrap=tk.WORD,
            font=("Helvetica", 10),
            bg=ModernStyle.LIGHT
        )
        self.queue_display.pack(fill=tk.BOTH, expand=True)

    def create_data_structures_tab(self):
        """Data structures visualization and logs"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔧 Visualizer")

        # Create visualization canvas with modern styling
        canvas_frame = ttk.LabelFrame(frame, text="Data Structure Visualization", padding=15)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.viz_canvas = tk.Canvas(
            canvas_frame, 
            width=600, 
            height=300, 
            bg=ModernStyle.LIGHT,
            relief="solid",
            borderwidth=1
        )
        self.viz_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Control panel for visualization with modern styling
        control_frame = ttk.Frame(canvas_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(control_frame, text="Visualize:", style="Modern.TLabel").pack(side=tk.LEFT, padx=5)
        self.viz_type = ttk.Combobox(
            control_frame, 
            values=["BST", "Stack", "Queue", "Linked List"],
            width=15,
            style="Modern.TCombobox"
        )
        self.viz_type.pack(side=tk.LEFT, padx=5)
        self.viz_type.set("BST")
        self.viz_type.bind('<<ComboboxSelected>>', self.update_visualization)
        
        refresh_btn = tk.Button(
            control_frame, 
            text="Refresh View", 
            **ModernStyle.BUTTON_STYLE
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        refresh_btn.config(command=self.update_visualization)
        
        # Statistics frame with modern styling
        stats_frame = ttk.LabelFrame(frame, text="Collection Statistics", padding=15)
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.stats_text = tk.Text(
            stats_frame, 
            height=8, 
            wrap=tk.WORD,
            font=("Helvetica", 10),
            bg=ModernStyle.LIGHT,
            relief="solid",
            borderwidth=1
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Activity log with modern styling
        log_frame = ttk.LabelFrame(frame, text="Activity Log", padding=15)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame, 
            height=15, 
            wrap=tk.WORD,
            font=("Helvetica", 10),
            bg=ModernStyle.LIGHT,
            relief="solid",
            borderwidth=1
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Log controls with modern styling
        log_controls = ttk.Frame(log_frame)
        log_controls.pack(fill=tk.X, pady=5)
        
        clear_btn = tk.Button(
            log_controls, 
            text="Clear Log", 
            **ModernStyle.DANGER_BUTTON
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        clear_btn.config(command=self.clear_log)
        
        save_btn = tk.Button(
            log_controls, 
            text="Save Log", 
            **ModernStyle.SUCCESS_BUTTON
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        save_btn.config(command=self.save_log)

    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = ttk.Label(tooltip, text=text, background=ModernStyle.LIGHT,
                            relief="solid", borderwidth=1)
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            widget.tooltip = tooltip
            widget.bind("<Leave>", lambda e: hide_tooltip())
            tooltip.bind("<Leave>", lambda e: hide_tooltip())
        
        widget.bind("<Enter>", show_tooltip)

    # Event handlers
    def on_book_select(self, event):
        """Handle book selection in treeview"""
        selection = self.books_tree.selection()
        if selection:
            item = self.books_tree.item(selection[0])
            values = item['values']
            if values:
                self.isbn_var.set(values[0])
                self.title_var.set(values[1])
                self.author_var.set(values[2])

    def clear_fields(self):
        """Clear all input fields"""
        self.isbn_var.set("")
        self.title_var.set("")
        self.author_var.set("")
        self.search_var.set("")
        self.checkout_book_var.set("")
        self.user_var.set("")

    def add_book(self):
        """Add a new book"""
        isbn = self.isbn_var.get().strip()
        title = self.title_var.get().strip()
        author = self.author_var.get().strip()
        
        if not all([isbn, title, author]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            # Add to database and data structures
            self.storage.conn.execute(
                "INSERT INTO books (isbn, title, author) VALUES (?, ?, ?)",
                (isbn, title, author)
            )
            self.storage.conn.commit()
            
            # Update all data structures
            self.bst.insert(isbn, {"title": title, "author": author})
            self.book_dict.add_book(isbn, title, author)
            self.linked_list.add_book(title, author, isbn)
            self.book_graph.add_book_node(title)  # Add to graph
            
            self._log(f"Added book: {title} (ISBN: {isbn})")
            self.refresh_books_display()
            self.refresh_similar_books_combo()  # Update similar books dropdown
            self.clear_fields()
            
            # Update visualization if BST is selected
            if self.viz_type.get() == "BST":
                self.update_visualization()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "ISBN already exists!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_book(self):
        """Update selected book"""
        selection = self.books_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a book to update")
            return

        isbn = self.isbn_var.get().strip()
        title = self.title_var.get().strip()
        author = self.author_var.get().strip()

        if not all([isbn, title, author]):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            # Update in database
            cursor = self.storage.conn.cursor()
            cursor.execute("UPDATE books SET title=?, author=? WHERE isbn=?",
                           (title, author, isbn))
            self.storage.conn.commit()

            # Update in data structures (simplified approach)
            self._reload_data_structures()

            self._log(f"Updated book: {title} by {author} (ISBN: {isbn})")
            self.refresh_books_display()
            self.status_var.set("Book updated successfully")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update book: {str(e)}")

    def delete_book(self):
        """Delete selected book"""
        selection = self.books_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a book to delete!")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this book?"):
            item = self.books_tree.item(selection[0])
            isbn = item['values'][0]
            title = item['values'][1]
            
            try:
                # Start transaction
                cursor = self.storage.conn.cursor()
                
                # First verify the book exists
                cursor.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
                if not cursor.fetchone():
                    raise Exception("Book not found in database")
                
                # Delete from database
                cursor.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
                
                # Delete from data structures
                try:
                    self.bst.delete(isbn)
                except Exception as e:
                    self._log(f"Warning: BST deletion failed for ISBN {isbn}: {str(e)}")
                    
                try:
                    if not self.book_dict.delete_book(isbn):
                        self._log(f"Warning: Dictionary deletion failed for ISBN {isbn}")
                except Exception as e:
                    self._log(f"Warning: Dictionary deletion error for ISBN {isbn}: {str(e)}")
                    
                try:
                    result = self.linked_list.delete_book(isbn)
                    if result == "Book not found":
                        self._log(f"Warning: Linked list deletion failed for ISBN {isbn}")
                except Exception as e:
                    self._log(f"Warning: Linked list deletion error for ISBN {isbn}: {str(e)}")

                # Remove from graph
                try:
                    self.book_graph.remove_book(title)
                except Exception as e:
                    self._log(f"Warning: Graph deletion error for title {title}: {str(e)}")
                
                # Commit database changes
                self.storage.conn.commit()
                
                self._log(f"Deleted book: {title} (ISBN: {isbn})")
                self.refresh_books_display()
                self.refresh_similar_books_combo()  # Update similar books dropdown
                self.clear_fields()
                
                # Update visualization based on current view
                self.update_visualization()
                
            except Exception as e:
                # Rollback on error
                self.storage.conn.rollback()
                error_msg = str(e)
                self._log(f"Error deleting book: {error_msg}")
                messagebox.showerror("Error", f"Failed to delete book: {error_msg}")
                # Try to recover data structure consistency
                self._reload_data_structures()

    def bst_search(self):
        """Search using BST"""
        search_term = self.search_var.get().strip()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term")
            return

        self.search_results.delete(1.0, tk.END)
        self.search_results.insert(tk.END, "BST Search Results:\n" + "=" * 50 + "\n")

        found_count = 0
        for key, (title, author, isbn) in self.bst.inorder():
            if (self.search_type.get() == "Title" and search_term.lower() in title.lower()) or \
                    (self.search_type.get() == "Author" and search_term.lower() in author.lower()) or \
                    (self.search_type.get() == "ISBN" and search_term in isbn):
                self.search_results.insert(tk.END, f"ID: {key}\nTitle: {title}\nAuthor: {author}\nISBN: {isbn}\n\n")
                found_count += 1

        if found_count == 0:
            self.search_results.insert(tk.END, "No books found matching your search.\n")
        else:
            self.search_results.insert(tk.END, f"Found {found_count} book(s).")

        self._log(f"BST search for '{search_term}' returned {found_count} results")

    def dict_search(self):
        """Search using dictionary"""
        search_term = self.search_var.get().strip()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term")
            return

        self.search_results.delete(1.0, tk.END)
        self.search_results.insert(tk.END, "Dictionary Search Results:\n" + "=" * 50 + "\n")

        if self.search_type.get() == "ISBN":
            book = self.book_dict.search_by_isbn(search_term)
            if book:
                self.search_results.insert(tk.END,
                                           f"Title: {book['title']}\nAuthor: {book['author']}\nISBN: {book['isbn']}\nStatus: {'Available' if book['available'] else 'Checked Out'}\n")
                self._log(f"Dictionary search found book by ISBN: {search_term}")
            else:
                self.search_results.insert(tk.END, "No book found with that ISBN.\n")
        elif self.search_type.get() == "Title":
            books = self.book_dict.search_by_title(search_term)
            if books:
                for book in books:
                    self.search_results.insert(tk.END,
                                               f"Title: {book['title']}\nAuthor: {book['author']}\nISBN: {book['isbn']}\n\n")
                self._log(f"Dictionary search found {len(books)} books by title")
            else:
                self.search_results.insert(tk.END, "No books found with that title.\n")
        else:
            self.search_results.insert(tk.END, "Dictionary search only supports ISBN and Title searches.\n")

    def linked_search(self):
        """Search using linked list"""
        search_term = self.search_var.get().strip()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term")
            return

        self.search_results.delete(1.0, tk.END)
        self.search_results.insert(tk.END, "Linked List Search Results:\n" + "=" * 50 + "\n")

        if self.search_type.get() == "Title":
            book = self.linked_list.search_by_title(search_term)
            if book:
                self.search_results.insert(tk.END,
                                           f"Title: {book.title}\nAuthor: {book.author}\nISBN: {book.isbn}\nAvailable: {book.available}\n")
                self._log(f"Linked list search found book: {search_term}")
            else:
                self.search_results.insert(tk.END, "No book found with that title.\n")
        else:
            self.search_results.insert(tk.END, "Linked list search only supports Title searches.\n")

    def checkout_book(self):
        """Checkout a book"""
        book_id = self.checkout_book_var.get().strip()
        user_id = self.user_var.get().strip()
        
        if not all([book_id, user_id]):
            messagebox.showerror("Error", "Book ID and User ID are required!")
            return
        
        try:
            result = self.queue_system.check_out_book(user_id, book_id)
            if result:
                self._log(f"Book {book_id} checked out to {user_id}")
            else:
                self._log(f"Book {book_id} not available - {user_id} added to queue")
                
            self.clear_fields()
            self.view_queue_status()
            
            # Update visualization if Queue is selected
            if self.viz_type.get() == "Queue":
                self.update_visualization()
                
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def return_book(self):
        """Return a book"""
        book_id = self.checkout_book_var.get().strip()
        user_id = self.user_var.get().strip()
        
        if not all([book_id, user_id]):
            messagebox.showerror("Error", "Book ID and User ID are required!")
            return
        
        try:
            self.queue_system.return_book(book_id, user_id)
            self._log(f"Book {book_id} returned by {user_id}")
            self.clear_fields()
            self.view_queue_status()
            
            # Update visualization if Queue is selected
            if self.viz_type.get() == "Queue":
                self.update_visualization()
                
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_queue_status(self):
        """Display queue status"""
        self.queue_display.delete(1.0, tk.END)
        self.queue_display.insert(tk.END, "Queue Status:\n" + "=" * 50 + "\n")

        for book_id, book_info in self.queue_system.books.items():
            self.queue_display.insert(tk.END, f"Book ID: {book_id}\n")
            self.queue_display.insert(tk.END, f"Title: {book_info['title']}\n")
            self.queue_display.insert(tk.END, f"Available Copies: {book_info['available_copies']}\n")
            self.queue_display.insert(tk.END, f"Checked Out To: {book_info['checked_out_to']}\n")
            self.queue_display.insert(tk.END, f"Reservation Queue: {list(book_info['reservation_queue'])}\n")
            self.queue_display.insert(tk.END, "-" * 30 + "\n")

    def refresh_statistics(self):
        """Refresh statistics display"""
        self.stats_text.delete(1.0, tk.END)

        # Get counts
        cursor = self.storage.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM books")
        total_books = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM books WHERE status='Available'")
        available_books = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM books WHERE status='Checked Out'")
        checked_out_books = cursor.fetchone()[0]

        # BST statistics
        bst_nodes = len(list(self.bst.inorder()))

        # Linked list statistics
        linked_list_books = len(self.linked_list.get_all_books())

        # Dictionary statistics
        dict_books = len(self.book_dict.get_all_books())

        stats = f"""Library Statistics:
{"=" * 50}
Total Books in Database: {total_books}
Available Books: {available_books}
Checked Out Books: {checked_out_books}

Data Structure Statistics:
BST Nodes: {bst_nodes}
Linked List Books: {linked_list_books}
Dictionary Books: {dict_books}

System Status: All data structures synchronized
Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        self.stats_text.insert(tk.END, stats)

    def show_bst_traversal(self):
        """Show BST inorder traversal"""
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, "BST Inorder Traversal:\n" + "=" * 50 + "\n")

        for key, (title, author, isbn) in self.bst.inorder():
            self.stats_text.insert(tk.END, f"ID: {key} | {title} by {author}\n")

    def show_linked_list(self):
        """Show linked list contents"""
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, "Linked List Contents:\n" + "=" * 50 + "\n")

        books = self.linked_list.get_all_books()
        for i, book in enumerate(books, 1):
            self.stats_text.insert(tk.END, f"{i}. {book['title']} by {book['author']} (ISBN: {book['isbn']})\n")

    def clear_log(self):
        """Clear activity log"""
        self.log_text.delete(1.0, tk.END)
        self._log("Activity log cleared")

    def save_log(self):
        """Save activity log to file"""
        try:
            with open("library_activity.log", "w") as f:
                f.write(self.log_text.get(1.0, tk.END))
            messagebox.showinfo("Success", "Activity log saved to library_activity.log")
            self._log("Activity log saved to file")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save log: {str(e)}")

    def refresh_books_display(self):
        """Refresh the books treeview"""
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)

        cursor = self.storage.conn.cursor()
        cursor.execute("SELECT isbn, title, author, status FROM books ORDER BY title")

        for row in cursor.fetchall():
            self.books_tree.insert("", tk.END, values=row)

    def _load_existing_data(self):
        """Load existing data from database"""
        try:
            cursor = self.storage.conn.cursor()
            cursor.execute("SELECT id, isbn, title, author, status FROM books")
            books = cursor.fetchall()

            for book_id, isbn, title, author, status in books:
                # Add to data structures
                self.bst.insert(isbn, (title, author, isbn))
                self.book_dict.add_book(isbn, title, author)
                self.linked_list.add_book(title, author, isbn)
                self.queue_system.add_book(str(book_id), title, 1)
                self.book_graph.add_book_node(title)  # Add to graph

            self.refresh_books_display()
            self.refresh_similar_books_combo()  # Update similar books dropdown
            self.refresh_statistics()
            self._log(f"Loaded {len(books)} books from database")

        except Exception as e:
            self._log(f"Error loading data: {str(e)}")

    def _reload_data_structures(self):
        """Reload all data structures from database"""
        # Clear existing data structures
        self.bst = BinarySearchTree(log_fn=self._log)
        self.book_dict = BookDictionary()
        self.linked_list = BookLinkedList()
        self.queue_system = LibrarySystem()
        self.book_graph = Graphs()  # Reset graph

        # Reload from database
        self._load_existing_data()

    def update_visualization(self, event=None):
        """Update the visualization based on selected data structure"""
        self.viz_canvas.delete("all")
        viz_type = self.viz_type.get()
        
        if viz_type == "BST":
            self._visualize_bst()
        elif viz_type == "Stack":
            self._visualize_stack()
        elif viz_type == "Queue":
            self._visualize_queue()
        elif viz_type == "Linked List":
            self._visualize_linked_list()

    def _visualize_bst(self):
        """Visualize Binary Search Tree"""
        def draw_node(node, x, y, dx):
            if not node:
                return
            # Draw node
            self.viz_canvas.create_oval(x-20, y-20, x+20, y+20, fill='lightblue')
            self.viz_canvas.create_text(x, y, text=str(node.key))
            
            # Draw left child
            if node.left:
                new_x = x - dx
                new_y = y + 60
                self.viz_canvas.create_line(x, y+20, new_x, new_y-20)
                draw_node(node.left, new_x, new_y, dx/2)
                
            # Draw right child
            if node.right:
                new_x = x + dx
                new_y = y + 60
                self.viz_canvas.create_line(x, y+20, new_x, new_y-20)
                draw_node(node.right, new_x, new_y, dx/2)
        
        # Start drawing from root
        if self.bst.root:
            draw_node(self.bst.root, 300, 50, 150)
        else:
            self.viz_canvas.create_text(300, 150, text="Empty BST")

    def _visualize_stack(self):
        """Visualize Stack"""
        y = 250  # Start from bottom
        current = self.activity_stack.top
        count = 0
        
        while current and count < 6:  # Show top 6 items
            # Draw box
            self.viz_canvas.create_rectangle(200, y-30, 400, y, fill='lightgreen')
            # Draw text
            self.viz_canvas.create_text(300, y-15, text=f"{current.action}: {current.details[:20]}...")
            y -= 40
            current = current.next
            count += 1
        
        if not self.activity_stack.top:
            self.viz_canvas.create_text(300, 150, text="Empty Stack")

    def _visualize_queue(self):
        """Visualize Queue"""
        x = 50  # Start from left
        count = 0
        
        # Get all books with queues
        queued_books = []
        for book_id, book in self.queue_system.books.items():
            if book['reservation_queue']:
                queued_books.append({
                    'id': book_id,
                    'title': book['title'],
                    'queue': list(book['reservation_queue'])
                })
        
        if queued_books:
            for book in queued_books[:6]:  # Show first 6 queued books
                # Draw box
                self.viz_canvas.create_rectangle(x, 120, x+100, 180, fill='lightpink')
                # Draw text
                self.viz_canvas.create_text(x+50, 140, text=book['title'][:10])
                self.viz_canvas.create_text(x+50, 160, text=f"Queue: {len(book['queue'])}")
                x += 120
                count += 1
        else:
            self.viz_canvas.create_text(300, 150, text="No Books in Queue")

    def _visualize_linked_list(self):
        """Visualize Linked List"""
        x = 50  # Start from left
        current = self.linked_list.head
        count = 0
        
        while current and count < 5:  # Show first 5 items
            # Draw node
            self.viz_canvas.create_oval(x-30, 120, x+30, 180, fill='lightyellow')
            # Draw text
            self.viz_canvas.create_text(x, 150, text=current.title[:10])
            
            # Draw arrow if there's a next node
            if current.next and count < 4:
                self.viz_canvas.create_line(x+30, 150, x+90, 150, arrow=tk.LAST)
            
            x += 120
            current = current.next
            count += 1
        
        if not self.linked_list.head:
            self.viz_canvas.create_text(300, 150, text="Empty Linked List")

    def connect_similar_books(self):
        """Connect two books as similar in the graph"""
        selected = self.books_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book first!")
            return

        similar_book = self.similar_var.get()
        if not similar_book:
            messagebox.showwarning("Warning", "Please select a similar book!")
            return

        item = self.books_tree.item(selected[0])
        current_book = item['values'][1]  # Get title of selected book

        if current_book == similar_book:
            messagebox.showwarning("Warning", "Cannot connect a book to itself!")
            return

        self.book_graph.add_edge(current_book, similar_book)
        self._log(f"Connected similar books: {current_book} ↔ {similar_book}")
        self.show_recommendations(current_book)

    def on_book_selected(self, event=None):
        """Handle book selection from dropdown"""
        selected_book = self.similar_var.get()
        if selected_book:
            self.show_recommendations(selected_book)

    def show_recommendations(self, title):
        """Show book recommendations in the text widget"""
        recommendations = self.book_graph.get_recommendations(title)
        self.recommendations_text.delete(1.0, tk.END)
        
        if recommendations:
            self.recommendations_text.insert(tk.END, f"Recommended Books for '{title}':\n")
            self.recommendations_text.insert(tk.END, "=" * 40 + "\n")
            for i, book in enumerate(recommendations, 1):
                self.recommendations_text.insert(tk.END, f"{i}. {book}\n")
        else:
            self.recommendations_text.insert(tk.END, f"No recommendations available for '{title}'.\n")
            self.recommendations_text.insert(tk.END, "Connect this book with similar books to get recommendations.")

    def refresh_similar_books_combo(self):
        """Update the similar books dropdown"""
        all_books = self.book_graph.get_all_books()
        self.similar_combo['values'] = all_books
        
        # If there's a currently selected book in the tree, show its recommendations
        selection = self.books_tree.selection()
        if selection:
            item = self.books_tree.item(selection[0])
            title = item['values'][1]  # Get title
            self.show_recommendations(title)

    def books_tree_select(self, event=None):
        """Handle book selection in the main tree view"""
        selection = self.books_tree.selection()
        if selection:
            item = self.books_tree.item(selection[0])
            title = item['values'][1]  # Get title
            self.show_recommendations(title)


if __name__ == "__main__":
    app = IntegratedLibraryGUI()
    app.mainloop()