# Student Result Analysis System (Python + Tkinter + DAA)

A beginner-friendly desktop mini-project using Tkinter, SQLite, Quick Sort,
Merge Sort, and Linear Search.

## Features
- Add, view, update, and delete student records (CRUD)
- Five subjects: Python, DAA, DBMS, Java, OS
- Automatic total, percentage, and grade calculation
- Dashboard cards: student count, class average, topper
- Search by UID or student name using Linear Search
- Sort by percentage, name, or UID using manually implemented Quick Sort
- Generate a sorted list using manually implemented Merge Sort
- SQLite database persistence

## Requirements
- Python 3.9 or newer
- Tkinter (usually included with standard Windows Python installation)
- SQLite (included with Python)

No third-party packages are required.

## How to run on Windows
1. Extract the ZIP file.
2. Open the extracted `Student_Result_Analysis_Tkinter` folder.
3. Click the address bar in File Explorer, type `cmd`, and press Enter.
4. Run:

   ```bash
   python main.py
   ```

If `python` does not work, try:

```bash
py main.py
```

## How to use
1. Enter a unique Student UID and student name.
2. Enter marks from 0 to 100 for each subject.
3. Click **Add Student**.
4. Select a row to load its details into the form.
5. Click **Update Selected** or **Delete Selected** as needed.
6. Use the search box to find a UID or name.
7. Choose a sort field and click **Quick Sort** or **Merge Sort**.
8. Click **Result Analysis** for class summary.

## Grade scale
- A+: 90–100
- A: 80–89.99
- B: 70–79.99
- C: 60–69.99
- D: 50–59.99
- F: below 50

The sample application uses a 40% pass threshold in the class analysis.
Adjust the threshold and grading scale in `main.py` if your institution uses
different rules.

## Project structure
```text
Student_Result_Analysis_Tkinter/
├── main.py
├── database.py
├── students.db       # created automatically on first run
├── algorithms/
│   ├── __init__.py
│   ├── sorting.py
│   └── searching.py
└── README.md
```

## DAA complexity
| Algorithm | Average time | Worst time | Extra space |
|---|---:|---:|---:|
| Quick Sort | O(n log n) | O(n²) | O(n) in this recursive implementation |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) in this slicing implementation |
| Linear Search | O(n) | O(n) | O(k) for returned matches |

This is an educational mini-project. It is not intended for storing sensitive
or official student records.
