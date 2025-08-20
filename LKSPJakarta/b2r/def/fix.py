from flask import Flask, request, session, redirect, render_template_string, escape, url_for
import pyfiglet
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "fallback_key_dev")

BOOTSTRAP_HEAD = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>ASCII Art Generator</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container py-5">
"""

BOOTSTRAP_END = """
</div>
</body>
</html>
"""

@app.route("/")
def index():
    user = session.get("user")
    return BOOTSTRAP_HEAD + f'''
        <div class="card shadow-sm p-4">
            <h2 class="mb-3">Welcome to ASCII Art Generator!</h2>
            <div class="alert alert-info">Logged in as: <strong>{escape(user) if user else "guest"}</strong></div>
            <p><a href="/ascii-art" class="btn btn-primary">🎨 Try ASCII-ART Generator</a></p>
            <p><a href="/ascii-premium" class="btn btn-warning">🔐 Go to Pro ASCII-Art Generator</a></p>
            <p><a href="/login" class="btn btn-success">🔐 Login</a>
            <a href="/logout" class="btn btn-danger">Logout</a></p>
        </div>
    ''' + BOOTSTRAP_END

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        pw = request.form.get("password")
        if user == "admin" and pw == "admin123":  # bisa diganti pakai DB
            session["user"] = user
            return redirect(url_for("admin_panel"))
        else:
            return BOOTSTRAP_HEAD + '''
                <div class="alert alert-danger">❌ Login failed</div>
                <a href="/login" class="btn btn-secondary">Back</a>
            ''' + BOOTSTRAP_END

    return BOOTSTRAP_HEAD + '''
        <div class="card shadow p-4">
            <h2>Login</h2>
            <form method="post">
                <input name="username" placeholder="Username" class="form-control mb-2" required>
                <input name="password" placeholder="Password" type="password" class="form-control mb-2" required>
                <button class="btn btn-success">Login</button>
            </form>
        </div>
    ''' + BOOTSTRAP_END

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

@app.route("/ascii-premium", methods=["GET", "POST"])
def admin_panel():
    if session.get("user") != "admin":
        return redirect(url_for("login"))

    if request.method == "POST":
        user_input = request.form.get("template", "")
        if "{{" in user_input or "{%" in user_input:
            rendered = "<div class='alert alert-danger'>❌ Unsafe input detected.</div>"
        else:
            try:
                rendered = render_template_string(escape(user_input))
            except Exception as e:
                rendered = f"<div class='alert alert-danger'>Error rendering: {e}</div>"

        return BOOTSTRAP_HEAD + f'''
            <h2>Rendered Output</h2>
            <div class="card card-body bg-dark text-light">
                <pre>{rendered}</pre>
            </div>
            <a href="/ascii-premium" class="btn btn-secondary mt-3">Back</a>
        ''' + BOOTSTRAP_END

    return BOOTSTRAP_HEAD + '''
        <div class="card p-4 shadow">
            <h2 class="mb-3">🔧 Supreme Renderer</h2>
            <form method="post">
                <label for="template">Input your content:</label>
                <input id="template" name="template" size="80" class="form-control mb-3" />
                <button type="submit" class="btn btn-success">Render</button>
            </form>
        </div>
    ''' + BOOTSTRAP_END

@app.route("/ascii-art", methods=["GET", "POST"])
def asciiart():
    if request.method == "POST":
        text = request.form.get("text", "")
        try:
            safe_text = escape(text)
            result = pyfiglet.figlet_format(safe_text)
            content = f"<pre>{result}</pre>"
        except Exception as e:
            content = f"<div class='alert alert-danger'>Error: {e}</div>"

        return BOOTSTRAP_HEAD + f'''
            <h2 class="mb-3">🎨 ASCII Art Result</h2>
            {content}
            <a href="/ascii-art" class="btn btn-secondary mt-3">Try Again</a>
        ''' + BOOTSTRAP_END

    return BOOTSTRAP_HEAD + '''
        <div class="card p-4 shadow-sm">
            <h2 class="mb-3">🎨 ASCII Art Generator</h2>
            <form method="post">
                <label for="text">Text:</label>
                <input id="text" name="text" size="100" class="form-control mb-3" placeholder="Example: HELLO!" />
                <button type="submit" class="btn btn-primary">Generate</button>
            </form>
        </div>
    ''' + BOOTSTRAP_END

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8081)
