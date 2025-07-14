[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/__oZ-IAL)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=19822243&assignment_repo_type=AssignmentRepo)

# Library Management System

A comprehensive library management system implementing various data structures for efficient book management, searching, and checkout operations.

## Features

- Book management (Add, Update, Delete, Search)
- Checkout system with waiting queue
- Multiple search methods using different data structures
- Activity logging and visualization
- SQLite database persistence

## Data Structures Implementation

### 1. Binary Search Tree (BST)
Used for efficient book searches by ISBN

**Time Complexities:**
- Search: O(log n) - average case, O(n) - worst case
- Insert: O(log n) - average case, O(n) - worst case
- Delete: O(log n) - average case, O(n) - worst case

**Space Complexity:** O(n)

### 2. Queue
Used for managing book checkout waitlist

**Time Complexities:**
- Enqueue: O(1)
- Dequeue: O(1)
- Front/Rear access: O(1)

**Space Complexity:** O(n)

### 3. Linked List
Used for maintaining book history

**Time Complexities:**
- Insert at end: O(1) with tail pointer
- Delete: O(n)
- Search: O(n)
- Get all books: O(n)

**Space Complexity:** O(n)

### 4. Stack
Used for activity logging

**Time Complexities:**
- Push: O(1)
- Pop: O(1)
- Peek: O(1)
- Get all actions: O(n)

**Space Complexity:** O(n)

### 5. Dictionary (Hash Table)
Used for quick book lookups

**Time Complexities:**
- Add: O(1) average
- Delete: O(1) average
- Search by ISBN: O(1) average
- Search by title: O(n)

**Space Complexity:** O(n)

## Setup and Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python src/main.py
   ```

## Project Structure

```
dsa-semester-project/
├── src/
│   ├── data_struct/      # Data structure implementations
│   ├── database/         # Database operations
│   ├── ui/              # GUI implementation
│   ├── main.py          # Application entry point
│   └── tests.py         # Unit tests
├── tests/               # Additional test files
├── app_data.db          # SQLite database
└── requirements.txt     # Project dependencies
```

## Testing

Run tests using:
```bash
python -m pytest tests/
```

## Contributing

1. Create a feature branch:
   ```bash
   git checkout -b regNo_<YourRegNo>_<ModuleName>
   ```
2. Make your changes
3. Submit a pull request

## License

This project is part of the Data Structures & Algorithms course at Strathmore University.
