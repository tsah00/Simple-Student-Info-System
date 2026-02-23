# Simple Student Information System (SIS)

A Python-based Command Line Interface (CLI) application designed to manage academic records using a flat-file database approach.

## Features
- **Full CRUDL Implementation**: Create, Read, Update, Delete, and List operations for Colleges, Programs, and Students.
- **Data Persistence**: Uses `csv` files to ensure data is saved permanently on the local disk.
- **Relational Integrity**:
  - Validates that a `Student` can only be enrolled in a `Program` that already exists.
  - Prevents duplicate Primary Keys (IDs and Codes) across all tables.
- **Search & Sort**: 
  - Search functionality filtered by specific fields (e.g., search by Firstname).
  - Alphabetical sorting for organized data viewing.
- **Formatted UI**: Uses text-alignment logic to display CSV data in a clean, readable table format.

## Tech Stack
- **Language**: Python 3.x
- **Storage**: CSV (Comma Separated Values)
- **Libraries**: `csv`, `os` (Standard Libraries)

## File Structure
- `main.py`: The core application logic and UI.
- `students.csv`: Stores student profiles.
- `programs.csv`: Stores academic program details.
- `colleges.csv`: Stores college department information.

## How to Use
1. Run the program: `python main.py`
2. **Important**: Add a **College** first, then a **Program**, before adding a **Student** to maintain relational links.