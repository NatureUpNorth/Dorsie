import os
import json
from flask import Flask, render_template, request, flash, session, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask(__name__)
app.secret_key = "secret"
app.config['UPLOAD_FOLDER'] = 'uploads'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


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


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/index")
@login_required
def index():
    return render_template('upload.html')

@app.route("/location")
@login_required
def location():
    return render_template("map.html")

# upload route, only works with POST requests,  POST requests are used for sending data to the server
@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        # check if the form/request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('index'))

        # get a list of files from the request
        files = request.files.getlist('file')

        # make sure at least one file was selected
        if not files or files[0].filename == '':
            flash('No selected file')
            return redirect(url_for('index'))

        # create upload folder if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        skipped = []

        # save each uploaed file to the upload folder
        for file in files:
            if file and file.filename:
                # clean and simplify the filename to make it secure
                fname = secure_filename(os.path.basename(file.filename))
                if not fname:
                    continue
                # only save files with allowed extensions
                if allowed_file(fname):
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))          
        # show success message and redirect to home page
        flash('Files uploaded successfully!')
        return redirect(url_for('index'))

    return render_template('upload.html')

# @app.route('/index', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         image = request.files.get('image')
#         if image:
#             image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
#         return redirect(url_for('affiliation'))
#     return render_template('index.html')


@app.route('/affiliation', methods=['GET', 'POST'])
def affiliation():
    if request.method == 'POST':
        # Step 1: Choose affiliation type
        selected_type = request.form.get('affiliation_type')
        if selected_type:
            return render_template('affiliation_sub.html', affiliation_type=selected_type)
    return render_template('affiliation.html')


@app.route('/affiliation/submit', methods=['POST'])
def submit_affiliation():
    affiliation_type = request.form.get('affiliation_type')
    sub_affiliation = request.form.get('sub_affiliation')

    print(f"Affiliation Type: {affiliation_type}")
    print(f"Sub Affiliation: {sub_affiliation}")

    return redirect(url_for('habitat'))

#
# @app.route('/affiliation', methods=['GET', 'POST'])
# def affiliation():
#     if request.method == 'POST':
#         affiliation = request.form.get('affiliation')
#         print(f"Affiliation: {affiliation}")
#         return redirect(url_for('habitat'))
#     return render_template('affiliation.html')

@app.route('/habitat', methods=['GET', 'POST'])
def habitat():
    if request.method == 'POST':
        main = request.form.get('mainHabitat')
        sub = request.form.get('subHabitat')
        print(f"Main: {main}, Sub: {sub}")
        return redirect(url_for('dates'))
    return render_template('habitat.html')

@app.route('/dates', methods=['GET', 'POST'])
def dates():
    if request.method == 'POST':
        date = request.form.get('date')
        print(f"Date: {date}")
        return redirect(url_for('location'))
    return render_template('dates.html')

@app.route('/location', methods=['GET', 'POST'])
def location():
    if request.method == 'POST':
        location = request.form.get('location')
        print(f"Location: {location}")
        return redirect(url_for('index'))  # or thank you page
    return render_template('location.html')

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
