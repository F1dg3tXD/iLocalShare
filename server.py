from flask import Flask, request, send_from_directory, render_template, jsonify
import os

app = Flask(__name__, static_folder="static", template_folder="static")

UPLOAD_FOLDER = "shared"
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
    file = request.files["file"]
    if file:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return "File uploaded", 200

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
