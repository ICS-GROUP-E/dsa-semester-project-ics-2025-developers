class BookDictionary:
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

# --- Test Code ---
if __name__ == "__main__":
    lib = BookDictionary()
    lib.add_book("001", "Atomic Habits", "James Clear")
    print(lib.search_by_isbn("001"))
    print(lib.get_all_books())