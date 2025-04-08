from flask import Flask, request, send_from_directory, render_template, jsonify
import os
import socket

app = Flask(__name__, static_folder="static", template_folder="static")

UPLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Documents", "iLocalShareUploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/requires-auth")
def requires_auth():
    return jsonify({"requiresAuth": False})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/files")
def list_files():
    return jsonify(os.listdir(UPLOAD_FOLDER))

@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("files")
    if not files:
        return "No files selected", 400

    for file in files:
        if file.filename:
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))

    return "Files uploaded", 200

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

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
        "port": 5500  # Change this if you're running the server on a different port
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500, debug=True)
