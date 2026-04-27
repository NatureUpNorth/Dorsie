import os
import json
from flask import Flask, render_template, request, flash, session, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

from PIL import Image
from PIL.ExifTags import TAGS

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

# Main Page Route
@app.route("/index")
@login_required
def index():
    return render_template("index.html")

# Other "routes" (not actual pages)

<<<<<<< HEAD
=======
@app.route("/location")
@login_required
def location():
    return render_template("map.html")

>>>>>>> manual_merge
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

# EXIF extraction helper
def get_exif_data(filepath):
    try:
        image = Image.open(filepath)
        exif_data = image._getexif()
        if not exif_data:
            return {}
        readable = {}
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if isinstance(value, bytes):
                continue
            readable[tag] = str(value)
        return readable
    except Exception:
        return {}
<<<<<<< HEAD

=======
>>>>>>> manual_merge

@app.route("/submit_all", methods=["POST"])
@login_required
def submit_all():
    os.makedirs("uploads", exist_ok=True)

    uploaded_files = []
    files = request.files.getlist("file")

    total_files = len([f for f in files if f and f.filename and allowed_file(f.filename)])
<<<<<<< HEAD
    pad_width = len(str(total_files))
=======
    pad_width = len(str(total_files)) if total_files > 0 else 1
>>>>>>> manual_merge

    file_counter = 1

    for f in files:
        if f and f.filename and allowed_file(f.filename):
            ext = os.path.splitext(f.filename)[1].lower()
            new_filename = str(file_counter).zfill(pad_width) + ext

            save_path = os.path.join("uploads", new_filename)
            f.save(save_path)

            exif = get_exif_data(save_path)
            uploaded_files.append({
                "filename": new_filename,
                "original_filename": os.path.basename(f.filename),
                "filepath": save_path,
                "exif": exif
            })
            file_counter += 1

    # Fall back to form-submitted hidden inputs if session coords not set
    lat = session.get("latitude") or request.form.get("latitude")
    lon = session.get("longitude") or request.form.get("longitude")

    record = {
        "affiliation": {
            "type": request.form.get("affiliation_type"),
            "sub": request.form.get("sub_affiliation")
        },
        "habitat": request.form.getlist("habitat"),
        "urbanization": request.form.get("urbanization"),
        "dates": {
            "start_date": request.form.get("start_date"),
            "end_date": request.form.get("end_date")
        },
        "coordinates": {
            "lat": lat,
            "lon": lon
        },
        "camera": {
            "choice": request.form.get("camera_choice"),
            "model": request.form.get("camera_model") 
        },
        "location_name": request.form.get("location"),
        "comment": request.form.get("comment"),
        "uploaded_files": uploaded_files
    }

    with open("uploads/record.json", "w") as f:
        json.dump(record, f, indent=4)

    flash("All data submitted successfully!")
    return redirect("/index")

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)