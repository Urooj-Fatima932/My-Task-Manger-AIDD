import questionary
from rich.console import Console
from rich.table import Table
import json
from features.tasks import tasks

console = Console()
CATEGORIES_FILE = "database/categories.txt"

def get_all_categories():
    """
    This function retrieves all categories from the database file.
    
    Returns:
        A list of category dictionaries.
    """
    try:
        with open(CATEGORIES_FILE, "r") as f:
            categories = [json.loads(line) for line in f]
        return categories
    except FileNotFoundError:
        return []

def save_categories(categories):
    """
    This function saves a list of categories to the database file.
    
    Args:
        categories: A list of category dictionaries.
    """
    with open(CATEGORIES_FILE, "w") as f:
        for category in categories:
            f.write(json.dumps(category) + "\n")

def create_category_data(category_name):
    """
    This function creates a new category.
    """
    if not category_name:
        return None, "Category name is required."

    categories = get_all_categories()
    
    for category in categories:
        if category['name'].lower() == category_name.lower():
            return None, "Category already exists."

    new_category = {
        "id": len(categories) + 1,
        "name": category_name,
    }

    categories.append(new_category)
    save_categories(categories)
    return new_category, "Category created successfully."

def create_category():
    """
    This function prompts the user for a category name and creates a new category.
    """
    category_name = questionary.text("What is the name of the category?").ask()
    new_category, message = create_category_data(category_name)
    if new_category:
        console.print(f"[bold green]Category '{category_name}' created successfully![/bold green]")
    else:
        console.print(f"[bold red]{message}[/bold red]")

def list_categories():
    """
    This function lists all categories in a table.
    """
    categories = get_all_categories()
    if not categories:
        console.print("[bold yellow]No categories found.[/bold yellow]")
        return

    table = Table(title="Categories")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="magenta")

    for category in categories:
        table.add_row(
            str(category["id"]),
            category["name"],
        )

    console.print(table)

def category_summary():
    """
    This function displays a summary of tasks for each category.
    """
    categories = get_all_categories()
    if not categories:
        console.print("[bold yellow]No categories found.[/bold yellow]")
        return

    all_tasks = tasks.get_all_tasks()

    table = Table(title="Category Summary")
    table.add_column("Category", style="cyan")
    table.add_column("Total Tasks", style="magenta")
    table.add_column("Completed Tasks", style="green")
    table.add_column("Pending Tasks", style="yellow")

    for category in categories:
        category_tasks = [task for task in all_tasks if task['category'] == category['name']]
        total_tasks = len(category_tasks)
        completed_tasks = len([task for task in category_tasks if task['status'] == 'Completed'])
        pending_tasks = total_tasks - completed_tasks
        table.add_row(
            category["name"],
            str(total_tasks),
            str(completed_tasks),
            str(pending_tasks),
        )
    console.print(table)

from collections import Counter

def tag_insights():
    """
    This function displays insights about the most used tags.
    """
    all_tasks = tasks.get_all_tasks()
    if not all_tasks:
        console.print("[bold yellow]No tasks found to generate tag insights.[/bold yellow]")
        return

    all_tags = []
    for task in all_tasks:
        all_tags.extend(task.get('tags', []))

    if not all_tags:
        console.print("[bold yellow]No tags found in tasks.[/bold yellow]")
        return

    tag_counts = Counter(tag.lower() for tag in all_tags)
    most_common_tags = tag_counts.most_common()

    table = Table(title="Tag Insights (Most Used Tags)")
    table.add_column("Tag", style="cyan")
    table.add_column("Count", style="magenta")

    for tag, count in most_common_tags:
        table.add_row(tag, str(count))
    
    console.print(table)

if __name__ == '__main__':
    pass
