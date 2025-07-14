# Library Management System - User Guide

## Table of Contents
1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Features](#features)
   - [Book Management](#book-management)
   - [Search Operations](#search-operations)
   - [Checkout System](#checkout-system)
   - [Data Structure Visualization](#data-structure-visualization)
4. [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites
- Python 3.8 or higher
- SQLite3
- Required Python packages (install using pip):
  ```bash
  pip install -r requirements.txt
  ```

### Setup Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/dsa-semester-project-ics-2025-developers.git
   cd dsa-semester-project-ics-2025-developers
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python src/main.py
   ```

## Getting Started

Upon launching the application, you'll be presented with the main interface featuring multiple tabs for different operations.

[Screenshot: Main Interface]
*Main interface showing the application's tab-based navigation*

## Features

### Book Management

#### Adding a New Book
1. Click on the "Books" tab
2. Click "Add New Book" button
3. Fill in the required fields:
   - ISBN
   - Title
   - Author
   - Publication Year
   - Quantity
4. Click "Save" to add the book

[Screenshot: Add Book Form]
*Form for adding a new book to the system*

#### Editing Book Information
1. Select a book from the list
2. Click "Edit" button
3. Modify the desired fields
4. Click "Save" to update

[Screenshot: Edit Book]
*Interface for editing existing book information*

#### Deleting Books
1. Select a book from the list
2. Click "Delete" button
3. Confirm deletion in the popup dialog

[Screenshot: Delete Confirmation]
*Confirmation dialog for book deletion*

### Search Operations

The system uses a Binary Search Tree for efficient book searches:

1. Navigate to the "Search" tab
2. Enter search criteria:
   - ISBN (fastest search using BST)
   - Title
   - Author
3. Results appear in real-time as you type

[Screenshot: Search Interface]
*Search interface showing real-time results*

### Checkout System

#### Checking Out Books
1. Navigate to "Checkout" tab
2. Enter student/member ID
3. Scan or enter book ISBN
4. Set return date
5. Click "Checkout"

[Screenshot: Checkout Process]
*Book checkout interface with member details*

#### Managing Returns
1. Go to "Checkout" tab
2. Click "Returns" section
3. Enter book ISBN or scan barcode
4. Click "Return"

[Screenshot: Returns Interface]
*Interface for processing book returns*

### Data Structure Visualization

The system provides real-time visualization of internal data structures:

#### Binary Search Tree Viewer
- Shows book organization by ISBN
- Highlights search paths
- Updates in real-time

[Screenshot: BST Visualization]
*Visual representation of the Binary Search Tree*

#### Queue Visualization
- Shows pending checkouts
- Displays waitlist for popular books

[Screenshot: Queue Display]
*Queue visualization for pending checkouts*

#### Stack Operations
- Displays recent activities
- Shows undo history

[Screenshot: Stack Visualization]
*Stack visualization showing recent operations*

## Troubleshooting

### Common Issues and Solutions

1. **Database Connection Error**
   - Ensure SQLite is properly installed
   - Check file permissions
   - Verify database file exists in correct location

2. **Search Not Working**
   - Clear search field and try again
   - Ensure correct search criteria is selected
   - Check if database is properly populated

3. **GUI Not Responding**
   - Restart the application
   - Check system resources
   - Verify Python version compatibility

### Error Messages

| Error Code | Description | Solution |
|------------|-------------|----------|
| DB001 | Database connection failed | Check database file permissions |
| GUI001 | Interface not responding | Restart application |
| DS001 | Data structure corruption | Clear and rebuild indexes |

For additional support or to report issues, please contact the development team or create an issue on the project's GitHub repository. 