import unittest
from src.data_struct.Stacks import ActivityStack, ActivityNode

class TestActivityStack(unittest.TestCase):
    def setUp(self):
        self.stack = ActivityStack()
        
    def test_push_and_pop(self):
        # Test pushing single item
        result = self.stack.push("ADD", "Added book: Test Book")
        self.assertIn("Logged: ADD", result)
        
        # Test popping single item
        popped = self.stack.pop()
        self.assertEqual(popped[0], "ADD")
        self.assertEqual(popped[1], "Added book: Test Book")
        
    def test_peek(self):
        self.stack.push("ADD", "Book 1")
        self.stack.push("UPDATE", "Book 2")
        
        # Test peek returns top item without removing it
        peek_result = self.stack.peek()
        self.assertEqual(peek_result[0], "UPDATE")
        self.assertEqual(peek_result[1], "Book 2")
        
        # Verify item still exists after peek
        pop_result = self.stack.pop()
        self.assertEqual(pop_result[0], "UPDATE")
        
    def test_max_size(self):
        # Test stack maintains max size
        for i in range(15):  # Max size is 10
            self.stack.push(f"ACTION{i}", f"Details{i}")
            
        # Verify only last 10 items are kept
        actions = self.stack.get_all_actions()
        self.assertEqual(len(actions), 10)
        self.assertEqual(actions[0]["action"], "ACTION14")
        
    def test_empty_stack(self):
        # Test operations on empty stack
        self.assertIsNone(self.stack.pop())
        self.assertIsNone(self.stack.peek())
        self.assertEqual(len(self.stack.get_all_actions()), 0)
        
    def test_clear_stack(self):
        # Add some items
        self.stack.push("ADD", "Book 1")
        self.stack.push("UPDATE", "Book 2")
        
        # Clear stack
        self.stack.clear_stack()
        
        # Verify stack is empty
        self.assertEqual(self.stack.size, 0)
        self.assertIsNone(self.stack.top)
        self.assertEqual(len(self.stack.get_all_actions()), 0)

if __name__ == '__main__':
    unittest.main() 