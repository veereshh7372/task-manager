import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import os

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate('firebase_credentials.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://task-manager-1ed05-default-rtdb.firebaseio.com'
    })

def add_task(title, description='', due_date='', priority='medium'):
    """Add a new task to Firebase."""
    ref = db.reference('tasks')
    new_task_ref = ref.push({
        'title': title,
        'description': description,
        'due_date': due_date,
        'priority': priority,
        'status': 'pending',
        'created_at': datetime.now().isoformat(),
        'completed_at': None
    })
    return new_task_ref.key

def get_all_tasks():
    """Get all tasks from Firebase."""
    ref = db.reference('tasks')
    tasks = ref.get()
    
    if not tasks:
        return []
    
    # Convert to list of tuples for compatibility with existing code
    task_list = []
    for task_id, task_data in tasks.items():
        task_list.append((
            task_id,
            task_data.get('title', ''),
            task_data.get('description', ''),
            task_data.get('due_date', ''),
            task_data.get('priority', 'medium'),
            task_data.get('status', 'pending'),
            task_data.get('created_at', ''),
            task_data.get('completed_at', None)
        ))
    
    # Sort: completed last, then by priority, then by created_at
    task_list.sort(key=lambda x: (
        1 if x[5] == 'completed' else 0,
        {'high': 3, 'medium': 2, 'low': 1}.get(x[4], 0),
        x[6]
    ), reverse=True)
    
    return task_list

def complete_task(task_id):
    """Mark a task as completed."""
    ref = db.reference(f'tasks/{task_id}')
    ref.update({
        'status': 'completed',
        'completed_at': datetime.now().isoformat()
    })

def delete_task(task_id):
    """Delete a task from Firebase."""
    ref = db.reference(f'tasks/{task_id}')
    ref.delete()

def update_task(task_id, title, description, due_date, priority):
    """Update an existing task."""
    ref = db.reference(f'tasks/{task_id}')
    ref.update({
        'title': title,
        'description': description,
        'due_date': due_date,
        'priority': priority
    })

def uncomplete_task(task_id):
    """Mark a task as pending (undo completion)."""
    ref = db.reference(f'tasks/{task_id}')
    ref.update({
        'status': 'pending',
        'completed_at': None
    })
