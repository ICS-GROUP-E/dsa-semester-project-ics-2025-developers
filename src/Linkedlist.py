# === LIBRARY BOOK LINKED LIST WITH STYLED UI ===
import tkinter as tk
from tkinter import ttk, messagebox

# --- STYLE CONSTANTS ---
BG_COLOR = "#f0f0f0"
PRIMARY_COLOR = "#4a6fa5"
SECONDARY_COLOR = "#166088"
ACCENT_COLOR = "#4fc3f7"
TEXT_COLOR = "#333333"
FONT = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_TITLE = ("Segoe UI", 12, "bold")


# --- 1. NODE CLASS ---
class Node:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True
        self.next = None


# --- 2. LINKED LIST CLASS ---
class BookLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def add_book(self, title, author, isbn):
        new_node = Node(title, author, isbn)
        if not self.head:
            self.head = new_node
        else:
            self.tail.next = new_node
        self.tail = new_node
        self.size += 1
        return f"Added: {title}"

    def delete_book(self, isbn):
        current = self.head
        previous = None

        while current:
            if str(current.isbn) == str(isbn).strip():
                if previous:
                    previous.next = current.next
                    if not current.next:
                        self.tail = previous
                else:
                    self.head = current.next
                    if not self.head:
                        self.tail = None
                self.size -= 1
                return f"Deleted: {current.title}"
            previous = current
            current = current.next
        return "Book not found"

    def search_by_title(self, title):
        current = self.head
        while current:
            if current.title.lower() == title.lower():
                return current
            current = current.next
        return None

    def get_all_books(self):
        books = []
        current = self.head
        while current:
            books.append({
                "title": current.title,
                "author": current.author,
                "isbn": current.isbn,
                "available": current.available
            })
            current = current.next
        return books


