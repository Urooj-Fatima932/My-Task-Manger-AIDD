import json
import bcrypt

USERS_FILE = "database/users.txt"

def load_users():
    """
    Loads user data from the users.txt file.
    """
    try:
        with open(USERS_FILE, "r") as f:
            users = [json.loads(line) for line in f]
        return users
    except FileNotFoundError:
        return []

def save_users(users):
    """
    Saves user data to the users.txt file.
    """
    with open(USERS_FILE, "w") as f:
        for user in users:
            f.write(json.dumps(user) + "\n")

def hash_password(password):
    """
    Hashes a password using bcrypt.
    """
    hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')

def verify_password(password, hashed_password):
    """
    Verifies a password against a hashed password.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def register_user(username, password):
    """
    Registers a new user with a hashed password.
    Returns True on success, False if username already exists.
    """
    users = load_users()
    if any(user['username'] == username for user in users):
        return False
    
    hashed_password = hash_password(password)
    new_user = {"username": username, "password": hashed_password}
    users.append(new_user)
    save_users(users)
    return True

def authenticate_user(username, password):
    """
    Authenticates a user.
    Returns True on successful authentication, False otherwise.
    """
    users = load_users()
    for user in users:
        if user['username'] == username:
            if verify_password(password, user['password']):
                return True
            else:
                return False # Incorrect password
    return False # User not found

def user_exists(username):
    """
    Checks if a user with the given username already exists.
    """
    users = load_users()
    return any(user['username'] == username for user in users)

