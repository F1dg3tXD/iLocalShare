from flask import Flask, request, send_from_directory, render_template, session, redirect, url_for, jsonify
import os
import socket

app = Flask(__name__, static_folder="static", template_folder="static")
app.secret_key = os.urandom(24)
UPLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Documents", "iFileShareUploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

PASSWORD_FILE = "password.txt"

def load_password():
    """Load the password from the password.txt file."""
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as file:
            return file.read().strip()
    return None  # No password set

ADMIN_PASSWORD = load_password()

@app.route("/", methods=["GET", "POST"])
def login():
    global ADMIN_PASSWORD
    if "authenticated" in session:
        return render_template("index.html")

    if request.method == "POST":
        entered_password = request.form.get("password", "")
        if entered_password == ADMIN_PASSWORD:
            session["authenticated"] = True
            return render_template("index.html")
        return "Wrong password", 403

    return render_template("login.html")  # Ensure a login page is shown

@app.route("/requires-auth")
def requires_auth():
    """Inform frontend if authentication is required."""
    return jsonify({"requiresAuth": True})

@app.route("/change-password", methods=["POST"])
def change_password():
    """Change the server's access password."""
    global ADMIN_PASSWORD
    if "authenticated" not in session:
        return "Unauthorized", 403

    new_password = request.form.get("new_password", "").strip()
    if new_password:
        with open(PASSWORD_FILE, "w") as file:
            file.write(new_password)
        ADMIN_PASSWORD = new_password
        return "Password updated", 200
    return "Invalid password", 400

@app.route("/files")
def list_files():
    if "authenticated" not in session:
        return jsonify([]), 403
    return jsonify(os.listdir(UPLOAD_FOLDER))

@app.route("/upload", methods=["POST"])
def upload():
    if "authenticated" not in session:
        return "Unauthorized", 403

    files = request.files.getlist("files")
    if not files:
        return "No files selected", 400

    for file in files:
        if file.filename:
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    
    return "Files uploaded", 200

@app.route("/download/<filename>")
def download(filename):
    if "authenticated" not in session:
        return "Unauthorized", 403
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/logout")
def logout():
    session.pop("authenticated", None)
    return redirect(url_for("login"))

# Function to get local IP address
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

@app.route("/server-info")
def server_info():
    return jsonify({
        "ip": get_local_ip(),
        "port": 5000  # Change this if you're running the server on a different port
    })

if __name__ == "__main__":
    if not ADMIN_PASSWORD:
        print("Error: No password set! Please create 'password.txt' with a password before running the server.")
        exit(1)

    app.run(host="0.0.0.0", port=5000, debug=True)
