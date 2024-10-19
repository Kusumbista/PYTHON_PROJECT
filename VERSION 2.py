import json
import os

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
    """Display the current tasks."""
    if not tasks:
        print("No tasks in the list.")
    else:
        print("Tasks:")
        for idx, task in enumerate(tasks, start=1):
            priority = task.get('priority', 'Low')
            status = task.get('completed', False)
            status_display = "✓" if status else "✗"
            print(f"{idx}. [{status_display}] {task['name']} (Priority: {priority})")

def add_task(tasks):
    """Add a new task to the list."""
    task_name = input("Enter the task: ")
    priority = input("Enter priority (Low, Medium, High): ").capitalize()
    tasks.append({'name': task_name, 'priority': priority, 'completed': False})
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
            print(f'Task "{tasks[task_num - 1]["name"]}" marked as completed!')
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def main():
    filename = 'todo_list.json'
    tasks = load_tasks(filename)

    while True:
        print("\nTo-Do List Menu:")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Remove Task")
        print("4. Mark Task Completed")
        print("5. Exit")
        
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
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()