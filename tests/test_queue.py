import unittest
from src.data_struct.queue import LibrarySystem

class TestLibrarySystem(unittest.TestCase):
    def setUp(self):
        self.library = LibrarySystem()
        # Add test books
        self.library.add_book("B001", "Test Book 1", 2)
        self.library.add_book("B002", "Test Book 2", 1)
        
    def test_add_book(self):
        # Test adding new book
        self.library.add_book("B003", "Test Book 3", 3)
        self.assertIn("B003", self.library.books)
        self.assertEqual(self.library.books["B003"]["title"], "Test Book 3")
        self.assertEqual(self.library.books["B003"]["available_copies"], 3)
        
    def test_check_out_book(self):
        # Test successful checkout
        result = self.library.check_out_book("USER1", "B001")
        self.assertTrue(result)
        self.assertEqual(self.library.books["B001"]["available_copies"], 1)
        self.assertIn("USER1", self.library.books["B001"]["checked_out_to"])
        
        # Test checkout with no copies available
        self.library.check_out_book("USER2", "B002")  # Take last copy
        result = self.library.check_out_book("USER3", "B002")
        self.assertFalse(result)
        self.assertIn("USER3", self.library.books["B002"]["reservation_queue"])
        
    def test_return_book(self):
        # Check out and return book
        self.library.check_out_book("USER1", "B001")
        self.library.return_book("B001", "USER1")
        self.assertEqual(self.library.books["B001"]["available_copies"], 2)
        self.assertNotIn("USER1", self.library.books["B001"]["checked_out_to"])
        
        # Test return with waiting queue
        self.library.check_out_book("USER1", "B002")  # Take last copy
        self.library.check_out_book("USER2", "B002")  # Add to queue
        self.library.return_book("B002", "USER1")  # Should auto-checkout to USER2
        self.assertIn("USER2", self.library.books["B002"]["checked_out_to"])
        self.assertEqual(len(self.library.books["B002"]["reservation_queue"]), 0)
        
    def test_invalid_operations(self):
        # Test invalid book ID
        result = self.library.check_out_book("USER1", "INVALID")
        self.assertFalse(result)
        
        # Test invalid return
        self.library.return_book("B001", "INVALID_USER")
        self.assertEqual(self.library.books["B001"]["available_copies"], 2)
        
    def test_reservation_queue(self):
        # Fill up the queue
        self.library.check_out_book("USER1", "B002")  # Take last copy
        self.library.check_out_book("USER2", "B002")  # Add to queue
        self.library.check_out_book("USER3", "B002")  # Add to queue
        
        # Verify queue order
        queue = self.library.books["B002"]["reservation_queue"]
        self.assertEqual(len(queue), 2)
        self.assertEqual(queue[0], "USER2")
        self.assertEqual(queue[1], "USER3")
        
        # Test queue processing
        self.library.return_book("B002", "USER1")
        self.assertIn("USER2", self.library.books["B002"]["checked_out_to"])
        self.assertEqual(len(queue), 1)
        self.assertEqual(queue[0], "USER3")

if __name__ == '__main__':
    unittest.main() 