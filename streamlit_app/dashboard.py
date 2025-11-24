import streamlit as st
import altair as alt
import pandas as pd
from datetime import datetime
from features.tasks import tasks as tasks_manager
from features.reminders import reminders as reminders_manager
from features.categories import categories as categories_manager
from features.analytics import analytics
from streamlit_app.time_helper import get_total_time_spent
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

import uuid

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

            is_recurring = st.checkbox("Is this a recurring task?")
            recurrence_rule = None
            if is_recurring:
                recurrence_rule = st.selectbox("Recurrence", ["daily", "weekly", "monthly"])

            submitted = st.form_submit_button("Add Task")
            if submitted:
                tags_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
                tasks_manager.add_task_data(
                    title, description, category, priority, deadline, tags_list, 
                    is_recurring, recurrence_rule
                )
                st.success(f"Task '{title}' added!")
                st.rerun()

    st.subheader("📝 Task Board")
    
    all_tasks = tasks_manager.get_all_tasks()
    
    # Define Kanban columns
    statuses = ["Pending", "In Progress", "Completed"]
    kanban_cols = st.columns(len(statuses))

    # Group tasks by status
    tasks_by_status = {status: [] for status in statuses}
    for task in all_tasks:
        if task['status'] not in statuses:
            task['status'] = "Pending"
        tasks_by_status[task['status']].append(task)
        
    for i, status in enumerate(statuses):
        with kanban_cols[i]:
            st.markdown(f"**{status}** ({len(tasks_by_status[status])})")
            st.markdown("---")
            for task in sorted(tasks_by_status[status], key=lambda x: x['id'], reverse=True):
                with st.container(border=True):
                    st.markdown(f"**{task['title']}**")
                    
                    # Quick status change buttons
                    col1_status, col2_status, col3_status = st.columns(3)
                    if status == "Pending":
                        with col1_status:
                            if st.button("▶️", key=f"start_{task['id']}"):
                                tasks_manager.edit_task_data(task['id'], task['title'], task['description'], task['category'], task['priority'], task['deadline'], "In Progress", task['tags'], task.get('is_recurring'), task.get('recurrence_rule'))
                                st.rerun()
                    elif status == "In Progress":
                        with col1_status:
                            if st.button("↩️", key=f"back_{task['id']}"):
                                tasks_manager.edit_task_data(task['id'], task['title'], task['description'], task['category'], task['priority'], task['deadline'], "Pending", task['tags'], task.get('is_recurring'), task.get('recurrence_rule'))
                                st.rerun()
                        with col2_status:
                            if st.button("✔", key=f"complete_{task['id']}"):
                                tasks_manager.edit_task_data(task['id'], task['title'], task['description'], task['category'], task['priority'], task['deadline'], "Completed", task['tags'], task.get('is_recurring'), task.get('recurrence_rule'))
                                st.rerun()
                    elif status == "Completed":
                        with col1_status:
                            if st.button("🔄", key=f"reopen_{task['id']}"):
                                tasks_manager.edit_task_data(task['id'], task['title'], task['description'], task['category'], task['priority'], task['deadline'], "Pending", task['tags'], task.get('is_recurring'), task.get('recurrence_rule'))
                                st.rerun()

                    # Add delete button here
                    with col3_status:
                        if st.button("❌", key=f"delete_btn_quick_{task['id']}"):
                            tasks_manager.delete_task_data(task['id'])
                            st.warning(f"Task ID '{task['id']}' deleted!")
                            st.rerun()


                    st.write(f"Priority: {task['priority']}")
                    if task['deadline']:
                        st.write(f"Deadline: {task['deadline']}")
                    
                    time_spent = get_total_time_spent(task.get("time_entries", []))
                    st.write(f"**Time Spent:** {time_spent}")

                    if task.get("is_tracking", False):
                        if st.button("⏹️ Stop Tracking", key=f"stop_track_{task['id']}"):
                            tasks_manager.stop_time_tracking(task['id'])
                            st.rerun()
                    else:
                        if st.button("▶️ Start Tracking", key=f"start_track_{task['id']}"):
                            tasks_manager.start_time_tracking(task['id'])
                            st.rerun()

                    with st.expander("Details & Actions"):
                        st.write(f"Description: {task['description']}")
                        st.write(f"Category: {task['category']}")
                        st.write(f"Tags: {', '.join(task['tags'])}")

                        if st.button("✏️ Edit Task", key=f"edit_btn_{task['id']}"):
                            st.session_state[f"edit_mode_{task['id']}"] = True

                        if st.session_state.get(f"edit_mode_{task['id']}", False):
                            with st.form(f"edit_task_{task['id']}"):
                                new_title = st.text_input("Title", value=task['title'], key=f"edit_title_{task['id']}")
                                new_description = st.text_area("Description", value=task['description'], key=f"edit_desc_{task['id']}")
                                new_category = st.selectbox("Category", [task['category']] + [cat['name'] for cat in categories_manager.get_all_categories() if cat['name'] != task['category']], key=f"edit_cat_{task['id']}")
                                new_priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"], index=["Low", "Medium", "High", "Critical"].index(task['priority']), key=f"edit_prio_{task['id']}")
                                new_deadline_val = None
                                if task['deadline']:
                                    new_deadline_val = datetime.strptime(task['deadline'], "%Y-%m-%d").date()
                                new_deadline = st.date_input("Deadline", value=new_deadline_val, key=f"edit_ddl_{task['id']}")
                                new_status = st.selectbox("Status", statuses, index=statuses.index(task['status']), key=f"edit_stat_{task['id']}")
                                new_tags = st.text_input("Tags", value=", ".join(task['tags']), key=f"edit_tags_{task['id']}")
                                
                                new_is_recurring = st.checkbox("Is this a recurring task?", value=task.get("is_recurring", False), key=f"edit_is_recurring_{task['id']}")
                                new_recurrence_rule = None
                                if new_is_recurring:
                                    recurrence_options = ["daily", "weekly", "monthly"]
                                    recurrence_index = recurrence_options.index(task.get("recurrence_rule", "daily"))
                                    new_recurrence_rule = st.selectbox("Recurrence", recurrence_options, index=recurrence_index, key=f"edit_recurrence_{task['id']}")

                                col1_edit, col2_edit = st.columns(2)
                                with col1_edit:
                                    if st.form_submit_button("Update Task", key=f"update_btn_{task['id']}"):
                                        new_tags_list = [tag.strip() for tag in new_tags.split(',') if tag.strip()]
                                        tasks_manager.edit_task_data(
                                            task['id'], new_title, new_description, new_category, new_priority, 
                                            new_deadline, new_status, new_tags_list,
                                            new_is_recurring, new_recurrence_rule
                                        )
                                        st.session_state[f"edit_mode_{task['id']}"] = False
                                        st.success(f"Task '{new_title}' updated!")
                                        st.rerun()

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

