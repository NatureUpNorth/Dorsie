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
    return render_template("index.html")

# Location/Map route (not sure if still needed)
@app.route("/location")
@login_required
def location():
    return render_template("map.html")


# Other "routes" (not actual pages)

@app.route("/save_dates", methods=["POST"])
@login_required
def save_dates():
    session["start_date"] = request.form.get("start_date")
    session["end_date"] = request.form.get("end_date")
    return jsonify({"status": "ok"})


@app.route("/save_coordinates", methods=["POST"])
@login_required
def save_coordinates():
    data = request.get_json()
    session["latitude"] = data.get("latitude")
    session["longitude"] = data.get("longitude")
    return jsonify({"message": "Coordinates saved successfully"}), 200


@app.route("/upload_files", methods=["POST"])
@login_required
def upload_files():
    files = request.files.getlist("file")
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    saved_files = []
    for f in files:
        if f and allowed_file(f.filename):
            path = os.path.join(app.config["UPLOAD_FOLDER"], f.filename)
            f.save(path)
            saved_files.append(f.filename)

    session["files"] = saved_files
    return jsonify({"status": "ok", "files": saved_files})


@app.route("/submit_all", methods=["POST"])
@login_required
def submit_all():
    os.makedirs("uploads", exist_ok=True)

    uploaded_files = []
    files = request.files.getlist("file")
    for f in files:
        if f and f.filename:
            save_path = os.path.join("uploads", f.filename)
            f.save(save_path)
            uploaded_files.append(f.filename)

    record = {
        "affiliation": {
            "type": request.form.get("affiliation_type"),
            "sub": request.form.get("sub_affiliation")
        },
        "habitat": {
            "type": request.form.get("mainHabitat"),
            "sub": request.form.get("subHabitat")
        },
        "dates": {
            "start_date": request.form.get("start_date"),
            "end_date": request.form.get("end_date")
        },

        #SAVING LATITUDE AND LONGITUDE FROM MAP
        "coordinates": {
            "lat": session.get("latitude"),
            "lon": session.get("longitude")
        },

        "location_name": request.form.get("location"),
        "uploaded_files": uploaded_files
    }

    with open("uploads/record.json", "w") as f:
        json.dump(record, f, indent=4)

    flash("All data submitted successfully!")
    return redirect("/index")


if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)

