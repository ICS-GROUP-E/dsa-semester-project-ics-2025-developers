import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
from datetime import datetime
from collections import deque


# === DATA STRUCTURES ===

class BookDictionary:
    """Hash Table implementation for fast book lookups"""

    def __init__(self):
        self.books = {}

    def add_book(self, isbn, title, author):
        if isbn in self.books:
            return False
        self.books[isbn] = {
            "isbn": isbn,
            "title": title,
            "author": author,
            "available": True
        }
        return True

    def delete_book(self, isbn):
        return self.books.pop(isbn, None) is not None

    def search_by_isbn(self, isbn):
        return self.books.get(isbn)

    def search_by_title(self, title):
        title = title.lower()
        return [book for book in self.books.values() if book["title"].lower().startswith(title)]

    def get_all_books(self):
        return list(self.books.values())


class ActivityNode:
    """Node for activity stack"""

    def __init__(self, action, details):
        self.action = action
        self.details = details
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.next = None


class ActivityStack:
    """Stack for tracking user activities"""

    def __init__(self):
        self.top = None
        self.size = 0
        self.max_size = 50

    def push(self, action, details):
        new_node = ActivityNode(action, details)
        new_node.next = self.top
        self.top = new_node
        self.size += 1
        if self.size > self.max_size:
            self._remove_last()
        return f"Logged: {action}"

    def pop(self):
        if not self.top:
            return None
        popped = self.top
        self.top = self.top.next
        self.size -= 1
        return (popped.action, popped.details, popped.timestamp)

    def peek(self):
        return (self.top.action, self.top.details, self.top.timestamp) if self.top else None

    def _remove_last(self):
        if self.size <= 1:
            return
        current = self.top
        while current.next and current.next.next:
            current = current.next
        current.next = None
        self.size -= 1

    def get_all_actions(self):
        actions = []
        current = self.top
        while current:
            actions.append({
                "action": current.action,
                "details": current.details,
                "timestamp": current.timestamp
            })
            current = current.next
        return actions


