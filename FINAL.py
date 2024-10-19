import json
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate

def load_tasks(filename):
   
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as file:
        return json.load(file)

def save_tasks(filename, tasks):
   
    with open(filename, 'w') as file:
        json.dump(tasks, file, indent=4)

def export_tasks(filename, tasks):
    
    with open(filename, 'w') as file:
        json.dump(tasks, file, indent=4)
    print(f'Tasks exported to {filename} successfully!')

def import_tasks(filename):
    
    if not os.path.exists(filename):
        print(f"File {filename} does not exist.")
        return []
    with open(filename, 'r') as file:
        return json.load(file)

def display_tasks(tasks):
    
    if not tasks:
        print("No tasks in the list.")
    else:
        table = []
        for idx, task in enumerate(tasks, start=1):
            priority = task.get('priority', 'Low')
            status = "✓" if task.get('completed', False) else "✗"
            start_date = task.get('start_date', 'N/A')
            completion_date = task.get('completion_date', 'N/A')
            category = task.get('category', 'N/A')
            reminder_date = task.get('reminder_date', 'N/A')
            table.append([idx, task['name'], priority, status, start_date, completion_date, category, reminder_date])
        
        print(tabulate(table, headers=["No", "Task", "Priority", "Completed", "Start Date", "Completion Date", "Category", "Reminder Date"], tablefmt="grid"))

def add_task(tasks):
    
    task_name = input("Enter the Task: ")
    priority = input("Enter Priority (Low, Medium, High): ").capitalize()
    category = input("Enter Category (e.g., Work, Personal, Shopping): ")
    reminder_input = input("Set a Reminder Date (YYYY-MM-DD) or press Enter to skip: ")
    reminder_date = reminder_input if reminder_input else None
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
    print(f'Task "{task_name}" added successfully!')

def remove_task(tasks):
    
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
    completed_tasks = [task['name'] for task in tasks if task['completed']]
    uncompleted_tasks = [task['name'] for task in tasks if not task['completed']]
    
    # Pie Chart
    labels = ['Completed', 'Uncompleted']
    sizes = [len(completed_tasks), len(uncompleted_tasks)]
    colors = ['#F2C9A1', '#E6B69A']  # Nude color palette
    explode = (0.1, 0)  # explode the 1st slice (Completed)

    plt.figure(figsize=(14, 7))

    # Pie Chart
    plt.subplot(1, 2, 1)
    wedges, texts, autotexts = plt.pie(
        sizes, 
        explode=explode, 
        labels=labels, 
        colors=colors, 
        autopct='%1.1f%%', 
        shadow=True, 
        startangle=90, 
        textprops={'fontsize': 14}
    )
    
    # Enhance pie chart text
    for text in texts:
        text.set_fontsize(14)
        text.set_color('#5D3A28')  # Darker color for labels

    for autotext in autotexts:
        autotext.set_color('white')  # White color for percentage
        autotext.set_fontsize(12)

    plt.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle
    plt.title("Task Completion Visualization", fontsize=16, fontweight='bold')

    # Line Chart
    plt.subplot(1, 2, 2)
    task_names = [task['name'] for task in tasks]
    task_status = [1 if task['completed'] else 0 for task in tasks]  # 1 for completed, 0 for not completed

    # Use different colors for completed and uncompleted tasks
    plt.plot(task_names, task_status, marker='o', linestyle='-', color='#D29F84', linewidth=2, markersize=8, label='Task Status')

    # Add fill between completed and uncompleted tasks
    plt.fill_between(task_names, task_status, color='#EFD8D3', alpha=0.3)

    # Adding gridlines for better readability
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Adding labels above the markers
    for i, task in enumerate(tasks):
        plt.text(i, task_status[i] + 0.05, task['name'], ha='center', fontsize=10, rotation=45)

    plt.yticks([0, 1], ['Not Completed', 'Completed'])
    plt.xticks(rotation=45, ha='right')
    plt.title("Task Completion Status", fontsize=16, fontweight='bold')
    plt.xlabel("Tasks", fontsize=14)
    plt.ylabel("Status", fontsize=14)
    plt.legend(loc='upper left')

    plt.tight_layout()
    plt.show()

def check_reminders(tasks):
    
    for task in tasks:
        if task.get('reminder_date'):
            reminder_date = datetime.strptime(task['reminder_date'], "%Y-%m-%d")
            if reminder_date <= datetime.now() + timedelta(days=1) and not task['completed']:
                print(f"Reminder: Task '{task['name']}' is due on {reminder_date.date()}.")

def main():
    filename = 'todo_list.json'
    tasks = load_tasks(filename)

    while True:
        check_reminders(tasks) 
        print("\nTo-Do List Menu:")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Remove Task")
        print("4. Mark Task Completed")
        print("5. Visualize Task Completion")
        print("6. Export Tasks")
        print("7. Import Tasks")
        print("8. Exit")
        
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
            export_filename = input("Enter filename to export tasks (e.g., export_tasks.json): ")
            export_tasks(export_filename, tasks)
        elif choice == '7':
            import_filename = input("Enter filename to import tasks (e.g., tasks.json): ")
            imported_tasks = import_tasks(import_filename)
            tasks.extend(imported_tasks)
            save_tasks(filename, tasks)
        elif choice == '8':
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
