import unittest
from src.data_struct.Bsearch import BinarySearchTree

class TestBinarySearchTree(unittest.TestCase):
    def setUp(self):
        self.bst = BinarySearchTree()
        # Sample data for testing
        self.test_data = [
            (5, "Book 5"),
            (3, "Book 3"),
            (7, "Book 7"),
            (2, "Book 2"),
            (4, "Book 4"),
            (6, "Book 6"),
            (8, "Book 8"),
        ]
        
    def test_insert_and_search(self):
        # Test inserting and searching single item
        self.bst.insert(1, "Test Book")
        self.assertEqual(self.bst.search(1), "Test Book")
        
        # Test inserting and searching multiple items
        for key, data in self.test_data:
            self.bst.insert(key, data)
        
        for key, data in self.test_data:
            self.assertEqual(self.bst.search(key), data)
            
    def test_search_nonexistent(self):
        # Test searching for non-existent key
        self.assertIsNone(self.bst.search(100))
        
    def test_delete(self):
        # Insert test data
        for key, data in self.test_data:
            self.bst.insert(key, data)
            
        # Test deleting leaf node
        self.bst.delete(2)
        self.assertIsNone(self.bst.search(2))
        
        # Test deleting node with one child
        self.bst.delete(7)
        self.assertIsNone(self.bst.search(7))
        
        # Test deleting node with two children
        self.bst.delete(3)
        self.assertIsNone(self.bst.search(3))
        
    def test_inorder_traversal(self):
        # Insert test data
        for key, data in self.test_data:
            self.bst.insert(key, data)
            
        # Test inorder traversal
        inorder_result = list(self.bst.inorder())
        expected_keys = sorted([key for key, _ in self.test_data])
        actual_keys = [key for key, _ in inorder_result]
        self.assertEqual(actual_keys, expected_keys)

    def test_preorder_traversal(self):
        # Insert test data
        for key, data in self.test_data:
            self.bst.insert(key, data)
            
        # Test preorder traversal
        # For the given data, preorder should visit root first (5),
        # then left subtree (3,2,4), then right subtree (7,6,8)
        preorder_result = list(self.bst.preorder())
        expected_keys = [5, 3, 2, 4, 7, 6, 8]  # Expected order for our tree
        actual_keys = [key for key, _ in preorder_result]
        self.assertEqual(actual_keys, expected_keys)

    def test_postorder_traversal(self):
        # Insert test data
        for key, data in self.test_data:
            self.bst.insert(key, data)
            
        # Test postorder traversal
        # For the given data, postorder should visit left subtree (2,4,3),
        # then right subtree (6,8,7), then root (5)
        postorder_result = list(self.bst.postorder())
        expected_keys = [2, 4, 3, 6, 8, 7, 5]  # Expected order for our tree
        actual_keys = [key for key, _ in postorder_result]
        self.assertEqual(actual_keys, expected_keys)

if __name__ == '__main__':
    unittest.main()
