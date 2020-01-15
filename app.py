#Team super-duper-umbrella
#SoftDev1 pd1
#P02 -- The End
#2020-01-16

from flask import *
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
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
        session['username'] = user
        flash('Logged in successfully!', 'success')
        return redirect(url_for("home"))
    else:
        flash("Failed to log in")
        return redirect(url_for("login"))

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

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
def home():
    return render_template('home.html')

@app.route('/account', methods=['GET'])
def account():
    return render_template('account.html')

@app.route('/account', methods=['POST'])
def accountform():
    old_password = request.form["old_password"]
    new_password = request.form["new_password"]

    if (change_password(current_user,old_password,new_password)):
        flash("Successfully changed password")
        return redirect(url_for("home"))
    else:
        return redirect(url_for("account"))

@app.route('/invites', methods=['GET'])
def invites():
    i = get_invites(user = current_user)
    current = []
    for invite in i:
        if invite.status == 0:
            current.append(invite.project)
    return render_template('invites.html',
                            invites=current)

@app.route('/invites', methods=['POST'])
def invitesform():
    project = request.form["project"]
    response = request.form["response"]

    if (response == "yes"):
        accept_invite(current_user, project)
        flash("Successfully joined project: "+ project)
    else:
        decline_invite(current_user, project)
        flash("Rejected invite to project: "+ project)

    return redirect(url_for("invites"))

@app.route('/projects', methods=['GET'])
def projects():
    e = get_employments(user = current_user)
    current = []
    for employed in e:
        current.append(employed.project)

    m = Project.query.filter_by(manager=current_user.id).all()

    return render_template('projects.html',
                            myprojects = current,
                            managedprojects = m)

@app.route('/create', methods=['POST'])
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

@app.route('/project/<pid>', methods=['GET'])
def project(pid):
    project = Project.query.filter_by(id=pid).first()
    return render_template('id.html',
                            name=project.name,
                            description=project.description,
                            tasks=get_tasks(pid))

@app.route('/task_status', methods=['POST'])
def task_status():
    task = request.form["task"]
    status = request.form["status"]
    if (status == "1"):
        complete_task(task)
        flash("Completed task: "+ task)
    if (status == "-1"):
        delete_task(task)
        flash("Abandoned task: "+ task)
    return redirect(url_for("projects"))

@app.route('/edit', methods=['POST'])
def edit():
    project = request.form["project"]
    status = request.form["status"]

    check_manager = get_project(project)
    if (check_manager.manager != current_user.id):
        flash("You are not the manager of this project")
        return redirect(url_for("projects"))

    if (status == "1"):
        complete_project(project)
        flash("Completed project: "+ project)
    if (status == "-1"):
        abandon_project(project)
        flash("Abandoned project: "+ project)
    return redirect(url_for("projects"))

@app.route('/addtask', methods=['POST'])
def addtask():
    p = request.form["project"]

    check_manager = get_project(project)
    if (check_manager.manager != current_user.id):
        flash("You are not the manager of this project")
        return redirect(url_for("projects"))

    u = request.form["user"]
    s = request.form["status"]
    c = request.form["content"]
    d = request.form["deadline"]
    add_task(pname=p,uname=u,status=s,content=c,deadline=d)
    return redirect(url_for("projects"))

@app.route('/edittask', methods=['POST'])
def edittask():
    p = request.form["project"]

    check_manager = get_project(project)
    if (check_manager.manager != current_user.id):
        flash("You are not the manager of this project")
        return redirect(url_for("projects"))
    t = request.form["task"]
    c = request.form["content"]
    d = request.form["deadline"]
    edit_task(task=t,content=c,deadline=d)
    return redirect(url_for("projects"))

@app.route('/invite', methods=['POST'])
def invite():
    p = request.form["project"]

    check_manager = get_project(project)
    if (check_manager.manager != current_user.id):
        flash("You are not the manager of this project")
        return redirect(url_for("projects"))
    u = request.form["user"]
    add_invite(project=get_project(p),user=get_user(u))
    return redirect(url_for("projects"))

app.run(debug=True)
