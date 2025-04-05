import os
import subprocess
import sys
import threading
import signal
from pystray import Icon, MenuItem as Item, Menu
from PIL import Image
import webbrowser

current_server = None
server_type = None  # "open" or "private"

def open_ui():
    webbrowser.open("http://127.0.0.1:5500")

def run_server(script_name):
    global current_server
    if current_server:
        current_server.terminate()
        current_server.wait()
        current_server = None

    current_server = subprocess.Popen([sys.executable, script_name])
    print(f"Started {script_name}")

def start_open():
    global server_type
    server_type = "open"
    run_server("server.py")

# def start_private(): # Private mode deprecated
#     global server_type
#     server_type = "private"
#     run_server("secure-server.py")

def restart_open():
    start_open()

# def restart_private(): # Private mode deprecated
#     start_private()

def open_uploads_folder():
    folder_path = os.path.join(os.path.expanduser("~"), "Documents", "iFileShareUploads")
    if os.path.exists(folder_path):
        subprocess.run(["open", folder_path])
    else:
        print("Upload folder does not exist.")

def change_password():
    # Use TextEdit to let the user edit the password.txt
    subprocess.Popen(["open", "-a", "TextEdit", "password.txt"])

def exit_app(icon, item):
    if current_server:
        current_server.terminate()
        current_server.wait()
    icon.stop()

def setup_tray():
    image = Image.open("icon.png")

    menu = Menu(
        Item("Open Web UI", lambda: open_ui()),
        Item("Restart", lambda: restart_open()),
        # Item("Restart in Private", lambda: restart_private()), Private mode deprecated
        # Item("Change Password", lambda: change_password()),
        Item("Open Uploads Folder", open_uploads_folder),
        Item("Quit", exit_app)
    )

    icon = Icon("iFileShare", image, "iFileShare", menu)
    icon.run()

if __name__ == "__main__":
    # Start open server by default
    threading.Thread(target=start_open, daemon=True).start()
    setup_tray()