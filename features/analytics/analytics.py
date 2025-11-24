import questionary
from rich.console import Console
from rich.table import Table
import json
from datetime import datetime, timedelta
from features.tasks import tasks

console = Console()

def get_productivity_analytics():
    """
    This function retrieves productivity analytics data.
    """
    all_tasks = tasks.get_all_tasks()
    if not all_tasks:
        return None

    total_tasks = len(all_tasks)
    completed_tasks = len([task for task in all_tasks if task['status'] == 'Completed'])
    completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    tasks_by_priority = {}
    for task in all_tasks:
        priority = task.get('priority', 'Unknown')
        tasks_by_priority[priority] = tasks_by_priority.get(priority, 0) + 1

    tasks_by_category = {}
    for task in all_tasks:
        category = task.get('category', 'Unknown')
        tasks_by_category[category] = tasks_by_category.get(category, 0) + 1

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "completion_rate": completion_rate,
        "tasks_by_priority": tasks_by_priority,
        "tasks_by_category": tasks_by_category,
    }

def display_productivity_analytics():
    """
    This function displays productivity analytics.
    """
    analytics_data = get_productivity_analytics()
    if not analytics_data:
        console.print("[bold yellow]No tasks found for analytics.[/bold yellow]")
        return

    console.print("\n[bold blue]Productivity Analytics[/bold blue]")
    console.print(f"Total Tasks: {analytics_data['total_tasks']}")
    console.print(f"Completed Tasks: {analytics_data['completed_tasks']}")
    console.print(f"Completion Rate: {analytics_data['completion_rate']:.2f}%")

    table_priority = Table(title="Tasks by Priority")
    table_priority.add_column("Priority", style="cyan")
    table_priority.add_column("Count", style="magenta")
    for priority, count in analytics_data['tasks_by_priority'].items():
        table_priority.add_row(priority, str(count))
    console.print(table_priority)

    table_category = Table(title="Tasks by Category")
    table_category.add_column("Category", style="cyan")
    table_category.add_column("Count", style="magenta")
    for category, count in analytics_data['tasks_by_category'].items():
        table_category.add_row(category, str(count))
    console.print(table_category)

def display_daily_weekly_summaries():
    """
    This function displays daily and weekly summaries of tasks.
    """
    all_tasks = tasks.get_all_tasks()
    if not all_tasks:
        console.print("[bold yellow]No tasks found for summaries.[/bold yellow]")
        return

    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday()) # Monday as start of week

    # Daily Summary
    tasks_completed_today = [task for task in all_tasks if task['status'] == 'Completed' and datetime.strptime(task['created_at'], "%Y-%m-%d").date() == today]
    tasks_due_today = [task for task in all_tasks if task['deadline'] and datetime.strptime(task['deadline'], "%Y-%m-%d").date() == today and task['status'] != 'Completed']

    console.print("\n[bold blue]Daily Summary[/bold blue]")
    console.print(f"Tasks Completed Today: {len(tasks_completed_today)}")
    console.print(f"Tasks Due Today: {len(tasks_due_today)}")

    # Weekly Summary
    tasks_completed_this_week = [task for task in all_tasks if task['status'] == 'Completed' and datetime.strptime(task['created_at'], "%Y-%m-%d").date() >= start_of_week]
    tasks_due_this_week = [task for task in all_tasks if task['deadline'] and datetime.strptime(task['deadline'], "%Y-%m-%d").date() >= start_of_week and task['status'] != 'Completed']

    console.print("\n[bold blue]Weekly Summary[/bold blue]")
    console.print(f"Tasks Completed This Week: {len(tasks_completed_this_week)}")
    console.print(f"Tasks Due This Week: {len(tasks_due_this_week)}")

def display_priority_distribution_chart():
    """
    This function displays an ASCII chart for priority distribution.
    """
    all_tasks = tasks.get_all_tasks()
    if not all_tasks:
        console.print("[bold yellow]No tasks found for priority distribution chart.[/bold yellow]")
        return

    tasks_by_priority = {}
    for task in all_tasks:
        priority = task.get('priority', 'Unknown')
        tasks_by_priority[priority] = tasks_by_priority.get(priority, 0) + 1
    
    total_tasks = len(all_tasks)
    
    console.print("\n[bold blue]Priority Distribution Chart[/bold blue]")
    
    for priority, count in tasks_by_priority.items():
        percentage = (count / total_tasks) * 100
        bar = "█" * int(percentage / 2)
        console.print(f"{priority:<10} | {bar} {percentage:.2f}%")

def display_productivity_score():
    """
    This function calculates and displays a productivity score.
    """
    all_tasks = tasks.get_all_tasks()
    if not all_tasks:
        console.print("[bold yellow]No tasks found to calculate productivity score.[/bold yellow]")
        return

    total_tasks = len(all_tasks)
    completed_tasks = [task for task in all_tasks if task['status'] == 'Completed']
    completion_rate = (len(completed_tasks) / total_tasks) * 100 if total_tasks > 0 else 0

    overdue_tasks = [
        task for task in all_tasks 
        if task['deadline'] and datetime.strptime(task['deadline'], "%Y-%m-%d").date() < datetime.now().date() and task['status'] != 'Completed'
    ]
    overdue_penalty = len(overdue_tasks) * 5 # Penalize 5 points for each overdue task

    # Calculate task freshness (average completion time in days)
    total_completion_days = 0
    for task in completed_tasks:
        created_date = datetime.strptime(task['created_at'], "%Y-%m-%d").date()
        # Assuming 'completed_at' is added when a task is completed. If not, this will need adjustment.
        completed_at_str = task.get('completed_at', task.get('created_at')) # Fallback to created_at
        completed_date = datetime.strptime(completed_at_str, "%Y-%m-%d").date()
        completion_days = (completed_date - created_date).days
        total_completion_days += completion_days
    
    avg_completion_time = (total_completion_days / len(completed_tasks)) if completed_tasks else 0
    
    # Normalize avg_completion_time to a score component (e.g., less time is better)
    freshness_score = max(0, 10 - avg_completion_time) * 2 # Scale to be a significant part of the score

    # Calculate final score
    productivity_score = (completion_rate * 0.5) + freshness_score - overdue_penalty
    productivity_score = max(0, min(100, productivity_score)) # Clamp score between 0 and 100

    console.print("\n[bold blue]Productivity Score[/bold blue]")
    console.print(f"Your productivity score is: [bold green]{productivity_score:.2f}/100[/bold green]")
    
    if productivity_score < 50:
        console.print("[yellow]Keep going, you can improve![/yellow]")
    elif productivity_score < 80:
        console.print("[blue]You are doing great![/blue]")
    else:
        console.print("[green]You are a productivity master![/green]")

if __name__ == '__main__':
    display_priority_distribution_chart()
    display_productivity_score()
