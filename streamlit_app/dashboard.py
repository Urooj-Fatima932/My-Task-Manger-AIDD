import streamlit as st
import pandas as pd
from datetime import datetime
from features.tasks import tasks as tasks_manager
from features.reminders import reminders as reminders_manager
from features.categories import categories as categories_manager
from features.analytics import analytics
from features.export import export
from features import auth

st.set_page_config(layout="wide", page_title="Task Manager", page_icon="✅")

def show_login_page():
    st.title("Login / Sign Up")

    with st.expander("Login", expanded=True):
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_submitted = st.form_submit_button("Login")

            if login_submitted:
                if auth.authenticate_user(username, password):
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

    with st.expander("Sign Up", expanded=False):
        with st.form("signup_form"):
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            signup_submitted = st.form_submit_button("Sign Up")

            if signup_submitted:
                if auth.user_exists(new_username):
                    st.error("Username already taken. Please choose a different one.")
                else:
                    if auth.register_user(new_username, new_password):
                        st.success("Account created successfully! Please log in.")
                    else:
                        st.error("Failed to create account.")

def show_main_app():
    st.title(f"✅ Task Manager - Welcome, {st.session_state['username']}!")
    
    col1, col2, col3 = st.columns([0.8, 0.1, 0.1])
    with col3:
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            st.rerun()

    st.sidebar.title("Navigation")
    
    menu = ["✍️ Tasks", "⏰ Reminders", "📂 Categories", "📊 Analytics", "📤 Export"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "✍️ Tasks":
        st.header("Task Management")
        display_tasks()
    elif choice == "⏰ Reminders":
        st.header("Reminder Management")
        display_reminders()
    elif choice == "📂 Categories":
        st.header("Category Management")
        display_categories_and_summary()
    elif choice == "📊 Analytics":
        st.header("Productivity Analytics")
        display_analytics()
    elif choice == "📤 Export":
        st.header("Export Data")
        display_export_options()

def display_tasks():
    with st.expander("➕ Add New Task", expanded=False):
        with st.form("add_task_form", clear_on_submit=True):
            title = st.text_input("Title")
            description = st.text_area("Description")
            
            categories = [cat['name'] for cat in categories_manager.get_all_categories()]
            category = st.selectbox("Category", [""] + categories)

            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            deadline = st.date_input("Deadline", value=None)
            tags = st.text_input("Tags (comma-separated)")

            submitted = st.form_submit_button("Add Task")
            if submitted:
                tags_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
                tasks_manager.add_task_data(title, description, category, priority, deadline, tags_list)
                st.success(f"Task '{title}' added!")
                st.rerun()

    st.subheader("📝 Your Tasks")
    all_tasks = tasks_manager.get_all_tasks()
    if all_tasks:
        for task in sorted(all_tasks, key=lambda x: x['id'], reverse=True):
            with st.container(border=True): # Use border for visual separation
                st.markdown(f"### {task['title']}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Priority:** {task['priority']}")
                with col2:
                    st.write(f"**Status:** {task['status']}")
                with col3:
                    st.write(f"**Deadline:** {task['deadline']}")

                with st.expander("Details & Actions"):
                    st.write(f"**Description:** {task['description']}")
                    st.write(f"**Category:** {task['category']}")
                    st.write(f"**Tags:** {', '.join(task['tags'])}")
                    
                    st.subheader("Edit Task")
                    with st.form(f"edit_task_{task['id']}"):
                        new_title = st.text_input("Title", value=task['title'], key=f"edit_title_{task['id']}")
                        new_description = st.text_area("Description", value=task['description'], key=f"edit_desc_{task['id']}")
                        new_category = st.selectbox("Category", [task['category']] + [cat['name'] for cat in categories_manager.get_all_categories() if cat['name'] != task['category']], key=f"edit_cat_{task['id']}")
                        new_priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"], index=["Low", "Medium", "High", "Critical"].index(task['priority']), key=f"edit_prio_{task['id']}")
                        new_deadline_val = None
                        if task['deadline']:
                            new_deadline_val = datetime.strptime(task['deadline'], "%Y-%m-%d").date()
                        new_deadline = st.date_input("Deadline", value=new_deadline_val, key=f"edit_ddl_{task['id']}")
                        new_status = st.selectbox("Status", ["Pending", "Completed"], index=["Pending", "Completed"].index(task['status']), key=f"edit_stat_{task['id']}")
                        new_tags = st.text_input("Tags", value=", ".join(task['tags']), key=f"edit_tags_{task['id']}")
                        
                        col1_edit, col2_edit = st.columns(2)
                        with col1_edit:
                            if st.form_submit_button("Update Task", key=f"update_btn_{task['id']}"):
                                new_tags_list = [tag.strip() for tag in new_tags.split(',') if tag.strip()]
                                tasks_manager.edit_task_data(task['id'], new_title, new_description, new_category, new_priority, new_deadline, new_status, new_tags_list)
                                st.success(f"Task '{new_title}' updated!")
                                st.rerun()
                        with col2_edit:
                            if st.form_submit_button("Delete Task", key=f"delete_btn_{task['id']}"):
                                tasks_manager.delete_task_data(task['id'])
                                st.warning(f"Task ID '{task['id']}' deleted!")
                                st.rerun()

                st.markdown("---")
    else:
        st.info("No tasks yet. Add one above!")

def display_reminders():
    with st.expander("➕ Add New Reminder", expanded=False):
        with st.form("add_reminder_form", clear_on_submit=True):
            message = st.text_input("Reminder Message")
            reminder_date = st.date_input("Reminder Date", value=datetime.now().date())
            reminder_time = st.time_input("Reminder Time", value=datetime.now().time())

            submitted = st.form_submit_button("Add Reminder")
            if submitted:
                remind_at = datetime.combine(reminder_date, reminder_time)
                reminders_manager.add_reminder_data(message, remind_at)
                st.success(f"Reminder '{message}' added!")
                st.rerun()

    st.subheader("🔔 Your Reminders")
    all_reminders = reminders_manager.get_all_reminders()
    if all_reminders:
        for reminder in sorted(all_reminders, key=lambda x: x['id'], reverse=True):
            with st.container(border=True): # Use border for visual separation
                st.markdown(f"### {reminder['message']}")
                st.write(f"**Remind At:** {reminder['remind_at']}")
                
                col1_del, col2_del = st.columns(2)
                with col1_del:
                    if st.button(f"Delete Reminder {reminder['id']}", key=f"del_rem_{reminder['id']}"):
                        reminders_manager.delete_reminder_data(reminder['id'])
                        st.warning(f"Reminder ID '{reminder['id']}' deleted!")
                        st.rerun()
                st.markdown("---")
    else:
        st.info("No reminders yet.")

def display_categories_and_summary():
    with st.expander("➕ Add New Category", expanded=False):
        with st.form("add_category_form", clear_on_submit=True):
            name = st.text_input("Category Name")
            submitted = st.form_submit_button("Add Category")
            if submitted:
                new_cat, msg = categories_manager.create_category_data(name)
                if new_cat:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
    
    st.subheader("🗂️ All Categories")
    all_categories = categories_manager.get_all_categories()
    if all_categories:
        df = pd.DataFrame(all_categories)
        st.dataframe(df, use_container_width=True)
        
        st.subheader("Category Summary")
        all_tasks = tasks_manager.get_all_tasks()
        category_summary_data = []
        for cat in all_categories:
            category_tasks = [task for task in all_tasks if task['category'] == cat['name']]
            total_tasks = len(category_tasks)
            completed_tasks = len([task for task in category_tasks if task['status'] == 'Completed'])
            pending_tasks = total_tasks - completed_tasks
            category_summary_data.append({
                "Category": cat['name'],
                "Total Tasks": total_tasks,
                "Completed Tasks": completed_tasks,
                "Pending Tasks": pending_tasks
            })
        if category_summary_data:
            df_summary = pd.DataFrame(category_summary_data)
            st.dataframe(df_summary, use_container_width=True)
    else:
        st.info("No categories yet.")

def display_analytics():
    analytics_data = analytics.get_productivity_analytics()
    if not analytics_data:
        st.info("No tasks found for analytics.")
        return

    st.metric(label="Total Tasks", value=analytics_data['total_tasks'])
    st.metric(label="Completed Tasks", value=analytics_data['completed_tasks'])
    st.metric(label="Completion Rate", value=f"{analytics_data['completion_rate']:.2f}%")

    st.subheader("Tasks by Priority")
    priority_df = pd.DataFrame(list(analytics_data['tasks_by_priority'].items()), columns=['Priority', 'Count'])
    st.bar_chart(priority_df.set_index('Priority'))

    st.subheader("Tasks by Category")
    category_df = pd.DataFrame(list(analytics_data['tasks_by_category'].items()), columns=['Category', 'Count'])
    st.bar_chart(category_df.set_index('Category'))

def display_export_options():
    st.subheader("Export Tasks")
    if st.button("Export Tasks to CSV"):
        all_tasks = tasks_manager.get_all_tasks()
        if all_tasks:
            csv_data = pd.DataFrame(all_tasks).to_csv(index=False)
            st.download_button(
                label="Download Tasks CSV",
                data=csv_data,
                file_name="tasks.csv",
                mime="text/csv",
            )
    if st.button("Export Tasks to JSON"):
        all_tasks = tasks_manager.get_all_tasks()
        if all_tasks:
            json_data = pd.DataFrame(all_tasks).to_json(orient="records", indent=4)
            st.download_button(
                label="Download Tasks JSON",
                data=json_data,
                file_name="tasks.json",
                mime="application/json",
            )

    st.subheader("Export Reminders")
    if st.button("Export Reminders to CSV"):
        all_reminders = reminders_manager.get_all_reminders()
        if all_reminders:
            csv_data = pd.DataFrame(all_reminders).to_csv(index=False)
            st.download_button(
                label="Download Reminders CSV",
                data=csv_data,
                file_name="reminders.csv",
                mime="text/csv",
            )
    if st.button("Export Reminders to JSON"):
        all_reminders = reminders_manager.get_all_reminders()
        if all_reminders:
            json_data = pd.DataFrame(all_reminders).to_json(orient="records", indent=4)
            st.download_button(
                label="Download Reminders JSON",
                data=json_data,
                file_name="reminders.json",
                mime="application/json",
            )

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = None

    if st.session_state['logged_in']:
        show_main_app()
    else:
        show_login_page()

if __name__ == "__main__":
    main()
