# todo_list.py

def load_tasks(filename):
    """Load tasks from a text file."""
    try:
        with open(filename, 'r') as file:
            tasks = file.readlines()
            return [task.strip() for task in tasks]
    except FileNotFoundError:
        return []

def save_tasks(filename, tasks):
    """Save tasks to a text file."""
    with open(filename, 'w') as file:
        for task in tasks:
            file.write(f"{task}\n")

def display_tasks(tasks):
    """Display the current tasks."""
    if not tasks:
        print("No tasks in the list.")
    else:
        print("Tasks:")
        for idx, task in enumerate(tasks, start=1):
            print(f"{idx}. {task}")

def add_task(tasks):
    """Add a new task to the list."""
    task = input("Enter the task: ")
    tasks.append(task)
    print(f'Task "{task}" added successfully!')

def remove_task(tasks):
    """Remove a task from the list."""
    display_tasks(tasks)
    try:
        task_num = int(input("Enter the task number to remove: "))
        if 0 < task_num <= len(tasks):
            removed_task = tasks.pop(task_num - 1)
            print(f'Task "{removed_task}" removed successfully!')
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def main():
    filename = 'todo_list.txt'
    tasks = load_tasks(filename)

    while True:
        print("\nTo-Do List Menu:")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Remove Task")
        print("4. Exit")
        
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
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
