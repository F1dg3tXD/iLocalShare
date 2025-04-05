from flask import Flask, request, send_from_directory, render_template, session, redirect, url_for, jsonify
import os
import socket

app = Flask(__name__, static_folder="static", template_folder="static")
app.secret_key = os.urandom(24)
UPLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Documents", "iFileShareUploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ADMIN_PASSWORD = os.getenv("FILESHARE_PASSWORD", "defaultpassword")

@app.route("/", methods=["GET"])
def index():
    if "authenticated" in session:
        return render_template("index.html")
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login_post():
    if request.form.get("password") == ADMIN_PASSWORD:
        session["authenticated"] = True
        return jsonify({"success": True})
    return jsonify({"success": False}), 403

@app.route("/requires-auth")
def requires_auth():
    return jsonify({"requiresAuth": True})

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
    return redirect(url_for("index"))

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
        "port": 5500
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500, debug=True)