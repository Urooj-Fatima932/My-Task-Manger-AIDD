import json
import os

DATABASE_FILE = os.path.join(os.path.dirname(__file__), '..', 'database', 'tasks.txt')

def _get_next_id(tasks):
    if not tasks:
        return 1
    return max(task.get("id", 0) for task in tasks) + 1

def fix_duplicate_ids():
    """
    Reads tasks from the database file, fixes any duplicate IDs, 
    and writes the corrected data back to the file.
    """
    try:
        with open(DATABASE_FILE, "r") as f:
            tasks = [json.loads(line) for line in f]
    except FileNotFoundError:
        print("No tasks file found. Nothing to fix.")
        return

    print("Checking for duplicate task IDs...")
    
    cleaned_tasks = []
    seen_ids = set()
    duplicates_found = False

    for task in tasks:
        if "id" not in task:
            task["id"] = _get_next_id(cleaned_tasks)
            print(f"Task '{task.get('title', 'Untitled')}' was missing an ID. Assigned new ID: {task['id']}")
            duplicates_found = True

        if task["id"] in seen_ids:
            duplicates_found = True
            old_id = task["id"]
            new_id = _get_next_id(cleaned_tasks)
            task["id"] = new_id
            print(f"Found duplicate ID {old_id}. Assigning new ID: {new_id} to task '{task.get('title', 'Untitled')}'")
        
        cleaned_tasks.append(task)
        seen_ids.add(task["id"])

    if duplicates_found:
        print("\nDuplicates were found and fixed. Writing corrected data back to tasks.txt...")
        with open(DATABASE_FILE, "w") as f:
            for task in cleaned_tasks:
                f.write(json.dumps(task) + "\n")
        print("Successfully fixed duplicate IDs.")
    else:
        print("No duplicate IDs found. Your data is clean!")

if __name__ == "__main__":
    fix_duplicate_ids()
