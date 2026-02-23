 # Simple Student Information System (SIS)

A robust Command Line Interface (CLI) application for managing academic records. This system implements full CRUDL functionality and ensures data persistence through CSV file handling.

## Features
- **Full CRUDL Operations**: 
  - **Create**: Add new Colleges, Programs, and Students.
  - **Read/Search**: Filter records by specific fields (e.g., search by Lastname).
  - **Update**: Modify existing records with partial update support.
  - **Delete**: Securely remove records with a user confirmation prompt.
  - **List**: Display all records in a neatly formatted table with alphabetical sorting.
- **Relational Integrity**: Prevents orphan records by validating Program and College links.
- **Data Persistence**: All data is stored in localized `.csv` files.

## Tech Stack
- **Language**: Python 3.x
- **Storage**: CSV (Flat-file database)

## Testing Guide
To verify the system logic, it is recommended to add data in this specific order:

1. **Add College**: 
   - Code: `CCS` | Name: `College of Computer Studies`
2. **Add Program**: 
   - Code: `BSCS` | Name: `Computer Science` | College: `CCS`
3. **Add Student**: 
   - ID: `2024-0001` | Name: `Cha Jane Torres` | Program: `BSCS` | Year: `2`

## File Structure
- `main.py`: Main application logic.
- `colleges.csv`, `programs.csv`, `students.csv`: Data storage files.