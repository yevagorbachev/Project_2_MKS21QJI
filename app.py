#Team super-duper-umbrella
#SoftDev1 pd1
#P02 -- The End
#2020-01-16

from flask import *
from flask_login import LoginManager, login_required, login_user, logout_user
from os import urandom
from utl.models import db, User, Invites, Project, Task, Assignment, Employment
from utl.dbfuncs import *
from utl.errors import NoPerms
import json

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/sitedata.db'
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

    current1 = []
    for i in current:
        current1.append(Project.query.filter_by(id=i).first())
        print(current1)

    current2 = []
    for i in current1:
        current2.append(i.name)

    return render_template('invites.html',
                            invites=current2)

@app.route('/invites', methods=['POST'])
def invitesform():
    if('username' not in session):
        return redirect(url_for("login"))

    p = request.form["project"]
    response = request.form["response"]
    print(p)
    if (response == "y"):
        accept_invite(user=get_user(uname=session['username']), project=get_project_by_name(pname=p))
        flash("Successfully joined project: "+ p, 'success')
    else:
        decline_invite(user=get_user(uname=session['username']), project=get_project_by_name(pname=p))
        flash("Rejected invite to project: "+ p, 'primary')

    return redirect(url_for("invites"))

@app.route('/projects', methods=['GET'])
def projects():
    if('username' not in session):
        return redirect(url_for("login"))

    e = get_user_project(uid = get_user(uname=session['username']).id)
    print(e)
    current = []
    for employed in e:
        current.append(employed.project)

    m = Project.query.filter_by(manager=get_user(uname=session['username']).id).all()

    # print(m)
    return render_template('projects.html',
                            myprojects = current,
                            managedprojects = m)

@app.route('/create', methods=['POST'])
def create():
    if('username' not in session):
        return redirect(url_for("login"))

    name = request.form["name"]
    manager = get_user(uname=session['username']).id
    #teams = request.form["teams"]
    teams = '';
    #blurb = request.form["blurb"]
    blurb = '';
    description = request.form["description"]
    #log = request.form["log"]
    log = '';
    if (add_project(pname=name, manager=manager, teams=teams, blurb=blurb, description=description, log=log)):
        flash("Created project: "+ name, 'primary')
    else:
        flash("Project name not unique: "+ name, 'danger')
    return redirect(url_for("projects"))

@app.route('/projects/<pid>', methods=['GET'])
def project(pid):
    if('username' not in session):
        return redirect(url_for("login"))


    project = Project.query.filter_by(id=pid).first()
    t = get_tasks(projid=pid)
    print(t)
    return render_template('proj_info.html',
                            pid=pid,
                            name=project.name,
                            description=project.description,
                            tasks=t)

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

    check_manager = get_project_by_name(pname=project)
    if (check_manager.manager != get_user(uname=session['username']).id):
        flash("You are not the manager of this project",'danger')
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
    print(request.form)
    if('username' not in session):
        return redirect(url_for("login"))

    p = int(request.form["projid"])
    check_manager = get_project_by_id(pid=p)
    if (check_manager.manager != get_user(uname=session['username']).id):
        raise NoPerms('You are not the manager of this project')
    u = request.form['user']
    s = 'incomplete'
    c = ''
    d = ''
    taskid = add_task(pname=p,uname=u,status=s,content=c,deadline=d)
    return json.dumps({'id' : taskid})

@app.route('/edittask', methods=['GET', 'POST'])
def edittask():
    if('username' not in session):
        return redirect(url_for("login"))

    if request.method == 'GET':
        p = request.args["projid"]
        check_manager = get_project_by_id(pid=p)
        if (check_manager.manager != get_user(uname=session['username']).id):
            raise NoPerms('You are not the manager of this project')
        task = get_task(taskid=request.args['id'])
        return '<input type="hidden" id="id" value="{}"><textarea id="content">{}</textarea><br><input type="date" id="deadline" value="{}"><br><button class="btn btn-primary" id="push">Push Edits</button>'.format(task.id, task.content, task.deadline)
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

    print(p)
    check_manager = get_project_by_name(pname=p)
    if (check_manager.manager != get_user(uname=session['username']).id):
        flash("You are not the manager of this project",'danger')
        return redirect(url_for("projects"))

    u = request.form["uname"]

    if(get_user(uname=u) == None):
        flash("There is no user with that name",'danger')
        return redirect(url_for("projects"))

    add_invite(project=get_project_by_name(pname=p),user=get_user(uname=u))
    flash("Invite sent",'success')
    return redirect(url_for("projects"))

app.run(debug=True)
