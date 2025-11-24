import questionary
from rich.console import Console
from rich.table import Table
import json
from datetime import datetime
from features.categories.categories import get_all_categories, create_category

console = Console()
DATABASE_FILE = "database/tasks.txt"

def get_all_tasks():
    """
    This function retrieves all tasks from the database file.
    
    Returns:
        A list of task dictionaries.
    """
    try:
        with open(DATABASE_FILE, "r") as f:
            tasks = [json.loads(line) for line in f]
        return tasks
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    """
    This function saves a list of tasks to the database file.
    
    Args:
        tasks: A list of task dictionaries.
    """
    with open(DATABASE_FILE, "w") as f:
        for task in tasks:
            f.write(json.dumps(task) + "\n")

def add_task_data(title, description, category, priority, deadline, tags):
    """
    This function adds a new task to the database.
    """
    tasks = get_all_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "category": category,
        "priority": priority,
        "status": "Pending",
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "deadline": deadline.strftime("%Y-%m-%d") if deadline else None,
        "tags": tags,
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task

def add_task():
    """
    This function prompts the user for task details and adds the task to the database.
    """
    title = questionary.text("What is the title of the task?").ask()
    if not title:
        console.print("[bold red]Title is required.[/bold red]")
        return

    description = questionary.text("What is the description of the task?").ask()
    
    categories = get_all_categories()
    category_choices = [cat['name'] for cat in categories]
    category_choices.append("None")
    category_choices.append("Create New Category")

    category_name = questionary.select(
        "Select a category for the task:",
        choices=category_choices,
    ).ask()

    if category_name == "Create New Category":
        create_category()
        categories = get_all_categories()
        category_choices = [cat['name'] for cat in categories]
        category_choices.append("None")
        category_name = questionary.select(
            "Select a category for the task:",
            choices=category_choices,
        ).ask()
    
    category = category_name if category_name != "None" else ""

    priority = questionary.select(
        "What is the priority of the task?",
        choices=["Low", "Medium", "High", "Critical"],
    ).ask()
    deadline_str = questionary.text("What is the deadline for the task (YYYY-MM-DD)?").ask()

    deadline = None
    if deadline_str:
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        except ValueError:
            console.print("[bold red]Invalid date format. Please use YYYY-MM-DD.[/bold red]")
            return
    
    tags_str = questionary.text("Enter tags for the task (comma-separated, leave empty to skip):").ask()
    tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()] if tags_str else []

    add_task_data(title, description, category, priority, deadline, tags)
    console.print(f"[bold green]Task '{title}' added successfully![/bold green]")

def list_tasks():
    """
    This function lists all tasks in a table.
    """
    tasks = get_all_tasks()
    if not tasks:
        console.print("[bold yellow]No tasks found.[/bold yellow]")
        return

    table = Table(title="Tasks")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Priority", style="yellow")
    table.add_column("Category", style="blue")
    table.add_column("Deadline", style="green")
    table.add_column("Status", style="red")

    for task in tasks:
        status_color = "green" if task['status'] == 'Completed' else "yellow" if task['status'] == 'Pending' else "red"
        table.add_row(
            str(task["id"]),
            task["title"],
            task["priority"],
            task["category"],
            task["deadline"] if task["deadline"] else "N/A",
            f"[{status_color}]{task['status']}[/{status_color}]"
        )

    console.print(table)

def edit_task_data(task_id, title, description, category, priority, deadline, status, tags):
    """
    This function edits an existing task's data.
    """
    tasks = get_all_tasks()
    task_to_edit = None
    for task in tasks:
        if task["id"] == task_id:
            task_to_edit = task
            break
    
    if not task_to_edit:
        return None

    task_to_edit["title"] = title
    task_to_edit["description"] = description
    task_to_edit["category"] = category
    task_to_edit["priority"] = priority
    task_to_edit["deadline"] = deadline.strftime("%Y-%m-%d") if deadline else None
    task_to_edit["status"] = status
    task_to_edit["tags"] = tags
    save_tasks(tasks)
    return task_to_edit

