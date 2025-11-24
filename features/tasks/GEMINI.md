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
