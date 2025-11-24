
from datetime import datetime, timedelta

def get_total_time_spent(time_entries):
    total_seconds = 0
    for entry in time_entries:
        start = datetime.fromisoformat(entry["start_time"])
        end = datetime.fromisoformat(entry["end_time"]) if entry["end_time"] else datetime.now()
        total_seconds += (end - start).total_seconds()
    
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    return f"{hours}h {minutes}m {seconds}s"
