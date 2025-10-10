# from flask import Flask, render_template, request, redirect, url_for
import os
from flask import Flask, request, render_template_string, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'dummy_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Dummy user class
class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = "123"
        self.password = "123"

    def get_id(self):
        return self.id

# Only one user!
users = {'123': User('123')}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == '123' and password == '123':
            user = users[username]
            login_user(user)
            return redirect(url_for('index'))
        return render_template_string(LOGIN_TEMPLATE, error="Invalid credentials.")
    return render_template_string(LOGIN_TEMPLATE)

LOGIN_TEMPLATE = '''
<!doctype html>
<title>Login</title>
<h2>Login</h2>
{% if error %}
<p style="color:red;">{{ error }}</p>
{% endif %}
<form method="post">
    Username: <input name="username" type="text"><br>
    Password: <input name="password" type="password"><br>
    <input type="submit" value="Login">
</form>
'''

#cooper start
# folder where uploaded files will be stored
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')

# key used so flash messages can work
# the secret key is used to secure and validate the data saved in the user's session cookie
app.secret_key = os.environ.get('FLASK_SECRET', 'dev_secret_key')

# To limit file types that can be uploaded
ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png', 'mp3', 'mp4', 'mov'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# home page route
@app.route('/index')
def index():
    return render_template('index.html')


# upload route, only works with POST requests,  POST requests are used for sending data to the server
@app.route('/upload', methods=['POST'])
def upload():
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
            else:
                skipped.append(fname)

    if skipped:
        flash(f'Skipped files with unsupported extensions: {", ".join(skipped)}')
    else:
        flash('All files uploaded successfully!')

    # show success message and redirect to home page
    flash('Files uploaded successfully!')
    return redirect(url_for('index'))

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

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
# 
