import questionary
from rich.console import Console
import csv
from features.tasks import tasks
from features.reminders import reminders

console = Console()

def import_tasks_from_csv():
    """
    Imports tasks from a CSV file, avoiding duplicates.
    """
    file_name = questionary.text("Enter the CSV file name for tasks to import (e.g., tasks.csv):").ask()
    if not file_name:
        console.print("[bold red]File name is required.[/bold red]")
        return

    try:
        with open(file_name, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            all_tasks = tasks.get_all_tasks()
            existing_titles = {task['title'] for task in all_tasks}
            imported_count = 0
            
            for row in reader:
                if row['title'] not in existing_titles:
                    # Convert tags string back to list
                    row['tags'] = row['tags'].split(',') if row['tags'] else []
                    row['id'] = len(all_tasks) + 1
                    all_tasks.append(row)
                    existing_titles.add(row['title'])
                    imported_count += 1
            
            tasks.save_tasks(all_tasks)
            console.print(f"[bold green]Successfully imported {imported_count} new tasks from {file_name}[/bold green]")

    except FileNotFoundError:
        console.print(f"[bold red]File not found: {file_name}[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error importing tasks from CSV: {e}[/bold red]")

def import_reminders_from_csv():
    """
    Imports reminders from a CSV file, avoiding duplicates.
    """
    file_name = questionary.text("Enter the CSV file name for reminders to import (e.g., reminders.csv):").ask()
    if not file_name:
        console.print("[bold red]File name is required.[/bold red]")
        return

    try:
        with open(file_name, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            all_reminders = reminders.get_all_reminders()
            existing_messages = {rem['message'] for rem in all_reminders}
            imported_count = 0

            for row in reader:
                if row['message'] not in existing_messages:
                    row['id'] = len(all_reminders) + 1
                    all_reminders.append(row)
                    existing_messages.add(row['message'])
                    imported_count += 1
            
            reminders.save_reminders(all_reminders)
            console.print(f"[bold green]Successfully imported {imported_count} new reminders from {file_name}[/bold green]")

    except FileNotFoundError:
        console.print(f"[bold red]File not found: {file_name}[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error importing reminders from CSV: {e}[/bold red]")

if __name__ == '__main__':
    pass
