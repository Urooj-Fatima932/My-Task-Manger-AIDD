import questionary
from rich.console import Console
import json
import csv
from features.tasks import tasks
from features.reminders import reminders

console = Console()

def export_tasks_to_csv():
    """
    Exports all tasks to a CSV file.
    """
    all_tasks = tasks.get_all_tasks()
    if not all_tasks:
        console.print("[bold yellow]No tasks found to export.[/bold yellow]")
        return

    file_name = questionary.text("Enter the CSV file name for tasks (e.g., tasks.csv):", default="tasks.csv").ask()
    if not file_name:
        console.print("[bold red]File name is required.[/bold red]")
        return

    try:
        with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'title', 'description', 'category', 'priority', 'status', 'created_at', 'deadline', 'tags']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for task in all_tasks:
                # Convert tags list to a comma-separated string for CSV
                task['tags'] = ','.join(task['tags'])
                writer.writerow(task)
        console.print(f"[bold green]Tasks exported successfully to {file_name}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error exporting tasks to CSV: {e}[/bold red]")

def export_tasks_to_json():
    """
    Exports all tasks to a JSON file.
    """
    all_tasks = tasks.get_all_tasks()
    if not all_tasks:
        console.print("[bold yellow]No tasks found to export.[/bold yellow]")
        return

    file_name = questionary.text("Enter the JSON file name for tasks (e.g., tasks.json):", default="tasks.json").ask()
    if not file_name:
        console.print("[bold red]File name is required.[/bold red]")
        return

    try:
        with open(file_name, 'w', encoding='utf-8') as jsonfile:
            json.dump(all_tasks, jsonfile, indent=4)
        console.print(f"[bold green]Tasks exported successfully to {file_name}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error exporting tasks to JSON: {e}[/bold red]")

def export_reminders_to_csv():
    """
    Exports all reminders to a CSV file.
    """
    all_reminders = reminders.get_all_reminders()
    if not all_reminders:
        console.print("[bold yellow]No reminders found to export.[/bold yellow]")
        return

    file_name = questionary.text("Enter the CSV file name for reminders (e.g., reminders.csv):", default="reminders.csv").ask()
    if not file_name:
        console.print("[bold red]File name is required.[/bold red]")
        return

    try:
        with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'message', 'remind_at', 'created_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(all_reminders)
        console.print(f"[bold green]Reminders exported successfully to {file_name}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error exporting reminders to CSV: {e}[/bold red]")

def export_reminders_to_json():
    """
    Exports all reminders to a JSON file.
    """
    all_reminders = reminders.get_all_reminders()
    if not all_reminders:
        console.print("[bold yellow]No reminders found to export.[/bold yellow]")
        return

    file_name = questionary.text("Enter the JSON file name for reminders (e.g., reminders.json):", default="reminders.json").ask()
    if not file_name:
        console.print("[bold red]File name is required.[/bold red]")
        return

    try:
        with open(file_name, 'w', encoding='utf-8') as jsonfile:
            json.dump(all_reminders, jsonfile, indent=4)
        console.print(f"[bold green]Reminders exported successfully to {file_name}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error exporting reminders to JSON: {e}[/bold red]")

if __name__ == '__main__':
    pass