class CheckoutQueue:
    """Queue for managing book checkouts"""

    def __init__(self):
        self.queue = deque()

    def enqueue(self, user_id, isbn, title):
        checkout_data = {
            "user_id": user_id,
            "isbn": isbn,
            "title": title,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.queue.append(checkout_data)
        return f"Added to checkout queue: {title}"

    def dequeue(self):
        if self.queue:
            return self.queue.popleft()
        return None

    def get_all_checkouts(self):
        return list(self.queue)

    def is_empty(self):
        return len(self.queue) == 0


class BookNode:
    """Node for linked list"""

    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.available = True
        self.next = None


class BookLinkedList:
    """Linked list for sequential book storage"""

    def __init__(self):
        self.head = None
        self.size = 0

    def add_book(self, isbn, title, author):
        new_node = BookNode(isbn, title, author)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
        return f"Added: {title}"

    def delete_book(self, isbn):
        current = self.head
        previous = None

        while current:
            if current.isbn == isbn:
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next
                self.size -= 1
                return f"Deleted: {current.title}"
            previous = current
            current = current.next
        return "Book not found"

    def search_by_isbn(self, isbn):
        current = self.head
        while current:
            if current.isbn == isbn:
                return current
            current = current.next
        return None

    def get_all_books(self):
        books = []
        current = self.head
        while current:
            books.append({
                "isbn": current.isbn,
                "title": current.title,
                "author": current.author,
                "available": current.available
            })
            current = current.next
        return books


class BSTNode:
    """Node for Binary Search Tree"""

    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.available = True
        self.left = None
        self.right = None


class BookBST:
    """Binary Search Tree for efficient searching"""

    def __init__(self):
        self.root = None

    def insert(self, isbn, title, author):
        if not self.root:
            self.root = BSTNode(isbn, title, author)
        else:
            self._insert_recursive(self.root, isbn, title, author)

    def _insert_recursive(self, node, isbn, title, author):
        if isbn < node.isbn:
            if node.left is None:
                node.left = BSTNode(isbn, title, author)
            else:
                self._insert_recursive(node.left, isbn, title, author)
        elif isbn > node.isbn:
            if node.right is None:
                node.right = BSTNode(isbn, title, author)
            else:
                self._insert_recursive(node.right, isbn, title, author)
        else:
            # Update existing node
            node.title = title
            node.author = author

    def search(self, isbn):
        return self._search_recursive(self.root, isbn)

    def _search_recursive(self, node, isbn):
        if node is None:
            return None
        if node.isbn == isbn:
            return node
        elif isbn < node.isbn:
            return self._search_recursive(node.left, isbn)
        else:
            return self._search_recursive(node.right, isbn)

    def inorder_traversal(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append({
                "isbn": node.isbn,
                "title": node.title,
                "author": node.author,
                "available": node.available
            })
            self._inorder_recursive(node.right, result)


# === DATABASE SERVICE ===

class DatabaseService:
    """SQLite database service for persistence"""

    def __init__(self, db_name="library.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                isbn TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                available BOOLEAN DEFAULT 1
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS checkouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                isbn TEXT NOT NULL,
                checkout_date TEXT NOT NULL,
                FOREIGN KEY (isbn) REFERENCES books (isbn)
            )
        ''')
        self.conn.commit()

    def add_book(self, isbn, title, author):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO books (isbn, title, author) VALUES (?, ?, ?)",
                (isbn, title, author)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_all_books(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT isbn, title, author, available FROM books")
        return cursor.fetchall()

    def delete_book(self, isbn):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
        self.conn.commit()
        return cursor.rowcount > 0

    def checkout_book(self, user_id, isbn):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO checkouts (user_id, isbn, checkout_date) VALUES (?, ?, ?)",
            (user_id, isbn, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        cursor.execute("UPDATE books SET available = 0 WHERE isbn = ?", (isbn,))
        self.conn.commit()

    def return_book(self, isbn):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE books SET available = 1 WHERE isbn = ?", (isbn,))
        cursor.execute("DELETE FROM checkouts WHERE isbn = ?", (isbn,))
        self.conn.commit()


# === MAIN APPLICATION ===

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System - DSA Project")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')

        # Initialize data structures
        self.book_dict = BookDictionary()
        self.activity_stack = ActivityStack()
        self.checkout_queue = CheckoutQueue()
        self.book_list = BookLinkedList()
        self.book_bst = BookBST()
        self.db = DatabaseService()

        # Load existing data
        self.load_data()

        # Create GUI
        self.create_widgets()

        # Initialize with sample data if empty
        if not self.book_dict.get_all_books():
            self.add_sample_data()

    def load_data(self):
        """Load books from database into data structures"""
        books = self.db.get_all_books()
        for isbn, title, author, available in books:
            self.book_dict.add_book(isbn, title, author)
            self.book_list.add_book(isbn, title, author)
            self.book_bst.insert(isbn, title, author)

    def add_sample_data(self):
        """Add sample books for demonstration"""
        sample_books = [
            ("978-0-7432-7356-5", "The 7 Habits of Highly Effective People", "Stephen Covey"),
            ("978-1-4516-7388-9", "Atomic Habits", "James Clear"),
            ("978-0-06-112008-4", "The Lean Startup", "Eric Ries"),
            ("978-0-201-83595-3", "Design Patterns", "Gang of Four"),
            ("978-0-13-235088-4", "Clean Code", "Robert Martin")
        ]

        for isbn, title, author in sample_books:
            self.add_book(isbn, title, author)

    def create_widgets(self):
        """Create the main GUI interface"""
        # Main title
        title_label = tk.Label(
            self.root,
            text="📚 Library Management System",
            font=("Arial", 20, "bold"),
            bg='#2c3e50',
            fg='white',
            pady=10
        )
        title_label.pack(fill=tk.X)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tabs
        self.create_book_management_tab()
        self.create_search_tab()
        self.create_checkout_tab()
        self.create_activity_tab()
        self.create_data_structures_tab()

    def create_book_management_tab(self):
        """Create the book management tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📖 Book Management")

        # Input frame
        input_frame = ttk.LabelFrame(tab, text="Add/Update Book", padding=20)
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        # ISBN input
        ttk.Label(input_frame, text="ISBN:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.isbn_entry = ttk.Entry(input_frame, width=30, font=("Arial", 10))
        self.isbn_entry.grid(row=0, column=1, padx=10, pady=5)

        # Title input
        ttk.Label(input_frame, text="Title:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.title_entry = ttk.Entry(input_frame, width=30, font=("Arial", 10))
        self.title_entry.grid(row=1, column=1, padx=10, pady=5)

        # Author input
        ttk.Label(input_frame, text="Author:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.author_entry = ttk.Entry(input_frame, width=30, font=("Arial", 10))
        self.author_entry.grid(row=2, column=1, padx=10, pady=5)

        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="➕ Add Book", command=self.add_book_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Delete Book", command=self.delete_book_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Refresh", command=self.refresh_book_list).pack(side=tk.LEFT, padx=5)

        # Book list
        list_frame = ttk.LabelFrame(tab, text="All Books", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview for book list
        columns = ("ISBN", "Title", "Author", "Status")
        self.book_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.book_tree.heading(col, text=col)
            self.book_tree.column(col, width=200)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.book_tree.yview)
        self.book_tree.configure(yscrollcommand=scrollbar.set)

        self.book_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Populate book list
        self.refresh_book_list()

    def create_search_tab(self):
        """Create the search tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔍 Search Books")

        # Search frame
        search_frame = ttk.LabelFrame(tab, text="Search Options", padding=20)
        search_frame.pack(fill=tk.X, padx=10, pady=10)

        # Search by ISBN
        ttk.Label(search_frame, text="Search by ISBN:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.search_isbn_entry = ttk.Entry(search_frame, width=30)
        self.search_isbn_entry.grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(search_frame, text="🔍 Search", command=self.search_by_isbn).grid(row=0, column=2, padx=5)

        # Search by Title
        ttk.Label(search_frame, text="Search by Title:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.search_title_entry = ttk.Entry(search_frame, width=30)
        self.search_title_entry.grid(row=1, column=1, padx=10, pady=5)
        ttk.Button(search_frame, text="🔍 Search", command=self.search_by_title).grid(row=1, column=2, padx=5)

        # Results frame
        results_frame = ttk.LabelFrame(tab, text="Search Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Results text area
        self.search_results = scrolledtext.ScrolledText(results_frame, height=20, font=("Arial", 10))
        self.search_results.pack(fill=tk.BOTH, expand=True)

    def create_checkout_tab(self):
        """Create the checkout tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📋 Checkout/Return")

        # Checkout frame
        checkout_frame = ttk.LabelFrame(tab, text="Checkout Book", padding=20)
        checkout_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(checkout_frame, text="User ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.user_id_entry = ttk.Entry(checkout_frame, width=30)
        self.user_id_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(checkout_frame, text="Book ISBN:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.checkout_isbn_entry = ttk.Entry(checkout_frame, width=30)
        self.checkout_isbn_entry.grid(row=1, column=1, padx=10, pady=5)

        button_frame = ttk.Frame(checkout_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="📤 Checkout", command=self.checkout_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📥 Return", command=self.return_book).pack(side=tk.LEFT, padx=5)

        # Queue display
        queue_frame = ttk.LabelFrame(tab, text="Checkout Queue", padding=10)
        queue_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.queue_text = scrolledtext.ScrolledText(queue_frame, height=15, font=("Arial", 10))
        self.queue_text.pack(fill=tk.BOTH, expand=True)

        self.refresh_queue_display()

    def create_activity_tab(self):
        """Create the activity log tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📊 Activity Log")

        # Controls frame
        controls_frame = ttk.Frame(tab)
        controls_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(controls_frame, text="🔄 Refresh", command=self.refresh_activity_log).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="⏪ Undo Last", command=self.undo_last_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="🗑️ Clear Log", command=self.clear_activity_log).pack(side=tk.LEFT, padx=5)

        # Activity log display
        log_frame = ttk.LabelFrame(tab, text="Recent Activities", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Activity treeview
        columns = ("Action", "Details", "Timestamp")
        self.activity_tree = ttk.Treeview(log_frame, columns=columns, show="headings", height=20)

        for col in columns:
            self.activity_tree.heading(col, text=col)
            self.activity_tree.column(col, width=300)

        activity_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.activity_tree.yview)
        self.activity_tree.configure(yscrollcommand=activity_scrollbar.set)

        self.activity_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        activity_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.refresh_activity_log()

    def create_data_structures_tab(self):
        """Create the data structures visualization tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔧 Data Structures")

        # Info frame
        info_frame = ttk.LabelFrame(tab, text="Data Structure Information", padding=20)
        info_frame.pack(fill=tk.X, padx=10, pady=10)

        # Statistics
        self.stats_text = tk.Text(info_frame, height=8, font=("Arial", 10))
        self.stats_text.pack(fill=tk.X)

        # BST visualization
        bst_frame = ttk.LabelFrame(tab, text="Binary Search Tree (In-order Traversal)", padding=10)
        bst_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.bst_text = scrolledtext.ScrolledText(bst_frame, height=15, font=("Arial", 10))
        self.bst_text.pack(fill=tk.BOTH, expand=True)

        # Refresh button
        ttk.Button(tab, text="🔄 Refresh Data Structures", command=self.refresh_data_structures).pack(pady=10)

        self.refresh_data_structures()

    def add_book_gui(self):
        """Add book through GUI"""
        isbn = self.isbn_entry.get().strip()
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()

        if not isbn or not title or not author:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        if self.add_book(isbn, title, author):
            messagebox.showinfo("Success", f"Book '{title}' added successfully!")
            self.clear_entries()
            self.refresh_book_list()
        else:
            messagebox.showerror("Error", "Book with this ISBN already exists")

    def add_book(self, isbn, title, author):
        """Add book to all data structures"""
        if self.book_dict.add_book(isbn, title, author):
            self.book_list.add_book(isbn, title, author)
            self.book_bst.insert(isbn, title, author)
            self.db.add_book(isbn, title, author)
            self.activity_stack.push("ADD_BOOK", f"Added '{title}' by {author}")
            return True
        return False

    def delete_book_gui(self):
        """Delete book through GUI"""
        isbn = self.isbn_entry.get().strip()

        if not isbn:
            messagebox.showerror("Error", "Please enter ISBN")
            return

        book = self.book_dict.search_by_isbn(isbn)
        if book:
            if messagebox.askyesno("Confirm", f"Delete book '{book['title']}'?"):
                self.delete_book(isbn)
                messagebox.showinfo("Success", "Book deleted successfully!")
                self.clear_entries()
                self.refresh_book_list()
        else:
            messagebox.showerror("Error", "Book not found")

    def delete_book(self, isbn):
        """Delete book from all data structures"""
        book = self.book_dict.search_by_isbn(isbn)
        if book:
            self.book_dict.delete_book(isbn)
            self.book_list.delete_book(isbn)
            self.db.delete_book(isbn)
            self.activity_stack.push("DELETE_BOOK", f"Deleted '{book['title']}'")
            return True
        return False

    def search_by_isbn(self):
        """Search book by ISBN"""
        isbn = self.search_isbn_entry.get().strip()
        if not isbn:
            messagebox.showerror("Error", "Please enter ISBN")
            return

        self.activity_stack.push("SEARCH_ISBN", f"Searched for ISBN: {isbn}")

        # Search using hash table (O(1))
        book = self.book_dict.search_by_isbn(isbn)

        self.search_results.delete(1.0, tk.END)
        if book:
            result = f"✅ FOUND (Hash Table Search - O(1)):\n"
            result += f"ISBN: {book['isbn']}\n"
            result += f"Title: {book['title']}\n"
            result += f"Author: {book['author']}\n"
            result += f"Available: {'Yes' if book['available'] else 'No'}\n\n"

            # Also search using BST for comparison
            bst_node = self.book_bst.search(isbn)
            if bst_node:
                result += f"✅ ALSO FOUND (BST Search - O(log n)):\n"
                result += f"Title: {bst_node.title}\n"
                result += f"Author: {bst_node.author}\n"
        else:
            result = f"❌ NOT FOUND: No book with ISBN '{isbn}'"

        self.search_results.insert(tk.END, result)

    def search_by_title(self):
        """Search book by title"""
        title = self.search_title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Please enter title")
            return

        self.activity_stack.push("SEARCH_TITLE", f"Searched for title: {title}")

        # Search using hash table
        books = self.book_dict.search_by_title(title)

        self.search_results.delete(1.0, tk.END)
        if books:
            result = f"✅ FOUND {len(books)} book(s) matching '{title}':\n\n"
            for i, book in enumerate(books, 1):
                result += f"{i}. {book['title']} by {book['author']}\n"
                result += f"   ISBN: {book['isbn']}\n"
                result += f"   Available: {'Yes' if book['available'] else 'No'}\n\n"
        else:
            result = f"❌ NOT FOUND: No books with title matching '{title}'"

        self.search_results.insert(tk.END, result)

    def checkout_book(self):
        """Checkout a book"""
        user_id = self.user_id_entry.get().strip()
        isbn = self.checkout_isbn_entry.get().strip()

        if not user_id or not isbn:
            messagebox.showerror("Error", "Please enter both User ID and ISBN")
            return

        book = self.book_dict.search_by_isbn(isbn)
        if not book:
            messagebox.showerror("Error", "Book not found")
            return

        if not book['available']:
            messagebox.showerror("Error", "Book is already checked out")
            return

        # Update availability
        book['available'] = False

        # Add to checkout queue
        self.checkout_queue.enqueue(user_id, isbn, book['title'])

        # Update database
        self.db.checkout_book(user_id, isbn)

        # Log activity
        self.activity_stack.push("CHECKOUT", f"User {user_id} checked out '{book['title']}'")

        messagebox.showinfo("Success", f"Book '{book['title']}' checked out to {user_id}")
        self.user_id_entry.delete(0, tk.END)
        self.checkout_isbn_entry.delete(0, tk.END)
        self.refresh_book_list()
        self.refresh_queue_display()

    def return_book(self):
        """Return a book"""
        isbn = self.checkout_isbn_entry.get().strip()

        if not isbn:
            messagebox.showerror("Error", "Please enter ISBN")
            return

        book = self.book_dict.search_by_isbn(isbn)
        if not book:
            messagebox.showerror("Error", "Book not found")
            return

        if book['available']:
            messagebox.showerror("Error", "Book is not checked out")
            return

        # Update availability
        book['available'] = True

        # Update database
        self.db.return_book(isbn)

        # Log activity
        self.activity_stack.push("RETURN", f"Book '{book['title']}' returned")

        messagebox.showinfo("Success", f"Book '{book['title']}' returned successfully")
        self.checkout_isbn_entry.delete(0,