import altair as alt

def display_analytics():
    st.subheader("Basic Analytics")
    analytics_data = analytics.get_productivity_analytics()
    
    if not analytics_data:
        st.info("No tasks found for analytics.")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Tasks", value=analytics_data['total_tasks'])
    col2.metric(label="Completed Tasks", value=analytics_data['completed_tasks'])
    col3.metric(label="Completion Rate", value=f"{analytics_data['completion_rate']:.2f}%")

    st.subheader("Task Distribution")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### By Priority")
        priority_df = pd.DataFrame(list(analytics_data['tasks_by_priority'].items()), columns=['Priority', 'Count'])
        
        priority_chart = alt.Chart(priority_df).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Count", type="quantitative"),
            color=alt.Color(field="Priority", type="nominal", title="Priority"),
            tooltip=['Priority', 'Count']
        ).properties(
            title='Task Distribution by Priority'
        )
        st.altair_chart(priority_chart, use_container_width=True)

    with col2:
        st.markdown("##### By Category")
        category_df = pd.DataFrame(list(analytics_data['tasks_by_category'].items()), columns=['Category', 'Count'])
        
        category_chart = alt.Chart(category_df).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Count", type="quantitative"),
            color=alt.Color(field="Category", type="nominal", title="Category"),
            tooltip=['Category', 'Count']
        ).properties(
            title='Task Distribution by Category'
        )
        st.altair_chart(category_chart, use_container_width=True)
    
    st.subheader("Advanced Time Analytics")
    advanced_analytics_data = analytics.get_advanced_analytics()
    if not advanced_analytics_data:
        st.info("No time tracking data available for advanced analytics.")
        return
        
    st.markdown("##### Time Spent per Category (hours)")
    time_cat_df = pd.DataFrame(list(advanced_analytics_data['time_by_category'].items()), columns=['Category', 'Hours'])
    time_cat_chart = alt.Chart(time_cat_df).mark_bar().encode(
        x=alt.X('Category', sort=None),
        y='Hours',
        tooltip=['Category', 'Hours']
    ).properties(
        title="Time Spent per Category"
    )
    st.altair_chart(time_cat_chart, use_container_width=True)

    st.markdown("##### Time Spent per Priority (hours)")
    time_prio_df = pd.DataFrame(list(advanced_analytics_data['time_by_priority'].items()), columns=['Priority', 'Hours'])
    time_prio_chart = alt.Chart(time_prio_df).mark_bar().encode(
        x=alt.X('Priority', sort=None),
        y='Hours',
        color='Priority',
        tooltip=['Priority', 'Hours']
    ).properties(
        title="Time Spent per Priority"
    )
    st.altair_chart(time_prio_chart, use_container_width=True)
    
    st.subheader("Productivity Trends")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### By Day of Week")
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        day_df = pd.DataFrame({
            'Day': days,
            'Tasks Completed': [advanced_analytics_data['tasks_completed_by_day'][i] for i in range(7)]
        })
        day_chart = alt.Chart(day_df).mark_line(point=True).encode(
            x=alt.X('Day', sort=days),
            y='Tasks Completed',
            tooltip=['Day', 'Tasks Completed']
        ).properties(
            title="Weekly Productivity Trend"
        )
        st.altair_chart(day_chart, use_container_width=True)

    with col2:
        st.markdown("##### By Hour of Day")
        hour_df = pd.DataFrame({
            'Hour': range(24),
            'Tasks Completed': [advanced_analytics_data['tasks_completed_by_hour'][i] for i in range(24)]
        })
        hour_chart = alt.Chart(hour_df).mark_line(point=True).encode(
            x='Hour',
            y='Tasks Completed',
            tooltip=['Hour', 'Tasks Completed']
        ).properties(
            title="Daily Productivity Trend"
        )
        st.altair_chart(hour_chart, use_container_width=True)

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
