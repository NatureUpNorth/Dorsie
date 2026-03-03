import os
import json
from flask import Flask, render_template, request, flash, session, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user


# App Setup
app = Flask(__name__)
app.secret_key = "secret"
app.config['UPLOAD_FOLDER'] = 'uploads'

# Login Manager Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# User Setup and Login (Prototype)
class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = "123"
        self.password = "123"

    def get_id(self):
        return self.id


users = {"123": User("123")}


@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)


# Login Route
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "123" and password == "123":
            login_user(users["123"])
            return redirect(url_for("index"))

        flash("Invalid login. Try again.")
        return redirect("/")

    return """
    <!doctype html>
    <title>Login</title>
    <h2>Login</h2>
    <form method="post">
        Username: <input name="username" type="text"><br>
        Password: <input name="password" type="password"><br><br>
        <input type="submit" value="Login">
    </form>
    """


# Allowed File Extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Page Routes

# Main page route
@app.route("/index")
@login_required
def index():
    return render_template("indexcopy.html")


if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
