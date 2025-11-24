# Day X: User Authentication System

## Today's Goal
Implement a robust user authentication system (signup, login, logout) for the Streamlit Task Manager.

## Concepts Learned
-   **User Credential Management:** Secure storage and retrieval of user data.
-   **Password Hashing:** Using `bcrypt` for secure, one-way password encryption to protect user privacy.
-   **Session Management:** Utilizing Streamlit's `st.session_state` to maintain user login status across interactions.
-   **Conditional UI Rendering:** Dynamically displaying login/signup forms or application content based on authentication status.
-   **Modular Design:** Separating authentication logic into its own module (`features/auth.py`).

## Features Implemented

### 1. User Registration (Sign Up)
-   Allows new users to create an account with a unique username and password.
-   Passwords are securely hashed using `bcrypt` before storage.
-   Checks for existing usernames to prevent duplicates.
-   Stores user credentials (username, hashed password) in `database/users.txt`.

### 2. User Authentication (Login)
-   Users can log in with their registered username and password.
-   Verifies provided password against the stored hashed password using `bcrypt`.
-   Updates `st.session_state` to reflect the user's logged-in status and store their username.

### 3. Session Management
-   Uses `st.session_state` to persist the logged-in status (`'logged_in': True/False`) and the `username` across Streamlit reruns.
-   Application content is only accessible if `st.session_state['logged_in']` is `True`.

### 4. Logout Functionality
-   A dedicated button allows logged-in users to terminate their session.
-   Resets `st.session_state['logged_in']` to `False` and `st.session_state['username']` to `None`.

### 5. Protected Content
-   The entire Task Manager application (tasks, reminders, categories, analytics, export) is only displayed to authenticated users.
-   Non-authenticated users are redirected to the login/signup page.

## Implementation Details

### `features/auth.py`
-   **`USERS_FILE = "database/users.txt"`**: Defines the file path for storing user data.
-   **`load_users()` / `save_users(users)`**: Functions to handle reading from and writing to `users.txt`.
-   **`hash_password(password)`**: Encodes and hashes the password using `bcrypt.gensalt()` for a salt.
-   **`verify_password(password, hashed_password)`**: Decodes and checks the plaintext password against the hash.
-   **`register_user(username, password)`**: Adds a new user after hashing the password. Returns `False` if username exists.
-   **`authenticate_user(username, password)`**: Verifies username and password.
-   **`user_exists(username)`**: Utility function to check for username availability during signup.

### `streamlit_app/dashboard.py`
-   **Import `auth` module**: `from features import auth`.
-   **`show_login_page()` function**:
    -   Displays "Login" and "Sign Up" forms using `st.expander`.
    -   Login form: Takes username/password, calls `auth.authenticate_user()`, and updates `st.session_state`.
    -   Sign Up form: Takes new username/password, calls `auth.register_user()`, and updates UI messages.
-   **`show_main_app()` function**:
    -   Displays the main Task Manager UI (sidebar, navigation, content areas).
    -   Includes a "Logout" button that clears `st.session_state` and reruns the app.
-   **Main execution block (`if __name__ == "__main__":`)**:
    -   Initializes `st.session_state['logged_in']` and `st.session_state['username']`.
    -   Conditionally calls `show_main_app()` if logged in, otherwise `show_login_page()`.

## Success Criteria
✅ Users can successfully sign up.  
✅ Users can successfully log in with correct credentials.  
✅ Users are prevented from logging in with incorrect credentials.  
✅ Users can log out, returning to the login screen.  
✅ Application content is protected and only visible to logged-in users.  
✅ Passwords are stored securely as hashes.
