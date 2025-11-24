import json
import questionary
from rich.console import Console
from features.tasks import tasks
from datetime import datetime, timedelta

console = Console()
DATABASE_FILE = "database/reminders.txt"

def get_all_reminders():
    """
    This function retrieves all reminders from the database file.
    
    Returns:
        A list of reminder dictionaries.
    """
    try:
        with open(DATABASE_FILE, "r") as f:
            reminders = [json.loads(line) for line in f]
        return reminders
    except FileNotFoundError:
        return []

def save_reminders(reminders):
    """
    This function saves a list of reminders to the database file.
    
    Args:
        reminders: A list of reminder dictionaries.
    """
    with open(DATABASE_FILE, "w") as f:
        for reminder in reminders:
            f.write(json.dumps(reminder) + "\n")

def add_reminder_data(message, remind_at):
    """
    This function adds a new reminder to the database.
    """
    reminders = get_all_reminders()
    new_reminder = {
        "id": len(reminders) + 1,
        "message": message,
        "remind_at": remind_at.strftime("%Y-%m-%d %H:%M"),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    reminders.append(new_reminder)
    save_reminders(reminders)
    return new_reminder

def add_reminder():
    """
    This function prompts the user for reminder details and adds the reminder to the database.
    """
    message = questionary.text("What is the reminder message?").ask()
    if not message:
        console.print("[bold red]Reminder message is required.[/bold red]")
        return

    reminder_datetime_str = questionary.text("When should the reminder be (YYYY-MM-DD HH:MM)?").ask()
    
    reminder_datetime = None
    if reminder_datetime_str:
        try:
            reminder_datetime = datetime.strptime(reminder_datetime_str, "%Y-%m-%d %H:%M")
        except ValueError:
            console.print("[bold red]Invalid datetime format. Please use YYYY-MM-DD HH:MM.[/bold red]")
            return
    else:
        console.print("[bold red]Reminder datetime is required.[/bold red]")
        return
    
    add_reminder_data(message, reminder_datetime)
    console.print(f"[bold green]Reminder '{message}' added successfully![/bold green]")

def list_reminders():
    """
    This function lists all reminders in a table.
    """
    reminders = get_all_reminders()
    if not reminders:
        console.print("[bold yellow]No reminders found.[/bold yellow]")
        return

    table = Table(title="Reminders")
    table.add_column("ID", style="cyan")
    table.add_column("Message", style="magenta")
    table.add_column("Remind At", style="yellow")
    table.add_column("Created At", style="blue")

    for reminder in reminders:
        table.add_row(
            str(reminder["id"]),
            reminder["message"],
            reminder["remind_at"],
            reminder["created_at"],
        )

    console.print(table)

def edit_reminder_data(reminder_id, message, remind_at):
    """
    This function edits an existing reminder's data.
    """
    reminders = get_all_reminders()
    reminder_to_edit = None
    for reminder in reminders:
        if reminder["id"] == reminder_id:
            reminder_to_edit = reminder
            break
    
    if not reminder_to_edit:
        return None

    reminder_to_edit["message"] = message
    reminder_to_edit["remind_at"] = remind_at.strftime("%Y-%m-%d %H:%M")
    save_reminders(reminders)
    return reminder_to_edit

def edit_reminder():
    """
    This function edits an existing reminder.
    """
    reminders = get_all_reminders()
    if not reminders:
        console.print("[bold yellow]No reminders to edit.[/bold yellow]")
        return

    list_reminders()
    reminder_id_str = questionary.text("Enter the ID of the reminder you want to edit:").ask()

    if not reminder_id_str or not reminder_id_str.isdigit():
        console.print("[bold red]Invalid ID.[/bold red]")
        return

    reminder_id = int(reminder_id_str)
    reminder_to_edit = None
    for reminder in reminders:
        if reminder["id"] == reminder_id:
            reminder_to_edit = reminder
            break

    if not reminder_to_edit:
        console.print("[bold red]Reminder not found.[/bold red]")
        return

    message = questionary.text(f"What is the new message for the reminder (current: {reminder_to_edit['message']})?", default=reminder_to_edit['message']).ask()
    reminder_datetime_str = questionary.text(f"When should the reminder be (YYYY-MM-DD HH:MM) (current: {reminder_to_edit['remind_at']})?", default=reminder_to_edit['remind_at']).ask()

    reminder_datetime = None
    if reminder_datetime_str:
        try:
            reminder_datetime = datetime.strptime(reminder_datetime_str, "%Y-%m-%d %H:%M")
        except ValueError:
            console.print("[bold red]Invalid datetime format. Please use YYYY-MM-DD HH:MM.[/bold red]")
            return
    else:
        console.print("[bold red]Reminder datetime is required.[/bold red]")
        return
    
    edit_reminder_data(reminder_id, message, reminder_datetime)
    console.print(f"[bold green]Reminder '{message}' updated successfully![/bold green]")

def delete_reminder_data(reminder_id):
    """
    This function deletes a reminder by its ID.
    """
    reminders = get_all_reminders()
    reminder_to_delete = None
    for reminder in reminders:
        if reminder["id"] == reminder_id:
            reminder_to_delete = reminder
            break
    
    if not reminder_to_delete:
        return False
    
    reminders.remove(reminder_to_delete)
    save_reminders(reminders)
    return True

def delete_reminder():
    """
    This function deletes a reminder.
    """
    reminders = get_all_reminders()
    if not reminders:
        console.print("[bold yellow]No reminders to delete.[/bold yellow]")
        return

    list_reminders()
    reminder_id_str = questionary.text("Enter the ID of the reminder you want to delete:").ask()

    if not reminder_id_str or not reminder_id_str.isdigit():
        console.print("[bold red]Invalid ID.[/bold red]")
        return

    reminder_id = int(reminder_id_str)
    reminder_to_delete = None
    for reminder in reminders:
        if reminder["id"] == reminder_id:
            reminder_to_delete = reminder
            break

    if not reminder_to_delete:
        console.print("[bold red]Reminder not found.[/bold red]")
        return

    confirm = questionary.confirm(f"Are you sure you want to delete reminder '{reminder_to_delete['message']}'?").ask()

    if confirm:
        if delete_reminder_data(reminder_id):
            console.print(f"[bold green]Reminder '{reminder_to_delete['message']}' deleted successfully![/bold green]")
        else:
            console.print(f"[bold red]Failed to delete reminder '{reminder_to_delete['message']}'.[/bold red]")

def display_smart_alerts():
    """
    This function displays smart alerts for tasks.
    """
    all_tasks = tasks.get_all_tasks()
    if not all_tasks:
        console.print("[bold yellow]No tasks found for smart alerts.[/bold yellow]")
        return

    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    console.print("\n[bold blue]Smart Alerts[/bold blue]")

    # Deadline Alerts
    due_today = [task for task in all_tasks if task['deadline'] and datetime.strptime(task['deadline'], "%Y-%m-%d").date() == today and task['status'] != 'Completed']
    due_tomorrow = [task for task in all_tasks if task['deadline'] and datetime.strptime(task['deadline'], "%Y-%m-%d").date() == tomorrow and task['status'] != 'Completed']
    overdue = [task for task in all_tasks if task['deadline'] and datetime.strptime(task['deadline'], "%Y-%m-%d").date() < today and task['status'] != 'Completed']

    if due_today:
        console.print(f"[bold yellow]Tasks Due Today ({len(due_today)}):[/bold yellow]")
        for task in due_today:
            console.print(f"- {task['title']}")
            
    if due_tomorrow:
        console.print(f"[bold yellow]Tasks Due Tomorrow ({len(due_tomorrow)}):[/bold yellow]")
        for task in due_tomorrow:
            console.print(f"- {task['title']}")

    if overdue:
        console.print(f"[bold red]Overdue Tasks ({len(overdue)}):[/bold red]")
        for task in overdue:
            console.print(f"- {task['title']}")

    # Other Smart Alerts
    long_pending_tasks = [task for task in all_tasks if task['status'] == 'Pending' and (today - datetime.strptime(task['created_at'], "%Y-%m-%d").date()).days > 7]
    critical_due_soon = [task for task in all_tasks if task['priority'] == 'Critical' and task['deadline'] and (datetime.strptime(task['deadline'], "%Y-%m-%d").date() - today).days <= 3 and task['status'] != 'Completed']

    if long_pending_tasks:
        console.print(f"[bold magenta]Long Pending Tasks (>7 days) ({len(long_pending_tasks)}):[/bold magenta]")
        for task in long_pending_tasks:
            console.print(f"- {task['title']}")

    if critical_due_soon:
        console.print(f"[bold red]Critical Tasks Due Soon ({len(critical_due_soon)}):[/bold red]")
        for task in critical_due_soon:
            console.print(f"- {task['title']}")

def display_suggestion_engine():
    """
    This function provides suggestions based on the user's tasks.
    """
    all_tasks = tasks.get_all_tasks()
    if not all_tasks:
        console.print("[bold yellow]No tasks found to generate suggestions.[/bold yellow]")
        return

    today = datetime.now().date()
    overdue_tasks = [task for task in all_tasks if task['deadline'] and datetime.strptime(task['deadline'], "%Y-%m-%d").date() < today and task['status'] != 'Completed']
    completed_today = [task for task in all_tasks if task.get('completed_at') and datetime.strptime(task['completed_at'], "%Y-%m-%d").date() == today]
    critical_tasks = [task for task in all_tasks if task['priority'] == 'Critical' and task['status'] != 'Completed']

    console.print("\n[bold blue]Suggestion Engine[/bold blue]")

    if len(overdue_tasks) > 3:
        console.print("[bold yellow]Suggestion:[/bold yellow] You have several overdue tasks. Consider using time blocking to focus on them.")
    
    if not completed_today and any(task['status'] == 'Pending' for task in all_tasks):
        console.print("[bold yellow]Suggestion:[/bold yellow] No tasks completed today. Try tackling a small, easy task to gain momentum.")

    if len(critical_tasks) > 5:
        console.print("[bold yellow]Suggestion:[/bold yellow] You have a high number of critical tasks. It might be helpful to re-prioritize them.")

    if not any([len(overdue_tasks) > 3, not completed_today and any(task['status'] == 'Pending' for task in all_tasks), len(critical_tasks) > 5]):
        console.print("[bold green]You are doing great! Keep up the good work.[/bold green]")

if __name__ == '__main__':
    display_smart_alerts()
    display_suggestion_engine()
