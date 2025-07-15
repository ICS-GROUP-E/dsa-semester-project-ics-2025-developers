import unittest
from src.data_struct.linkedList import BookLinkedList, Node

class TestBookLinkedList(unittest.TestCase):
    def setUp(self):
        self.list = BookLinkedList()
        # Sample test data
        self.test_books = [
            ("Book 1", "Author 1", "ISBN001"),
            ("Book 2", "Author 2", "ISBN002"),
            ("Book 3", "Author 3", "ISBN003")
        ]
        
    def test_add_book(self):
        # Test adding single book
        result = self.list.add_book("Test Book", "Test Author", "TEST001")
        self.assertIn("Added: Test Book", result)
        self.assertEqual(self.list.size, 1)
        
        # Test adding multiple books
        for title, author, isbn in self.test_books:
            self.list.add_book(title, author, isbn)
        self.assertEqual(self.list.size, 4)  # Including the first test book
        
    def test_delete_book(self):
        # Add books for testing
        for title, author, isbn in self.test_books:
            self.list.add_book(title, author, isbn)
            
        # Test deleting existing book
        result = self.list.delete_book("ISBN002")
        self.assertIn("Deleted: Book 2", result)
        self.assertEqual(self.list.size, 2)
        
        # Test deleting non-existent book
        result = self.list.delete_book("INVALID")
        self.assertEqual(result, "Book not found")
        self.assertEqual(self.list.size, 2)
        
        # Test deleting first book
        result = self.list.delete_book("ISBN001")
        self.assertIn("Deleted: Book 1", result)
        self.assertEqual(self.list.size, 1)
        
        # Test deleting last book
        result = self.list.delete_book("ISBN003")
        self.assertIn("Deleted: Book 3", result)
        self.assertEqual(self.list.size, 0)
        
    def test_search_by_title(self):
        # Add books for testing
        for title, author, isbn in self.test_books:
            self.list.add_book(title, author, isbn)
            
        # Test searching existing book
        result = self.list.search_by_title("Book 2")
        self.assertIsNotNone(result)
        self.assertEqual(result.title, "Book 2")
        self.assertEqual(result.author, "Author 2")
        self.assertEqual(result.isbn, "ISBN002")
        
        # Test searching non-existent book
        result = self.list.search_by_title("Invalid Book")
        self.assertIsNone(result)
        
        # Test case-insensitive search
        result = self.list.search_by_title("book 2")
        self.assertIsNotNone(result)
        self.assertEqual(result.title, "Book 2")
        
    def test_get_all_books(self):
        # Test empty list
        self.assertEqual(len(self.list.get_all_books()), 0)
        
        # Add books and test
        for title, author, isbn in self.test_books:
            self.list.add_book(title, author, isbn)
            
        books = self.list.get_all_books()
        self.assertEqual(len(books), 3)
        
        # Verify book details
        self.assertEqual(books[0]["title"], "Book 1")
        self.assertEqual(books[1]["author"], "Author 2")
        self.assertEqual(books[2]["isbn"], "ISBN003")
        
        # Verify availability flag
        for book in books:
            self.assertTrue(book["available"])

if __name__ == '__main__':
    unittest.main() 