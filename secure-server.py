from flask import Flask, request, send_from_directory, render_template, session, redirect, url_for, jsonify
import os

app = Flask(__name__, static_folder="static", template_folder="static")
app.secret_key = os.urandom(24)
UPLOAD_FOLDER = "shared"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ADMIN_PASSWORD = os.getenv("FILESHARE_PASSWORD", "defaultpassword")

@app.route("/", methods=["GET", "POST"])
def login():
    if "authenticated" in session:
        return render_template("index.html")

    if request.method == "POST":
        if request.form["password"] == ADMIN_PASSWORD:
            session["authenticated"] = True
            return render_template("index.html")
        return "Wrong password", 403

    return render_template("index.html")

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
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
