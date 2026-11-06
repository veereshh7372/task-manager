import streamlit as st
from database import add_task, get_all_tasks, complete_task, delete_task, update_task, uncomplete_task

# Page configuration
st.set_page_config(page_title="Task Manager", page_icon="✓", layout="wide")

st.title("📋 Task Manager")
st.markdown("---")

# Sidebar for adding new tasks
st.sidebar.header("Add New Task")

with st.sidebar.form("add_task_form"):
    title = st.text_input("Task Title *", placeholder="Enter task title")
    description = st.text_area("Description", placeholder="Enter task description")
    due_date = st.date_input("Due Date")
    priority = st.selectbox("Priority", ["low", "medium", "high"])
    
    submitted = st.form_submit_button("Add Task")
    if submitted and title:
        add_task(title, description, str(due_date), priority)
        st.success("Task added successfully!")
        st.rerun()

# Main content area
st.header("Your Tasks")

# Filter options
col1, col2, col3 = st.columns(3)
with col1:
    filter_status = st.selectbox("Filter by Status", ["all", "pending", "completed"])
with col2:
    filter_priority = st.selectbox("Filter by Priority", ["all", "high", "medium", "low"])
with col3:
    sort_by = st.selectbox("Sort By", ["created_at", "priority", "due_date"])

# Get all tasks
tasks = get_all_tasks()

# Apply filters
filtered_tasks = []
for task in tasks:
    task_id, title, description, due_date, priority, status, created_at, completed_at = task
    
    # Status filter
    if filter_status != "all" and status != filter_status:
        continue
    
    # Priority filter
    if filter_priority != "all" and priority != filter_priority:
        continue
    
    filtered_tasks.append(task)

# Display tasks
if filtered_tasks:
    for task in filtered_tasks:
        task_id, title, description, due_date, priority, status, created_at, completed_at = task
        
        # Task card
        with st.container():
            col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
            
            with col1:
                if status == "completed":
                    st.markdown(f"~~**{title}**~~")
                else:
                    st.markdown(f"**{title}**")
                if description:
                    st.caption(description)
            
            with col2:
                priority_badge = f"🔴 {priority}" if priority == "high" else f"🟡 {priority}" if priority == "medium" else f"🟢 {priority}"
                st.markdown(priority_badge)
                if due_date:
                    st.caption(f"📅 {due_date}")
            
            with col3:
                if status == "completed":
                    st.success("✓ Completed")
                    if completed_at:
                        st.caption(f"at {completed_at[:16]}")
                else:
                    st.info("○ Pending")
            
            with col4:
                if status == "pending":
                    if st.button("✓ Complete", key=f"complete_{task_id}"):
                        complete_task(task_id)
                        st.rerun()
                else:
                    if st.button("↩ Undo", key=f"undo_{task_id}"):
                        uncomplete_task(task_id)
                        st.rerun()
                
                if st.button("🗑 Delete", key=f"delete_{task_id}"):
                    delete_task(task_id)
                    st.rerun()
            
            st.markdown("---")
else:
    st.info("No tasks found. Add a task from the sidebar!")

# Statistics
st.header("Statistics")
tasks = get_all_tasks()
total_tasks = len(tasks)
completed_tasks = len([t for t in tasks if t[5] == "completed"])
pending_tasks = total_tasks - completed_tasks

col1, col2, col3 = st.columns(3)
col1.metric("Total Tasks", total_tasks)
col2.metric("Completed", completed_tasks)
col3.metric("Pending", pending_tasks)
