
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=19822243&assignment_repo_type=AssignmentRepo)

# Library Management System

A Python desktop application implementing multiple data structures to manage a library system efficiently.

## Features

- Book management (add, search, update, delete)
- Checkout system with waitlist
- Activity logging with undo capability
- Real-time data structure visualization
- Modern Tkinter GUI interface

##  Data Structures Implementation

### 1. Binary Search Tree (BST)
Used for efficient book searches by ISBN.
```
Operations:
- Search: O(log n) - Binary traversal
- Insert: O(log n) - Binary traversal
- Delete: O(log n) - Binary traversal + successor finding
Space Complexity: O(n) - One node per book
```

### 2. Stack
Used for activity logging and undo operations.
```
Operations:
- Push: O(1) - Add to top
- Pop: O(1) - Remove from top
- Peek: O(1) - View top
Space Complexity: O(1) - Limited to 10 most recent actions
```

### 3. Queue
Used for managing book checkout waitlists.
```
Operations:
- Enqueue: O(1) - Add to rear
- Dequeue: O(1) - Remove from front
- Check Empty: O(1) - Size tracking
Space Complexity: O(n) - n is number of waiting users
```

### 4. Linked List
Used for maintaining book history.
```
Operations:
- Add: O(1) - Tail tracking
- Delete: O(n) - Linear search
- Search: O(n) - Linear traversal
Space Complexity: O(n) - One node per history entry
```

### 5. Dictionary
Used for instant book lookups.
```
Operations:
- Add: O(1) average - Hash table insert
- Delete: O(1) average - Hash table delete
- Search: O(1) average - Hash table lookup
Space Complexity: O(n) - One entry per book
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Tkinter (usually comes with Python)
- SQLite3 (comes with Python)

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/your-org/dsa-semester-project-ics-2025-developers.git
cd dsa-semester-project-ics-2025-developers
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

1. Navigate to the src directory:
```bash
cd src
```

2. Run the main application:
```bash
python main.py
```

## 📝 Usage Guide

### Adding a Book
1. Enter ISBN (13 digits)
2. Fill in title and author
3. Click "Add Book"

### Searching Books
1. Enter ISBN
2. Click "Search Book"
3. Results will appear in a dialog

### Checking Out Books
1. Enter ISBN
2. Enter username
3. Click "Checkout Book"
4. If book unavailable, user will be added to waitlist

### Viewing History
- Click "Show History" to view book operations
- Use "Undo Last" to reverse recent actions
- Check "Queue Status" for current checkouts and waitlist

## 🔍 Code Structure

```
src/
├── data_struct/         # Data structure implementations
│   ├── Bsearch.py      # Binary Search Tree
│   ├── Stacks.py       # Activity logging stack
│   ├── queue.py        # Checkout queue
│   ├── linkedList.py   # History tracking
│   └── BookDictionary.py # Quick lookups
├── database/           # Database operations
│   └── sqlite.py      # SQLite interface
├── ui/                # User interface
│   └── gui_appl.py   # Tkinter GUI
├── tests/            # Unit tests
└── main.py          # Application entry point
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

## 👥 Contributing

1. Create a feature branch:
```bash
git checkout -b regNo_<YourRegNo>_<ModuleName>
```

2. Make your changes and test
3. Submit a pull request
4. Get review from teammate
5. Merge after approval

## 📚 Documentation

For detailed documentation on each data structure and their implementations, see:
- [Data Structures Documentation](docs/data_structures.md)
- [User Guide](docs/user_guide.md)


