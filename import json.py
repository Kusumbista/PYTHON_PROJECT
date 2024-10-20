import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import matplotlib.pyplot as plt

def load_tasks(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as file:
        return json.load(file)

def save_tasks(filename, tasks):
    with open(filename, 'w') as file:
        json.dump(tasks, file, indent=4)

def add_task(tasks, task_name, priority, category, reminder_date):
    start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tasks.append({
        'name': task_name,
        'priority': priority,
        'completed': False,
        'start_date': start_date,
        'completion_date': None,
        'category': category,
        'reminder_date': reminder_date
    })
    save_tasks(filename, tasks)
    update_task_list(tasks)

def update_task_list(tasks):
    # Clear the current tree view
    for i in task_tree.get_children():
        task_tree.delete(i)
    
    for task in tasks:
        status = "✔️" if task['completed'] else "❌"
        task_tree.insert("", "end", values=(status, task['name'], task['priority'], task['category'], task['reminder_date']))

def mark_task_completed(tasks):
    selected_item = task_tree.selection()
    if selected_item:
        task_index = task_tree.index(selected_item[0])
        tasks[task_index]['completed'] = True
        tasks[task_index]['completion_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_tasks(filename, tasks)
        update_task_list(tasks)
    else:
        messagebox.showwarning("Warning", "Please select a task to mark as completed.")

def remove_task(tasks):
    selected_item = task_tree.selection()
    if selected_item:
        task_index = task_tree.index(selected_item[0])
        tasks.pop(task_index)
        save_tasks(filename, tasks)
        update_task_list(tasks)
    else:
        messagebox.showwarning("Warning", "Please select a task to remove.")

def open_add_task_dialog():
    task_name = simpledialog.askstring("Task Name", "Enter the Task:")
    if task_name:
        priority = simpledialog.askstring("Priority", "Enter Priority (Low, Medium, High):").capitalize()
        category = simpledialog.askstring("Category", "Enter Category (e.g., Work, Personal, Shopping):")
        reminder_date = simpledialog.askstring("Reminder Date", "Set a Reminder Date (YYYY-MM-DD) or press Enter to skip:")
        add_task(tasks, task_name, priority, category, reminder_date)

def visualize_tasks(tasks):
    completed_count = sum(1 for task in tasks if task['completed'])
    uncompleted_count = len(tasks) - completed_count

    # Pie chart for task completion
    labels = ['Completed', 'Uncompleted']
    sizes = [completed_count, uncompleted_count]
    colors = ['#66c2a5', '#fc8d62']  # Colors for pie chart

    plt.figure(figsize=(8, 5))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Task Completion Status')
    plt.show()

    # Optional: Bar chart for tasks per category
    categories = {}
    for task in tasks:
        category = task['category']
        if category in categories:
            categories[category] += 1
        else:
            categories[category] = 1

    plt.figure(figsize=(10, 5))
    plt.bar(categories.keys(), categories.values(), color='#66c2a5')
    plt.xlabel('Categories')
    plt.ylabel('Number of Tasks')
    plt.title('Number of Tasks per Category')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Main application window
app = tk.Tk()
app.title("To-Do List Application")

# Load tasks from JSON file
filename = 'todo_list.json'
tasks = load_tasks(filename)

# Create a Treeview to display tasks
columns = ("Status", "Task", "Priority", "Category", "Reminder")
task_tree = ttk.Treeview(app, columns=columns, show="headings")
task_tree.heading("Status", text="Status")
task_tree.heading("Task", text="Task")
task_tree.heading("Priority", text="Priority")
task_tree.heading("Category", text="Category")
task_tree.heading("Reminder", text="Reminder")

# Set column widths
task_tree.column("Status", width=50)
task_tree.column("Task", width=250)
task_tree.column("Priority", width=100)
task_tree.column("Category", width=100)
task_tree.column("Reminder", width=100)

task_tree.pack(pady=10)

# Buttons for adding, removing, marking tasks as complete, and visualizing tasks
add_task_button = tk.Button(app, text="Add Task", command=open_add_task_dialog)
add_task_button.pack(pady=5)

remove_task_button = tk.Button(app, text="Remove Task", command=lambda: remove_task(tasks))
remove_task_button.pack(pady=5)

mark_completed_button = tk.Button(app, text="Mark as Completed", command=lambda: mark_task_completed(tasks))
mark_completed_button.pack(pady=5)

visualize_button = tk.Button(app, text="Visualize Tasks", command=lambda: visualize_tasks(tasks))
visualize_button.pack(pady=5)

update_task_list(tasks)  # Initial update of the task list

# Start the Tkinter event loop
app.mainloop()