def edit_task():
    """
    This function edits an existing task.
    """
    tasks = get_all_tasks()
    if not tasks:
        console.print("[bold yellow]No tasks to edit.[/bold yellow]")
        return

    list_tasks()
    task_id_str = questionary.text("Enter the ID of the task you want to edit:").ask()

    if not task_id_str or not task_id_str.isdigit():
        console.print("[bold red]Invalid ID.[/bold red]")
        return

    task_id = int(task_id_str)
    task_to_edit = None
    for task in tasks:
        if task["id"] == task_id:
            task_to_edit = task
            break

    if not task_to_edit:
        console.print("[bold red]Task not found.[/bold red]")
        return

    title = questionary.text(f"What is the new title for the task (current: {task_to_edit['title']})?", default=task_to_edit['title']).ask()
    description = questionary.text(f"What is the new description for the task (current: {task_to_edit['description']})?", default=task_to_edit['description']).ask()
    
    categories = get_all_categories()
    category_choices = [cat['name'] for cat in categories]
    category_choices.append("None")
    category_choices.append("Create New Category")

    category_name = questionary.select(
        f"Select a new category for the task (current: {task_to_edit['category']}):",
        choices=category_choices,
        default=task_to_edit['category'] if task_to_edit['category'] else "None"
    ).ask()

    if category_name == "Create New Category":
        create_category()
        categories = get_all_categories()
        category_choices = [cat['name'] for cat in categories]
        category_choices.append("None")
        category_name = questionary.select(
            f"Select a new category for the task (current: {task_to_edit['category']}):",
            choices=category_choices,
            default=task_to_edit['category'] if task_to_edit['category'] else "None"
        ).ask()
    
    category = category_name if category_name != "None" else ""

    priority = questionary.select(
        f"What is the new priority for the task (current: {task_to_edit['priority']})?",
        choices=["Low", "Medium", "High", "Critical"],
        default=task_to_edit['priority']
    ).ask()
    deadline_str = questionary.text(f"What is the new deadline for the task (YYYY-MM-DD) (current: {task_to_edit['deadline']})?", default=task_to_edit['deadline'] if task_to_edit['deadline'] else "").ask()
    status = questionary.select(
        f"What is the new status for the task (current: {task_to_edit['status']})?",
        choices=["Pending", "Completed"],
        default=task_to_edit['status']
    ).ask()

    tags_str = questionary.text(f"Enter new tags for the task (comma-separated, current: {', '.join(task_to_edit['tags'])}):", default=', '.join(task_to_edit['tags'])).ask()
    tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()] if tags_str else []

    deadline = None
    if deadline_str:
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        except ValueError:
            console.print("[bold red]Invalid date format. Please use YYYY-MM-DD.[/bold red]")
            return
    
    edit_task_data(task_id, title, description, category, priority, deadline, status, tags)
    console.print(f"[bold green]Task '{title}' updated successfully![/bold green]")

def delete_task_data(task_id):
    """
    This function deletes a task by its ID.
    """
    tasks = get_all_tasks()
    task_to_delete = None
    for task in tasks:
        if task["id"] == task_id:
            task_to_delete = task
            break
    
    if not task_to_delete:
        return False
    
    tasks.remove(task_to_delete)
    save_tasks(tasks)
    return True

def delete_task():
    """
    This function deletes a task.
    """
    tasks = get_all_tasks()
    if not tasks:
        console.print("[bold yellow]No tasks to delete.[/bold yellow]")
        return

    list_tasks()
    task_id_str = questionary.text("Enter the ID of the task you want to delete:").ask()

    if not task_id_str or not task_id_str.isdigit():
        console.print("[bold red]Invalid ID.[/bold red]")
        return

    task_id = int(task_id_str)
    task_to_delete = None
    for task in tasks:
        if task["id"] == task_id:
            task_to_delete = task
            break

    if not task_to_delete:
        console.print("[bold red]Task not found.[/bold red]")
        return

    confirm = questionary.confirm(f"Are you sure you want to delete task '{task_to_delete['title']}'?").ask()

    if confirm:
        if delete_task_data(task_id):
            console.print(f"[bold green]Task '{task_to_delete['title']}' deleted successfully![/bold green]")
        else:
            console.print(f"[bold red]Failed to delete task '{task_to_delete['title']}'.[/bold red]")

def search_and_filter_tasks():
    """
    This function allows searching and filtering tasks.
    """
    tasks = get_all_tasks()
    if not tasks:
        console.print("[bold yellow]No tasks to search or filter.[/bold yellow]")
        return

    filtered_tasks = tasks

    search_title = questionary.text("Enter title to search (leave empty to skip):").ask()
    if search_title:
        filtered_tasks = [task for task in filtered_tasks if search_title.lower() in task['title'].lower()]

    filter_category = questionary.text("Enter category to filter by (leave empty to skip):").ask()
    if filter_category:
        filtered_tasks = [task for task in filtered_tasks if filter_category.lower() == task['category'].lower()]

    filter_priority = questionary.select(
        "Filter by priority (leave empty to skip):",
        choices=["Low", "Medium", "High", "Critical", "Skip"],
        default="Skip"
    ).ask()
    if filter_priority != "Skip":
        filtered_tasks = [task for task in filtered_tasks if filter_priority == task['priority']]

    filter_status = questionary.select(
        "Filter by status (leave empty to skip):",
        choices=["Pending", "Completed", "Skip"],
        default="Skip"
    ).ask()
    if filter_status != "Skip":
        filtered_tasks = [task for task in filtered_tasks if filter_status == task['status']]

    filter_tag = questionary.text("Enter tag to filter by (leave empty to skip):").ask()
    if filter_tag:
        filtered_tasks = [task for task in filtered_tasks if any(filter_tag.lower() == t.lower() for t in task['tags'])]

    if not filtered_tasks:
        console.print("[bold yellow]No tasks found matching your criteria.[/bold yellow]")
        return

    # Display filtered tasks using a temporary list_tasks-like function
    table = Table(title="Filtered Tasks")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Priority", style="yellow")
    table.add_column("Category", style="blue")
    table.add_column("Deadline", style="green")
    table.add_column("Status", style="red")

    for task in filtered_tasks:
        status_color = "green" if task['status'] == 'Completed' else "yellow" if task['status'] == 'Pending' else "red"
        table.add_row(
            str(task["id"]),
            task["title"],
            task["priority"],
            task["category"],
            task["deadline"] if task["deadline"] else "N/A",
            f"[{status_color}]{task['status']}[/{status_color}]"
        )

    console.print(table)

if __name__ == '__main__':
    pass
