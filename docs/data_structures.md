# Data Structures Documentation

This document provides detailed information about each data structure implemented in the Library Management System, including their purpose, implementation details, and complexity analysis.

## Binary Search Tree (BST)

### Purpose
The BST is used for efficient book searches using ISBN as the key. It provides fast lookups while maintaining sorted order.

### Implementation Details
```python
class TreeNode:
    def __init__(self, key, data):
        self.key = key      # ISBN
        self.data = data    # Book details
        self.left = None    # Left subtree
        self.right = None   # Right subtree
```

### Operations and Complexity

1. **Search**
   - Time: O(log n) average, O(n) worst case
   - Space: O(h) where h is height (recursion stack)
   - Implementation: Binary traversal comparing ISBN values
   ```python
   if key == node.key: return node.data
   if key < node.key: go left
   else: go right
   ```

2. **Insert**
   - Time: O(log n) average, O(n) worst case
   - Space: O(h) for recursion
   - Process: Traverse to leaf position and add new node

3. **Delete**
   - Time: O(log n) average, O(n) worst case
   - Space: O(h) for recursion
   - Steps:
     1. Find node
     2. If leaf: Remove directly
     3. If one child: Replace with child
     4. If two children: Find successor

### Best Practices
- Keep tree balanced for O(log n) operations
- Use string comparison for ISBN
- Handle duplicates by updating data

## Stack (Activity Log)

### Purpose
Maintains history of recent operations for undo functionality and activity tracking.

### Implementation Details
```python
class ActivityNode:
    def __init__(self, action, details):
        self.action = action        # Operation type
        self.details = details      # Operation details
        self.timestamp = datetime.now()
        self.next = None           # Next node in stack
```

### Operations and Complexity

1. **Push (Add Activity)**
   - Time: O(1)
   - Space: O(1)
   - Implementation: Add to top of stack

2. **Pop (Undo)**
   - Time: O(1)
   - Space: O(1)
   - Implementation: Remove and return top node

3. **Peek**
   - Time: O(1)
   - Space: O(1)
   - Implementation: Return top without removing

4. **Get All Actions**
   - Time: O(n) where n is stack size
   - Space: O(n) for return array
   - Implementation: Traverse and collect all nodes

### Memory Management
- Maximum size: 10 activities
- Auto-removal of oldest activity when full
- Constant memory footprint

## Queue (Checkout Waitlist)

### Purpose
Manages book reservation waitlist in first-come-first-served order.

### Implementation Details
```python
class QueueNode:
    def __init__(self, data):
        self.data = data    # User and book info
        self.next = None    # Next in queue
```

### Operations and Complexity

1. **Enqueue (Add to Waitlist)**
   - Time: O(1)
   - Space: O(1)
   - Implementation: Add to rear of queue

2. **Dequeue (Process Next)**
   - Time: O(1)
   - Space: O(1)
   - Implementation: Remove from front

3. **Check Empty**
   - Time: O(1)
   - Space: O(1)
   - Implementation: Size counter check

### Queue Management
- FIFO principle for fairness
- Automatic notification system
- Size tracking for status updates

## Linked List (Book History)

### Purpose
Maintains chronological history of book operations with efficient sequential access.

### Implementation Details
```python
class Node:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True
        self.next = None
```

### Operations and Complexity

1. **Add Book**
   - Time: O(1) with tail pointer
   - Space: O(1)
   - Implementation: Append to tail

2. **Delete Book**
   - Time: O(n) for search
   - Space: O(1)
   - Implementation: Linear search and relink

3. **Search by Title**
   - Time: O(n)
   - Space: O(1)
   - Implementation: Linear traversal

4. **Get All Books**
   - Time: O(n)
   - Space: O(n) for return array
   - Implementation: Traverse and collect

### Optimization
- Tail pointer for O(1) insertions
- No sorting required
- Sequential access pattern

## Dictionary (Hash Table)

### Purpose
Provides instant book lookups using ISBN as key.

### Implementation Details
```python
class BookDictionary:
    def __init__(self):
        self.books = {}  # ISBN to Book mapping
```

### Operations and Complexity

1. **Add Book**
   - Time: O(1) average
   - Space: O(1)
   - Implementation: Direct hash table insert

2. **Delete Book**
   - Time: O(1) average
   - Space: O(1)
   - Implementation: Hash table deletion

3. **Search by ISBN**
   - Time: O(1) average
   - Space: O(1)
   - Implementation: Direct hash lookup

4. **Search by Title**
   - Time: O(n)
   - Space: O(n) for results
   - Implementation: Linear scan of values

### Performance Considerations
- Load factor monitoring
- Collision handling (Python dict)
- Memory usage vs access speed

## Integration Points

### Data Structure Interactions
1. BST + Dictionary
   - Complementary search capabilities
   - BST for range queries
   - Dictionary for exact matches

2. Queue + Stack
   - Queue tracks future actions
   - Stack records past actions
   - Synchronized state management

3. Linked List + Stack
   - History tracking
   - Chronological operation record
   - Audit capability

### Consistency Maintenance
- Synchronized updates across structures
- Transaction-like operations
- Error state recovery

## Performance Optimization

### Memory Management
1. Stack
   - Fixed size limit (10 items)
   - Automatic cleanup
   - Constant memory footprint

2. Dictionary
   - Space-time tradeoff
   - Direct access benefit
   - Memory overhead acceptance

### Time Optimization
1. BST
   - No explicit balancing
   - Acceptable for library scale
   - ISBN distribution naturally balanced

2. Queue
   - O(1) operations priority
   - No unnecessary traversals
   - Direct state tracking

## Testing Considerations

### Unit Tests
- Individual data structure validation
- Edge case coverage
- Performance verification

### Integration Tests
- Cross-structure consistency
- Operation atomicity
- State synchronization