# --- 3. STYLED GUI WITH DROPDOWN ---
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Book Tracker")
        self.root.geometry("800x600")
        self.root.configure(bg=BG_COLOR)

        # Configure styles
        self.configure_styles()

        self.books = BookLinkedList()

        # Predefined book options for dropdown
        self.book_options = [
            ("The Hobbit", "J.R.R. Tolkien", "111"),
            ("1984", "George Orwell", "222"),
            ("Dune", "Frank Herbert", "333"),
            ("To Kill a Mockingbird", "Harper Lee", "444"),
            ("The Great Gatsby", "F. Scott Fitzgerald", "555"),
            ("Pride and Prejudice", "Jane Austen", "666"),
            ("The Catcher in the Rye", "J.D. Salinger", "777"),
            ("Brave New World", "Aldous Huxley", "888"),
            ("The Lord of the Rings", "J.R.R. Tolkien", "999"),
            ("Animal Farm", "George Orwell", "1011")
        ]

        # Header Frame
        header_frame = tk.Frame(root, bg=PRIMARY_COLOR, padx=10, pady=10)
        header_frame.pack(fill=tk.X)

        tk.Label(
            header_frame,
            text="LIBRARY BOOK TRACKER",
            font=FONT_TITLE,
            bg=PRIMARY_COLOR,
            fg="white"
        ).pack(side=tk.LEFT)

        # Main container frame
        main_frame = tk.Frame(root, bg=BG_COLOR, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Add Book Section
        add_frame = tk.LabelFrame(
            main_frame,
            text=" Add New Book ",
            font=FONT_BOLD,
            bg=BG_COLOR,
            fg=SECONDARY_COLOR,
            padx=10,
            pady=10
        )
        add_frame.pack(fill=tk.X, pady=(0, 20))

        # Dropdown menu
        self.selected_book = tk.StringVar()
        self.selected_book.set("Select a book")  # Default option

        self.book_dropdown = ttk.Combobox(
            add_frame,
            textvariable=self.selected_book,
            values=[book[0] for book in self.book_options],
            state="readonly",
            font=FONT,
            height=15
        )
        self.book_dropdown.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))

        # Add button
        add_button = ttk.Button(
            add_frame,
            text="Add Book",
            command=self.add_from_dropdown,
            style="Accent.TButton"
        )
        add_button.pack(side=tk.LEFT)

        # Books Display Section
        display_frame = tk.LabelFrame(
            main_frame,
            text=" Book Collection ",
            font=FONT_BOLD,
            bg=BG_COLOR,
            fg=SECONDARY_COLOR,
            padx=10,
            pady=10
        )
        display_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview with scrollbars
        tree_scroll = ttk.Scrollbar(display_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            display_frame,
            columns=("Title", "Author", "ISBN", "Status"),
            show="headings",
            yscrollcommand=tree_scroll.set,
            selectmode="browse"
        )
        self.tree.pack(fill=tk.BOTH, expand=True)

        tree_scroll.config(command=self.tree.yview)

        # Configure treeview columns
        self.tree.heading("Title", text="Title", anchor=tk.W)
        self.tree.heading("Author", text="Author", anchor=tk.W)
        self.tree.heading("ISBN", text="ISBN", anchor=tk.W)
        self.tree.heading("Status", text="Status", anchor=tk.CENTER)

        self.tree.column("Title", width=250, stretch=tk.YES)
        self.tree.column("Author", width=200, stretch=tk.YES)
        self.tree.column("ISBN", width=100, stretch=tk.YES)
        self.tree.column("Status", width=80, stretch=tk.NO, anchor=tk.CENTER)

        # Action buttons frame
        button_frame = tk.Frame(main_frame, bg=BG_COLOR, pady=10)
        button_frame.pack(fill=tk.X)

        # Delete button
        delete_button = ttk.Button(
            button_frame,
            text="Delete Selected",
            command=self.delete_selected,
            style="Danger.TButton"
        )
        delete_button.pack(side=tk.RIGHT, padx=(10, 0))

        # Initialize with sample data
        self.update_display()

    def configure_styles(self):
        """Configure custom styles for widgets"""
        style = ttk.Style()
        style.theme_use("clam")

        # Frame styles
        style.configure("TFrame", background=BG_COLOR)

        # Label styles
        style.configure("TLabel", background=BG_COLOR, font=FONT)

        # Button styles
        style.configure("TButton",
                        font=FONT,
                        padding=6,
                        background=SECONDARY_COLOR,
                        foreground="white")
        style.map("TButton",
                  background=[("active", PRIMARY_COLOR), ("disabled", "#cccccc")])

        # Accent button style
        style.configure("Accent.TButton",
                        background=ACCENT_COLOR,
                        foreground="white")
        style.map("Accent.TButton",
                  background=[("active", "#81d4fa"), ("disabled", "#cccccc")])

        # Danger button style
        style.configure("Danger.TButton",
                        background="#e53935",
                        foreground="white")
        style.map("Danger.TButton",
                  background=[("active", "#ef5350"), ("disabled", "#cccccc")])

        # Combobox style
        style.configure("TCombobox",
                        font=FONT,
                        padding=5)

        # Treeview styles
        style.configure("Treeview",
                        font=FONT,
                        background="white",
                        fieldbackground="white",
                        foreground=TEXT_COLOR,
                        rowheight=25)
        style.configure("Treeview.Heading",
                        font=FONT_BOLD,
                        background=PRIMARY_COLOR,
                        foreground="white",
                        padding=5)
        style.map("Treeview",
                  background=[("selected", SECONDARY_COLOR)])

    def add_from_dropdown(self):
        """Adds the selected book from dropdown"""
        selected_title = self.selected_book.get()

        if selected_title == "Select a book":
            messagebox.showwarning("Warning", "Please select a book first!")
            return

        # Find the selected book in our options
        for title, author, isbn in self.book_options:
            if title == selected_title:
                # Check if book already exists
                if self.books.search_by_title(title):
                    messagebox.showwarning("Warning", f"'{title}' already exists!")
                    return

                self.books.add_book(title, author, isbn)
                self.update_display()
                messagebox.showinfo("Success", f"Added: {title}")
                return

        messagebox.showerror("Error", "Book not found in options!")

    def delete_selected(self):
        """Deletes the selected book"""
        selected_items = self.tree.selection()

        if not selected_items:
            messagebox.showwarning("Warning", "Please select a book to delete first!")
            return

        selected_item = selected_items[0]
        item_values = self.tree.item(selected_item)['values']

        if len(item_values) < 3:
            messagebox.showerror("Error", "Invalid book data in selection")
            return

        selected_isbn = str(item_values[2]).strip()
        result = self.books.delete_book(selected_isbn)

        if result.startswith("Deleted"):
            self.tree.delete(selected_item)
            messagebox.showinfo("Success", result)
        else:
            messagebox.showerror("Error", result)

        self.update_display()

    def update_display(self):
        """Updates the Treeview with current books"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        for book in self.books.get_all_books():
            status = "✓ Available" if book["available"] else "✗ Checked Out"
            status_color = "#2e7d32" if book["available"] else "#c62828"

            self.tree.insert("", "end", values=(
                book["title"],
                book["author"],
                book["isbn"],
                status
            ))

            # Color the status text
            last_item = self.tree.get_children()[-1]
            self.tree.set(last_item, "Status", status)
            self.tree.tag_configure(status_color, foreground=status_color)
            self.tree.item(last_item, tags=(status_color,))


# --- 4. MAIN EXECUTION ---
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()