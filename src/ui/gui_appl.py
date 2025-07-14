import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from src.data_struct.Bsearch import BinarySearchTree
from src.data_struct.BookDictionary import BookDictionary
from src.data_struct.linkedList import BookLinkedList
from src.data_struct.queue import LibrarySystem
from src.data_struct.Stacks import ActivityStack
from src.database.sqlite import SQLiteService
from datetime import datetime
import sqlite3


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
        self.activity_stack = ActivityStack()  # Initialize the stack
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

        # Create visualization canvas
        canvas_frame = ttk.LabelFrame(frame, text="Data Structure Visualization", padding=10)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.viz_canvas = tk.Canvas(canvas_frame, width=600, height=300, bg='white')
        self.viz_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Control panel for visualization
        control_frame = ttk.Frame(canvas_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(control_frame, text="Visualize:").pack(side=tk.LEFT, padx=5)
        self.viz_type = ttk.Combobox(control_frame, values=["BST", "Stack", "Queue", "Linked List"])
        self.viz_type.pack(side=tk.LEFT, padx=5)
        self.viz_type.set("BST")
        self.viz_type.bind('<<ComboboxSelected>>', self.update_visualization)
        
        ttk.Button(control_frame, text="Refresh", command=self.update_visualization).pack(side=tk.LEFT, padx=5)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(frame, text="Collection Statistics", padding=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.stats_text = tk.Text(stats_frame, height=8, wrap=tk.WORD)
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Activity log
        log_frame = ttk.LabelFrame(frame, text="Activity Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)

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
            
            self._log(f"Added book: {title} (ISBN: {isbn})")
            self.refresh_books_display()
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
            
            try:
                # Delete from database
                self.storage.conn.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
                self.storage.conn.commit()
                
                # Delete from data structures
                self.bst.delete(isbn)
                self.book_dict.delete_book(isbn)
                self.linked_list.delete_book(isbn)
                
                self._log(f"Deleted book: {item['values'][1]} (ISBN: {isbn})")
                self.refresh_books_display()
                self.clear_fields()
                
                # Update visualization based on current view
                self.update_visualization()
                
            except Exception as e:
                messagebox.showerror("Error", str(e))

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


if __name__ == "__main__":
    app = IntegratedLibraryGUI()
    app.mainloop()