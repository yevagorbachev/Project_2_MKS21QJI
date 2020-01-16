#Team super-duper-umbrella
#SoftDev1 pd1
#P02 -- The End
#2020-01-16

from flask import *
from flask_login import LoginManager, login_required, login_user, logout_user
from os import urandom
from models import db, User, Invites, Project, Task, Assignment, Employment
from utl.dbfuncs import *
from utl.errors import NoPerms

app = Flask(__name__)

# set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please Log In to view this page!'
login_manager.login_message_category = 'danger'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

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
    if('username' not in session):
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

    if (verify_user(uname=user, password=password)):
        session['username'] = user
        flash('Logged in successfully!', 'success')
        return redirect(url_for("projects"))
    else:
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
        add_user(uname=user, password=password)
        return redirect(url_for("login"))

@app.route('/home', methods=['GET'])
def home():
    if('username' not in session):
        return redirect(url_for("login"))

    return render_template('home.html')

@app.route('/account', methods=['GET'])
def account():
    if('username' not in session):
        return redirect(url_for("login"))

    return render_template('account.html')

@app.route('/account', methods=['POST'])
def accountform():
    if('username' not in session):
        return redirect(url_for("login"))

    op = request.form["old_password"]
    np = request.form["new_password"]

    change_password(user=get_user(uname=session['username']),old_password=op,new_password=np)
    return redirect(url_for("account"))

@app.route('/invites', methods=['GET'])
def invites():
    if('username' not in session):
        return redirect(url_for("login"))

    print(get_user(uname=session['username']))
    i = get_invites(user=get_user(uname=session['username']))
    current = []
    for invite in i:
        if invite.status == 0:
            current.append(invite.project)
    return render_template('invites.html',
                            invites=current)

@app.route('/invites', methods=['POST'])
def invitesform():
    if('username' not in session):
        return redirect(url_for("login"))

    project = request.form["project"]
    response = request.form["response"]

    if (response == "yes"):
        accept_invite(get_user(uname=session['username']), project)
        flash("Successfully joined project: "+ project, 'success')
    else:
        decline_invite(get_user(uname=session['username']), project)
        flash("Rejected invite to project: "+ project, 'primary')

    return redirect(url_for("invites"))

@app.route('/projects', methods=['GET'])
def projects():
    if('username' not in session):
        return redirect(url_for("login"))

    print(session)
    e = get_user_project(uid = get_user(uname=session['username']).id)
    current = []
    for employed in e:
        current.append(employed.project)

    m = Project.query.filter_by(manager=get_user(uname=session['username']).id).all()

    return render_template('projects.html',
                            myprojects = current,
                            managedprojects = m)

@app.route('/create', methods=['POST'])
def create():
    if('username' not in session):
        return redirect(url_for("login"))

    name = request.form["name"]
    manager = get_user(uname=session['username']).id
    teams = request.form["teams"]
    blurb = request.form["blurb"]
    description = request.form["description"]
    log = request.form["log"]
    if (add_project(name, manager, teams, blurb, description, log)):
        flash("Created project: "+ name, 'primary')
    else:
        flash("Project name not unique: "+ name, 'danger')
    return redirect(url_for("project"))

@app.route('/projects/<pid>', methods=['GET'])
def project(pid):
    if('username' not in session):
        return redirect(url_for("login"))

    project = Project.query.filter_by(id=pid).first()
    return render_template('id.html',
                            name=project.name,
                            description=project.description,
                            tasks=get_tasks(pid))

@app.route('/task_status', methods=['POST'])
def task_status():
    if('username' not in session):
        return redirect(url_for("login"))

    task = request.form["task"]
    status = request.form["status"]
    if (status == "1"):
        complete_task(task)
        flash("Completed task: "+ task, 'success')
    if (status == "-1"):
        delete_task(task)
        flash("Abandoned task: "+ task, 'dark')
    return redirect(url_for("projects"))

@app.route('/edit', methods=['POST'])
def edit():
    if('username' not in session):
        return redirect(url_for("login"))

    project = request.form["project"]
    status = request.form["status"]

    check_manager = get_project(project)
    if (check_manager.manager != get_user(uname=session['username']).id):
        flash("You are not the manager of this project", 'danger')
        return redirect(url_for("projects"))

    if (status == "1"):
        complete_project(project)
        flash("Completed project: "+ project,'success')
    if (status == "-1"):
        abandon_project(project)
        flash("Abandoned project: "+ project,'dark')
    return redirect(url_for("projects"))

@app.route('/newtask', methods=['POST'])
def addtask():
    if('username' not in session):
        return redirect(url_for("login"))

    p = int(request.form["projid"])
    check_manager = get_project(project)
    if (check_manager.manager != get_user(uname=session['username']).id):
        raise NoPerms('You are not the manager of this project')
    u = request.form["user"]
    s = request.form["status"]
    c = request.form["content"]
    d = request.form["deadline"]
    taskid = add_task(pname=p,uname=u,status=s,content=c,deadline=d)
    return taskid;

@app.route('/edittask', methods=['GET', 'POST'])
def edittask():
    if('username' not in session):
        return redirect(url_for("login"))

    if request.method == 'GET':
        p = request.form["project"]
        check_manager = get_project(project)
        if (check_manager.manager != get_user(uname=session['username']).id):
            raise NoPerms('You are not the manager of this project')
        task = get_task(int(request.args['id']))
        return '<input type="hidden" id="id" value="{}">User:<input type="text" id="user"><br><textarea id="content">{}</textarea><br><input type="date" id="deadline" value="{}"><br><button class="btn btn-primary" id="push">Push Edits</button>'.format(task.id, task.content, task.deadline)
    else:
        t = int(request.form["id"])
        c = request.form["content"]
        d = request.form["deadline"]
        edit_task(task=t,content=c,deadline=d)
        task = get_task(t);
        return '{} - <i>{}</i>: {}'.format(d, task.status, c)

@app.route('/invite', methods=['POST'])
def invite():
    if('username' not in session):
        return redirect(url_for("login"))

    p = request.form["project"]

    check_manager = get_project(project)
    if (check_manager.manager != get_user(uname=session['username']).id):
        flash("You are not the manager of this project",'danger')
        return redirect(url_for("projects"))
    u = request.form["user"]
    add_invite(project=get_project(p),user=get_user(u))
    return redirect(url_for("projects"))

app.run(debug=True)
