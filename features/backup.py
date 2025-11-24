import os
import zipfile
from datetime import datetime
from rich.console import Console

console = Console()
BACKUP_DIR = "backups"
FILES_TO_BACKUP = ["database/tasks.txt", "database/reminders.txt", "database/categories.txt"]
MAX_BACKUPS = 10

def create_backup():
    """
    Creates a timestamped backup of the database files and manages old backups.
    """
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = os.path.join(BACKUP_DIR, f"backup_{timestamp}.zip")

    try:
        with zipfile.ZipFile(backup_filename, 'w') as zf:
            for file in FILES_TO_BACKUP:
                if os.path.exists(file):
                    zf.write(file, os.path.basename(file))
        
        console.print(f"[bold green]Backup created successfully: {backup_filename}[/bold green]")
        
        # Auto-delete old backups
        backups = sorted(os.listdir(BACKUP_DIR), key=lambda f: os.path.getmtime(os.path.join(BACKUP_DIR, f)))
        if len(backups) > MAX_BACKUPS:
            for old_backup in backups[:len(backups) - MAX_BACKUPS]:
                os.remove(os.path.join(BACKUP_DIR, old_backup))
                console.print(f"[yellow]Deleted old backup: {old_backup}[/yellow]")

    except Exception as e:
        console.print(f"[bold red]Error creating backup: {e}[/bold red]")

if __name__ == '__main__':
    create_backup()
