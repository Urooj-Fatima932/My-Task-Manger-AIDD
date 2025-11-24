import subprocess
import sys

def main():
    """
    Main function to run the Task Manager Streamlit app.
    """
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app/dashboard.py"])
    except FileNotFoundError:
        print("Error: streamlit is not installed. Please install it with 'pip install streamlit'")

if __name__ == "__main__":
    main()
