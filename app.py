from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, jsonify
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "qwertyuiop"

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "xlsx"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize the database
def init_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        
        # Users Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')

        # Files Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS files(
            id INTEGER PRIMARY KEY, filename TEXT, file_type TEXT, upload_date TEXT, user_id TEXT)''')

        conn.commit()

init_db()

# Home/Login Route
@app.route("/")
def login():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

    if user:
        session["username"] = username
        return redirect(url_for("dashboard"))
    else:
        return render_template("index.html", error="Invalid credentials")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

# Register Route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                return render_template("register.html", error="username already exists!")

            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

# Dashboard
@app.route("/dashboard")
def dashboard():
    if "username" in session:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM files WHERE user_id = ?", (session["username"],))
            files = cursor.fetchall()

        return render_template("dashboard.html", files=files)
    return redirect(url_for("login"))

# File Upload
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO files (filename, file_type, upload_date, user_id) VALUES (?, ?, datetime('now'), ?)",
                           (filename, filename.split(".")[-1], session["username"]))
            conn.commit()

        return redirect(url_for("dashboard"))
    else:
        return "Invalid file type", 400

# File Download
@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# API for file breakdown stats
@app.route("/file_stats")
def file_stats():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT file_type, COUNT(*) FROM files GROUP BY file_type")
        file_counts = dict(cursor.fetchall())

    return jsonify(file_counts)

# Allowed file types
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(debug=True)
