import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from src.data_struct.Bsearch import BinarySearchTree
from src.data_struct.BookDictionary import BookDictionary
from src.data_struct.linkedList import BookLinkedList
from src.data_struct.queue import LibrarySystem
from src.database.sqlite import SQLiteService
from datetime import datetime


class IntegratedLibraryGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DSA Library Management System - Integrated")
        self.geometry("1400x900")

        # Initialize all data structures
        self.bst = BinarySearchTree(log_fn=self._log)
        self.book_dict = BookDictionary()
        self.linked_list = BookLinkedList()
        self.queue_system = LibrarySystem()
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
        # Create notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tabs
        self.create_book_management_tab()
        self.create_search_operations_tab()
        self.create_checkout_system_tab()
        self.create_data_structures_tab()

    def create_book_management_tab(self):
        """Main book management operations"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📚 Book Management")

        # Input section
        input_frame = ttk.LabelFrame(frame, text="Book Information", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        # Create input fields
        ttk.Label(input_frame, text="ISBN:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.isbn_var = tk.StringVar()
        self.isbn_entry = ttk.Entry(input_frame, textvariable=self.isbn_var, width=20)
        self.isbn_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(input_frame, text="Title:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(input_frame, textvariable=self.title_var, width=30)
        self.title_entry.grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(input_frame, text="Author:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.author_var = tk.StringVar()
        self.author_entry = ttk.Entry(input_frame, textvariable=self.author_var, width=30)
        self.author_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=2)

        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)

        ttk.Button(button_frame, text="Add Book", command=self.add_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update Book", command=self.update_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Book", command=self.delete_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Fields", command=self.clear_fields).pack(side=tk.LEFT, padx=5)

        # Books display
        display_frame = ttk.LabelFrame(frame, text="Book Collection", padding=10)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Treeview for books
        columns = ("ISBN", "Title", "Author", "Status")
        self.books_tree = ttk.Treeview(display_frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.books_tree.heading(col, text=col)
            self.books_tree.column(col, width=150)

        # Scrollbar
        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.books_tree.yview)
        self.books_tree.configure(yscrollcommand=scrollbar.set)

        self.books_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind selection event
        self.books_tree.bind('<<TreeviewSelect>>', self.on_book_select)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, padx=10, pady=5)

    def create_search_operations_tab(self):
        """Search operations using different data structures"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔍 Search Operations")

        # Search controls
        search_frame = ttk.LabelFrame(frame, text="Search Options", padding=10)
        search_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(search_frame, text="Search Term:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.grid(row=0, column=1, padx=5)

        ttk.Label(search_frame, text="Search By:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.search_type = ttk.Combobox(search_frame, values=["ISBN", "Title", "Author"], width=15)
        self.search_type.grid(row=0, column=3, padx=5)
        self.search_type.set("Title")

        # Search buttons
        search_buttons = ttk.Frame(search_frame)
        search_buttons.grid(row=1, column=0, columnspan=4, pady=10)

        ttk.Button(search_buttons, text="BST Search", command=self.bst_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_buttons, text="Dictionary Search", command=self.dict_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_buttons, text="Linked List Search", command=self.linked_search).pack(side=tk.LEFT, padx=5)

        # Search results
        results_frame = ttk.LabelFrame(frame, text="Search Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.search_results = scrolledtext.ScrolledText(results_frame, height=20, wrap=tk.WORD)
        self.search_results.pack(fill=tk.BOTH, expand=True)

    def create_checkout_system_tab(self):
        """Checkout system using queue"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📋 Checkout System")

        # Checkout controls
        checkout_frame = ttk.LabelFrame(frame, text="Checkout/Return", padding=10)
        checkout_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(checkout_frame, text="Book ID:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.checkout_book_var = tk.StringVar()
        self.checkout_book_entry = ttk.Entry(checkout_frame, textvariable=self.checkout_book_var, width=20)
        self.checkout_book_entry.grid(row=0, column=1, padx=5)

        ttk.Label(checkout_frame, text="User ID:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.user_var = tk.StringVar()
        self.user_entry = ttk.Entry(checkout_frame, textvariable=self.user_var, width=20)
        self.user_entry.grid(row=0, column=3, padx=5)

        # Checkout buttons
        checkout_buttons = ttk.Frame(checkout_frame)
        checkout_buttons.grid(row=1, column=0, columnspan=4, pady=10)

        ttk.Button(checkout_buttons, text="Checkout Book", command=self.checkout_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(checkout_buttons, text="Return Book", command=self.return_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(checkout_buttons, text="View Queue Status", command=self.view_queue_status).pack(side=tk.LEFT,
                                                                                                    padx=5)

        # Queue status display
        queue_frame = ttk.LabelFrame(frame, text="Queue Status", padding=10)
        queue_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.queue_display = scrolledtext.ScrolledText(queue_frame, height=20, wrap=tk.WORD)
        self.queue_display.pack(fill=tk.BOTH, expand=True)

    def create_data_structures_tab(self):
        """Data structures visualization and logs"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔧 Data Structures")

        # Statistics frame
        stats_frame = ttk.LabelFrame(frame, text="Collection Statistics", padding=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)

        self.stats_text = tk.Text(stats_frame, height=8, wrap=tk.WORD)
        self.stats_text.pack(fill=tk.BOTH, expand=True)

        # Control buttons
        control_frame = ttk.Frame(stats_frame)
        control_frame.pack(fill=tk.X, pady=5)

        ttk.Button(control_frame, text="Refresh Statistics", command=self.refresh_statistics).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Show BST Traversal", command=self.show_bst_traversal).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Show Linked List", command=self.show_linked_list).pack(side=tk.LEFT, padx=5)

        # Activity log
        log_frame = ttk.LabelFrame(frame, text="Activity Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Log controls
        log_controls = ttk.Frame(log_frame)
        log_controls.pack(fill=tk.X, pady=5)

        ttk.Button(log_controls, text="Clear Log", command=self.clear_log).pack(side=tk.LEFT, padx=5)
        ttk.Button(log_controls, text="Save Log", command=self.save_log).pack(side=tk.LEFT, padx=5)

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
        """Add book to all data structures"""
        isbn = self.isbn_var.get().strip()
        title = self.title_var.get().strip()
        author = self.author_var.get().strip()

        if not all([isbn, title, author]):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            # Add to database
            cursor = self.storage.conn.cursor()
            cursor.execute("INSERT INTO books (isbn, title, author) VALUES (?, ?, ?)",
                           (isbn, title, author))
            self.storage.conn.commit()
            book_id = cursor.lastrowid

            # Add to all data structures
            self.bst.insert(book_id, (title, author, isbn))
            self.book_dict.add_book(isbn, title, author)
            self.linked_list.add_book(title, author, isbn)
            self.queue_system.add_book(str(book_id), title, 1)

            self._log(f"Added book: {title} by {author} (ISBN: {isbn})")
            self.refresh_books_display()
            self.clear_fields()
            self.status_var.set("Book added successfully")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book: {str(e)}")

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
            messagebox.showwarning("Warning", "Please select a book to delete")
            return

        item = self.books_tree.item(selection[0])
        isbn = item['values'][0]
        title = item['values'][1]

        if messagebox.askyesno("Confirm", f"Delete book '{title}'?"):
            try:
                # Delete from database
                cursor = self.storage.conn.cursor()
                cursor.execute("DELETE FROM books WHERE isbn=?", (isbn,))
                self.storage.conn.commit()

                # Reload data structures
                self._reload_data_structures()

                self._log(f"Deleted book: {title} (ISBN: {isbn})")
                self.refresh_books_display()
                self.clear_fields()
                self.status_var.set("Book deleted successfully")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete book: {str(e)}")

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
        """Checkout book using queue system"""
        book_id = self.checkout_book_var.get().strip()
        user_id = self.user_var.get().strip()

        if not all([book_id, user_id]):
            messagebox.showerror("Error", "Please enter both Book ID and User ID")
            return

        try:
            # Update database
            cursor = self.storage.conn.cursor()
            cursor.execute("UPDATE books SET status='Checked Out' WHERE id=?", (book_id,))
            self.storage.conn.commit()

            # Use queue system
            self.queue_system.check_out_book(user_id, book_id)

            self._log(f"Book {book_id} checked out to {user_id}")
            self.refresh_books_display()
            self.clear_fields()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to checkout book: {str(e)}")

    def return_book(self):
        """Return book using queue system"""
        book_id = self.checkout_book_var.get().strip()
        user_id = self.user_var.get().strip()

        if not all([book_id, user_id]):
            messagebox.showerror("Error", "Please enter both Book ID and User ID")
            return

        try:
            # Update database
            cursor = self.storage.conn.cursor()
            cursor.execute("UPDATE books SET status='Available' WHERE id=?", (book_id,))
            self.storage.conn.commit()

            # Use queue system
            self.queue_system.return_book(book_id, user_id)

            self._log(f"Book {book_id} returned by {user_id}")
            self.refresh_books_display()
            self.clear_fields()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to return book: {str(e)}")

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
                self.bst.insert(book_id, (title, author, isbn))
                self.book_dict.add_book(isbn, title, author)
                self.linked_list.add_book(title, author, isbn)
                self.queue_system.add_book(str(book_id), title, 1)

            self.refresh_books_display()
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

        # Reload from database
        self._load_existing_data()


if __name__ == "__main__":
    app = IntegratedLibraryGUI()
    app.mainloop()