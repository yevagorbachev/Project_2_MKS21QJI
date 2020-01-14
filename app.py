#Team super-duper-umbrella
#SoftDev1 pd1
#P02 -- The End
#2020-01-16

from flask import *
from flask_login import LoginManager, login_required, current_user
from os import urandom

from models import db, User, Project, Task, Assignment, Employment
from utl.dbfuncs import *

app = Flask(__name__)

# set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please Log In to view this page!'
login_manager.login_message_category = 'danger'

# app configurations
app.config['SECRET_KEY'] = (urandom(64))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['USE_SESSION_FOR_NEXT'] = True

# start database
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    if('username' in session):
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def loginform():
    user = request.form["username"]
    password = request.form["password"]
    if (verify_user(user=user, password=password)):
        flash("Successfully logged in")
        return redirect(url_for("home"))
    else:
        flash("Failed to log in")
        return redirect(url_for("login"))

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def registerform():
    user = request.form["username"]
    password = request.form["password"]

    check_user = User.query.filter_by(username=user).first()

    if (check_user != None):
        flash("Username is taken. Please try again.")
        return redirect(url_for("register"))
    else:
        add_user(user=user, password=password)
        return redirect(url_for("login"))

@app.route('/home', methods=['GET'])
@login_required
def home():
    return render_template('home.html')

@app.route('/account', methods=['GET'])
@login_required
def account():
    return render_template('account.html')

@app.route('/account', methods=['POST'])
@login_required
def accountform():
    old_password = request.form["old_password"]
    new_password = request.form["new_password"]

    if (change_password(current_user,old_password,new_password)):
        flash("Successfully changed password")
        return redirect(url_for("home"))
    else:
        return redirect(url_for("account"))

@app.route('/invites', methods=['GET'])
@login_required
def invites():
    return render_template('invites.html')

@app.route('/invites', methods=['POST'])
@login_required
def invitesform():
    project = request.form["project"]
    response = request.form["response"]

    if (response == "yes"):
        flash("Successfully joined project: "+ project)
        return redirect(url_for("home"))
    else:
        flash("Rejected invite to project: "+ project)
        return redirect(url_for("invites"))

@app.route('/projects', methods=['GET'])
@login_required
def projects():
    return render_template('projects.html')

@app.route('/create', methods=['POST'])
@login_required
def create():
    name = request.form["name"]
    manager = current_user.id
    teams = request.form["teams"]
    blurb = request.form["blurb"]
    description = request.form["description"]
    log = request.form["log"]
    if (add_project(name, manager, teams, blurb, description, log)):
        flash("Created project: "+ name)
    else:
        flash("Project name not unique: "+ name)
    return redirect(url_for("project"))

@app.route('/project/<id>', methods=['GET'])
@login_required
def project(id):
    return render_template('id.html')

@app.route('/task_status', methods=['POST'])
@login_required
def task_status():
    project = request.form["project"]
    status = request.form["status"]
    if (status == "1"):
        complete_project(project)
        flash("Completed project: "+ project)
    if (status == "-1"):
        abandon_project(project)
        flash("Abandoned project: "+ project)
    return redirect(url_for("project"))

app.run(debug=True)
