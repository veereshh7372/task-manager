# Task Manager

A simple, free task management system built with Python, SQLite, and Streamlit.

## Features

- ✅ Add, edit, and delete tasks
- ✅ Mark tasks as complete/incomplete
- ✅ Set due dates and priority levels
- ✅ Filter tasks by status and priority
- ✅ Sort tasks by date, priority, or due date
- ✅ View task statistics
- ✅ Local SQLite database (no cloud costs)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at http://localhost:8501

## Usage

- **Add Task**: Use the sidebar form to add new tasks
- **Complete Task**: Click the "✓ Complete" button on any pending task
- **Undo Completion**: Click the "↩ Undo" button on completed tasks
- **Delete Task**: Click the "🗑 Delete" button to remove a task
- **Filter**: Use the filter dropdowns to show specific tasks
- **Sort**: Change the sort order using the dropdown

## Database

The application uses SQLite database (`tasks.db`) stored locally. All data persists between sessions.

## Tech Stack

- **Backend**: Python
- **Database**: SQLite
- **Frontend**: Streamlit
