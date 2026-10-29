# ExpenseWise — Personal Expense Tracker

A beginner-friendly command-line expense tracker built with core Python. It stores expenses locally in JSON, summarizes monthly spending, exports reports, and warns users when they approach or exceed a monthly budget.

## Features
- Add, list, and delete expenses
- Validate amounts and dates
- Persistent local storage using JSON
- Monthly spending summaries by category
- Simple text-based category chart
- Monthly budget warnings
- Export monthly reports to a `.txt` file
- Uses only Python's standard library (no third-party packages)

## Requirements
- Python 3.9 or newer

## Run locally
1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run:

   ```bash
   python main.py
   ```

   On some systems, use `python3 main.py`.

The program creates `expenses.json` and `budget.json` automatically when you save your first expense or budget. Keep these files in the same folder as `main.py`.

## Example workflow
1. Choose `1` to add an expense, e.g. `Lunch`, `Food`, `120`.
2. Choose `4` to set a monthly budget, e.g. `5000`.
3. Choose `3` and enter a month like `2026-10` to view and export a report.

## Concepts demonstrated
- Functions and modular program structure
- Lists, dictionaries, loops, and conditionals
- Exception handling and input validation
- Reading and writing JSON files
- Date parsing with `datetime`
- Aggregation with `collections.defaultdict`
- Basic reporting and budget logic

## Future improvements
- Add a GUI using Tkinter or a web interface using Flask
- Add CSV export and data visualizations
- Add recurring expenses and income tracking
- Add unit tests and database support (SQLite)

## Resume description
**ExpenseWise | Python Personal Expense Tracker**
- Developed a command-line expense management application using core Python and JSON-based persistent storage.
- Implemented category-wise monthly spending analysis, report generation, input validation, and budget threshold alerts.
- Applied modular programming, exception handling, date processing, and file I/O to solve a practical personal-finance use case.

Only list features you have personally run and can explain during an interview.
