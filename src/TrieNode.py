class TrieNode:
    def __init__(self):
        self.children = {}       # Maps characters to child nodes
        self.is_end = False      # Marks end of a complete title
        self.books = []          # Stores book data for titles ending here


class BookTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, title: str, book_data: dict):
        """Inserts a book title into the trie."""
        node = self.root
        for char in title.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.books.append(book_data)  # Store full book data

    def search_prefix(self, prefix: str) -> list:
        """Returns all books matching a title prefix."""
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]

        # Collect all books under this prefix
        results = []
        self._dfs_collect(node, prefix, results)
        return results

    def _dfs_collect(self, node, current_prefix, results):
        """Helper: Depth-first search to gather complete titles."""
        if node.is_end:
            results.extend(node.books)  # Add all books at this node
        for char, child in node.children.items():
            self._dfs_collect(child, current_prefix + char, results)


# ✅ Test the Trie
if __name__ == "__main__":
    # Create trie
    trie = BookTrie()

    # Insert books
    trie.insert("Harry Potter and the Sorcerer's Stone", {"isbn": "1234", "author": "J.K. Rowling"})
    trie.insert("Harry Potter and the Chamber of Secrets", {"isbn": "5678", "author": "J.K. Rowling"})
    trie.insert("The Hobbit", {"isbn": "9012", "author": "J.R.R. Tolkien"})
    trie.insert("Hatchet", {"isbn": "3456", "author": "Gary Paulsen"})

    # Search books by prefix
    search_result = trie.search_prefix("har")

    # Print results
    print("Books matching prefix 'har':")
    for book in search_result:
        print(book)
