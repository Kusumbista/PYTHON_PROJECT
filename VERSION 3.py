import json
import os
from datetime import datetime
from tabulate import tabulate
import matplotlib.pyplot as plt

def load_tasks(filename):
    """Load tasks from a JSON file."""
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as file:
        return json.load(file)

def save_tasks(filename, tasks):
    """Save tasks to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(tasks, file, indent=4)

def display_tasks(tasks):
    """Display the current tasks in a table format."""
    if not tasks:
        print("No tasks in the list.")
    else:
        table = []
        for idx, task in enumerate(tasks, start=1):
            priority = task.get('priority', 'Low')
            status = "✓" if task.get('completed', False) else "✗"
            start_date = task.get('start_date', 'N/A')
            completion_date = task.get('completion_date', 'N/A')
            table.append([idx, task['name'], priority, status, start_date, completion_date])
        
        print(tabulate(table, headers=["No", "Task", "Priority", "Completed", "Start Date", "Completion Date"], tablefmt="grid"))

def add_task(tasks):
    """Add a new task to the list."""
    task_name = input("Enter the task: ")
    priority = input("Enter priority (Low, Medium, High): ").capitalize()
    start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tasks.append({'name': task_name, 'priority': priority, 'completed': False, 'start_date': start_date, 'completion_date': None})
    print(f'Task "{task_name}" added successfully!')

def remove_task(tasks):
    """Remove a task from the list."""
    display_tasks(tasks)
    try:
        task_num = int(input("Enter the task number to remove: "))
        if 0 < task_num <= len(tasks):
            removed_task = tasks.pop(task_num - 1)
            print(f'Task "{removed_task["name"]}" removed successfully!')
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def mark_task_completed(tasks):
    """Mark a task as completed."""
    display_tasks(tasks)
    try:
        task_num = int(input("Enter the task number to mark as completed: "))
        if 0 < task_num <= len(tasks):
            tasks[task_num - 1]['completed'] = True
            tasks[task_num - 1]['completion_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f'Task "{tasks[task_num - 1]["name"]}" marked as completed!')
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def visualize_tasks(tasks):
    """Visualize the number of completed vs. uncompleted tasks."""
    completed_tasks = sum(1 for task in tasks if task['completed'])
    uncompleted_tasks = len(tasks) - completed_tasks
    
    # Creating a pie chart
    labels = 'Completed', 'Uncompleted'
    sizes = [completed_tasks, uncompleted_tasks]
    colors = ['gold', 'lightcoral']
    explode = (0.1, 0)  # explode the 1st slice (Completed)

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Task Completion Visualization")
    plt.show()

def main():
    filename = 'todo_list.json'
    tasks = load_tasks(filename)

    while True:
        print("\nTo-Do List Menu:")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Remove Task")
        print("4. Mark Task Completed")
        print("5. Visualize Task Completion")
        print("6. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            display_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
            save_tasks(filename, tasks)
        elif choice == '3':
            remove_task(tasks)
            save_tasks(filename, tasks)
        elif choice == '4':
            mark_task_completed(tasks)
            save_tasks(filename, tasks)
        elif choice == '5':
            visualize_tasks(tasks)
        elif choice == '6':
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
