import os
import sys
import subprocess
import atexit
import psutil  # For killing running processes
import pystray
from pystray import MenuItem as item, Icon
from PIL import Image
import webbrowser

LOCK_FILE = "ilocalshare.lock"
server_process = None  # Track running server

def is_another_instance_running():
    if os.path.exists(LOCK_FILE):
        return True
    with open(LOCK_FILE, "w") as file:
        file.write(str(os.getpid()))
    return False

def cleanup():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)
    stop_server()  # Ensure the server is closed on exit

atexit.register(cleanup)

if is_another_instance_running():
    print("iLocalShare is already running.")
    sys.exit(0)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_EXEC = sys.executable

def stop_server():
    """Kill the currently running server process."""
    global server_process
    if server_process and server_process.poll() is None:  # If it's running
        try:
            print("Stopping current server...")
            parent = psutil.Process(server_process.pid)
            for child in parent.children(recursive=True):
                child.terminate()  # Kill child processes
            parent.terminate()  # Kill main process
            server_process.wait()
            print("Server stopped.")
        except Exception as e:
            print(f"Failed to stop server: {e}")
    server_process = None

def start_server(mode):
    """Restart the server in Open or Private mode."""
    global server_process
    stop_server()  # Kill any running server first

    server_script = "server.py" if mode == "open" else "secure-server.py"
    server_path = os.path.join(SCRIPT_DIR, server_script)

    if not os.path.exists(server_path):
        print(f"Error: {server_script} not found in {SCRIPT_DIR}")
        return

    try:
        server_process = subprocess.Popen(
            [PYTHON_EXEC, server_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        )
        print(f"Started {server_script}")
    except Exception as e:
        print(f"Failed to start {server_script}: {e}")

# Automatically start the server in Open mode when tray starts
start_server("open")

def open_web_ui():
    webbrowser.open("http://127.0.0.1:5500")

def open_uploads_folder():
    folder_path = os.path.join(os.path.expanduser("~"), "Documents", "iLocalShareUploads")
    if os.path.exists(folder_path):
        subprocess.run(["explorer", folder_path], shell=True)
    else:
        print("Upload folder does not exist.")

def exit_app(icon, item):
    stop_server()  # Ensure the server stops when exiting
    icon.stop()
    sys.exit(0)

icon_image = Image.open("icon.png")

menu = (
    item("Open Web UI", open_web_ui),
    item("Restart in Open", lambda icon, item: start_server("open")),
    # item("Restart in Private", lambda icon, item: start_server("private")), # Private mode deprecated
    pystray.MenuItem("Open Uploads Folder", open_uploads_folder),
    item("Exit", exit_app)
)

tray_icon = Icon("iLocalShare", icon_image, menu=menu)
tray_icon.run()
