# Task Manager App

A Streamlit-based task manager with secure user authentication for organizing tasks, reminders, and categories, complete with productivity analytics and data export. Created by Gemini CLI.

## ✨ Features

*   **User Authentication:** Secure signup, login, and logout system to protect user data.
*   **Task Management:**
    *   Add, edit, and delete tasks.
    *   Set priorities (Low, Medium, High, Critical) and deadlines.
    *   Assign categories and tags to tasks.
    *   Track task status (Pending, Completed).
*   **Reminder System:**
    *   Create and manage reminders with specific dates and times.
    *   Associate reminders with tasks.
*   **Category & Tagging:**
    *   Organize tasks using custom categories and multiple tags.
    *   View category summaries.
*   **Productivity Analytics:**
    *   Visualize total tasks, completed tasks, and completion rates.
    *   Breakdown tasks by priority and category.
*   **Data Export:** Export tasks and reminders to CSV and JSON formats.
*   **Intuitive UI:** A clean, responsive, and easy-to-use graphical interface powered by Streamlit, featuring collapsible sections and card-based displays.

## 🚀 Tech Stack

*   **Language:** Python 3.11+
*   **Web Framework:** Streamlit
*   **Data Handling:** Pandas
*   **Authentication:** `bcrypt` for secure password hashing
*   **CLI (Legacy/Internal):** `questionary`, `rich` (some core logic may still utilize rich for console output where applicable, but the primary UI is Streamlit)
*   **Package Manager:** UV

## 📂 Project Structure

```
task-manager-cli/
├── main.py                     # Entry point for launching the Streamlit app
├── pyproject.toml              # Project dependencies and metadata
├── README.md                   # This file
├── database/                   # Stores application data (tasks, reminders, categories, users)
│   ├── categories.txt
│   ├── reminders.txt
│   ├── tasks.txt
│   └── users.txt               # User credentials (hashed passwords)
├── features/                   # Core logic for different functionalities
│   ├── __init__.py             # Makes 'features' a Python package
│   ├── analytics/
│   │   ├── analytics.py        # Productivity analytics logic
│   │   └── GEMINI.md
│   ├── auth/
│   │   ├── auth.py             # User authentication (login, signup, hashing)
│   │   └── GEMINI.md           # Documentation for the authentication system
│   ├── categories/
│   │   ├── categories.py       # Category management logic
│   │   └── GEMINI.md
│   ├── export/
│   │   └── export.py           # Data export logic
│   ├── reminders/
│   │   ├── reminders.py        # Reminder management logic
│   │   └── GEMINI.md
│   └── tasks/
│       ├── tasks.py            # Task management logic
│       └── GEMINI.md
└── streamlit_app/
    └── dashboard.py            # The main Streamlit application UI
```

## ⚙️ Getting Started

### Prerequisites

*   Python 3.11 or higher
*   UV package manager (recommended for speed) - `pip install uv`

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/task-manager-app.git
    cd task-manager-app
    ```

2.  **Install dependencies:**
    Ensure you have `uv` installed (`pip install uv`). Then, install the project in editable mode to include all dependencies:

    ```bash
    uv pip install -e .
    ```

### Running the Application

Once the dependencies are installed, you can launch the Streamlit application:

```bash
python main.py
```

This will start the Streamlit server, and your web browser should automatically open to the application's interface (usually `http://localhost:8501`).

## 👨‍💻 Usage

1.  **Sign Up:**
    *   When you first run the app, you'll be presented with a login/signup page.
    *   Expand the "Sign Up" section, enter a unique username and a strong password, and click "Sign Up."
    *   You'll receive a success message if the account is created.

2.  **Login:**
    *   Use your newly created username and password in the "Login" section.
    *   Upon successful login, you'll be redirected to the main Task Manager dashboard.

3.  **Navigate:**
    *   Use the sidebar menu to switch between "Tasks," "Reminders," "Categories," "Analytics," and "Export" sections.

4.  **Manage Tasks:**
    *   In the "Tasks" section, use the "➕ Add New Task" expander to add new tasks.
    *   Your tasks will be displayed as cards. Expand "Details & Actions" for each task to view more details, or to access the edit and delete forms.

5.  **Manage Reminders:**
    *   In the "Reminders" section, add new reminders using the "➕ Add New Reminder" expander.
    *   Delete reminders directly from their cards.

6.  **Manage Categories:**
    *   Create new categories in the "Categories" section using the "➕ Add New Category" expander.
    *   View all categories and a summary of tasks per category.

7.  **View Analytics:**
    *   The "Analytics" section provides insights into your task completion rates and distribution by priority and category.

8.  **Export Data:**
    *   In the "Export" section, you can download your tasks and reminders as CSV or JSON files.

9.  **Logout:**
    *   Click the "Logout" button in the top right corner of the main app to end your session.


