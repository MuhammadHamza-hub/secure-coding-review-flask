import sqlite3
import subprocess
from flask import Flask, request, render_template_string, redirect, session

app = Flask(__name__)
app.secret_key = "supersecret123"  # VULN: hardcoded secret key

DB = "notes.db"


def get_db():
    conn = sqlite3.connect(DB)
    return conn


def init_db():
    conn = get_db()
    conn.execute("""CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY, username TEXT, password TEXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS notes
                     (id INTEGER PRIMARY KEY, user TEXT, content TEXT)""")
    conn.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'admin123')")
    conn.commit()
    conn.close()


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # VULN: SQL Injection - string concatenation into query
        conn = get_db()
        query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
        cur = conn.execute(query)
        user = cur.fetchone()

        if user:
            session["user"] = username
            return redirect("/notes")
        return "Invalid credentials"

    return """
        <form method="post">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit">
        </form>
    """


@app.route("/notes", methods=["GET", "POST"])
def notes():
    user = session.get("user")
    if not user:
        return redirect("/login")

    conn = get_db()
    if request.method == "POST":
        content = request.form["content"]
        conn.execute("INSERT INTO notes (user, content) VALUES (?, ?)", (user, content))
        conn.commit()

    cur = conn.execute("SELECT content FROM notes WHERE user = ?", (user,))
    all_notes = [row[0] for row in cur.fetchall()]

    # VULN: Reflected/Stored XSS - notes rendered without escaping
    html = "<h1>Your Notes</h1><ul>"
    for n in all_notes:
        html += f"<li>{n}</li>"
    html += """</ul>
        <form method="post">
            <textarea name="content"></textarea>
            <input type="submit">
        </form>"""
    return render_template_string(html)


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    # VULN: Command Injection - user input passed straight to shell
    result = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True, text=True)
    return f"<pre>{result.stdout}</pre>"


@app.route("/download")
def download():
    filename = request.args.get("file", "readme.txt")
    # VULN: Path Traversal - no sanitization of filename
    with open(filename, "r") as f:
        return f.read()


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0")  # VULN: debug mode + public bind in "prod"