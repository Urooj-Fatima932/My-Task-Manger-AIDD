# Task Manager CLI

## Project Overview
A complete command-line productivity tool to manage todos, priority tasks, deadlines, reminders, and productivity analytics.

## Core Features
- Add / Edit / Delete Tasks
- Priorities (Low, Medium, High, Critical)
- Deadlines with reminders
- Categories & Tags
- Productivity analytics
- Daily & weekly summaries
- Export to CSV & JSON
- Optional streamlit dashboard

## Tech Stack
- Language: Python 3.11+
- CLI Framework: Questionary
- UI Library: Rich (tables, colors, panels)
- Storage: Text files (no DB)
- Package Manager: UV

## Project Structure
task-manager-cli/
├── main.py
├── database/
│ ├── tasks.txt
│ └── reminders.txt
└── features/
├── tasks/
│ ├── GEMINI.md
│ └── tasks.py
├── analytics/
│ ├── GEMINI.md
│ └── analytics.py
├── reminders/
│ ├── GEMINI.md
│ └── reminders.py
└── categories/
├── GEMINI.md
└── categories.py


## Task Structure (Recommended)
```python
{
    "id": 1,
    "title": "Complete assignment",
    "description": "Finish math chapter 5 exercises",
    "category": "School",
    "priority": "High",
    "status": "Pending",
    "created_at": "2025-11-17",
    "deadline": "2025-11-20",
    "tags": ["Urgent", "Homework"]
}

Priority Levels

Low

Medium

High

Critical 🚨

CLI Philosophy

Use dropdowns, clean tables, colored status labels.

---

# **Day 2 — Task Management System**

Create `features/tasks/GEMINI.md`:

```markdown
# Day 2: Task Management System

## Today's Goal
Build core functionality: adding, listing, editing, and removing tasks.

## Concepts to Learn
- Task structure
- Input validation
- File operations
- Importance of deadlines
- Priority levels

## Features to Build

### 1. Add Task
Flow:
1. Ask task title (required)
2. Ask description
3. Ask category
4. Ask priority (low/medium/high/critical)
5. Ask deadline (optional)
6. Auto-generate created date
7. Save to tasks.txt

### 2. List Tasks
- Rich table display
- Columns: ID, Title, Priority, Category, Deadline, Status
- Color-coding:
  - Green → Completed
  - Yellow → Pending
  - Red → Overdue
- Sort options:
  - By priority
  - By deadline
  - By category
  - By date created

### 3. Edit Task
- Edit fields individually
- Change status (pending → completed)
- Update priority or deadline

### 4. Delete Task
- Ask ID → confirm → remove

### 5. Search & Filters
- Search by title
- Filter by:
  - Category
  - Priority
  - Status (completed/pending)
  - Tags

## Success Criteria
✅ Add tasks  
✅ Edit tasks  
✅ Delete tasks  
✅ List tasks with beautiful UI  
✅ Filtering works  


## Today's Goal
Add organization tools: categories, tags, and grouping.

## Concepts to Learn
- Classification
- Hierarchical grouping
- Searchability

## Features

### Categories
- Create category
- List all categories
- Assign tasks to categories
- Category summary:
  - Number of tasks
  - Completed tasks
  - Pending tasks

### Tags
- Add multiple tags per task
- Filter tasks by tag
- Tag-based insights (most-used tags)

## Success Criteria
✅ Create categories  
✅ Tag support  
✅ Filter by category and tag  
 
 # Day 4: Productivity Analytics Engine

## Today's Goal
Generate insights on productivity patterns.

## Features to Build

### 1. Daily Summary
- Tasks completed today
- Tasks pending
- Overdue tasks

### 2. Weekly Report
- Total tasks created
- Total completed  
- Completion rate  
- Top categories  
- Peak productivity day  

### 3. Priority Distribution
ASCII chart example:
Priority Breakdown:
Low ██████ 20%
Medium ██████████ 40%
High ██████ 20%
Critical ████ 20%

### 4. Overdue Analysis
- Count overdue tasks
- Tasks nearing deadline

### 5. Productivity Score
Score (0–100) based on:
- Completion rate  
- Overdue tasks  
- Task freshness (how quickly tasks are completed)

## Success Criteria
✅ Daily summary  
✅ Weekly analytics  
✅ Charts  

# Day 5: Reminder System

## Features

### 1. Deadline Alerts
- Tasks due today
- Tasks due tomorrow
- Overdue tasks

### 2. Smart Alerts
- Long pending tasks
- Critical tasks due soon
- Newly created tasks with short deadlines

### 3. Suggestion Engine
- If many overdue tasks → suggest time blocking
- If no tasks completed → suggest easier tasks
- If too many critical tasks → suggest re-prioritizing

### Daily Reminder Example

📅 **Daily Task Briefing (Nov 17, 2025)**  
Pending Tasks: 5  
Due Today: 2  
Overdue: 1  
Recommended: "Complete small tasks first to gain momentum."

## Success Criteria
✅ Reminders  
✅ Alerts  
# Day 6: Data Export & Backup

## Features

### 1. Export Tasks
- CSV export
- JSON export
- Filters before export (category/priority/status)

### 2. Backup System
- Timestamped backup
- Store in backups/ folder
- Auto-delete old backups (keep last 10)

### 3. Import Tasks
- Import from CSV
- Validate duplicates
- Summary of imported data

## Success Criteria
✅ CSV export  
✅ JSON export  
✅ Backup  
