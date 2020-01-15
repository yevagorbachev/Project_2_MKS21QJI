#Team super-duper-umbrella
#SoftDev1 pd1
#P02 -- The End
#2020-01-16

from flask import *
from os import urandom
import utl


app = Flask(__name__)
app.secret_key = urandom(32)
#
# @app.route('/')
# def index():
#     return render_template('_base.html')

@app.route("/welcome")
def welcome():
    return render_template('invites.html')

@app.route('/newtask', methods=['POST'])
#this function needs to be redone to fit into database stuff
def addtask():
    taskid = len(#<list of elements in a project with pid request.form['projid']>)
    add_task(request.form['projid'], taskid, "incomplete", "", "")
    print(taskid)
    return json.dumps({'id': taskid})

@app.route('/edittask', methods=['GET', 'POST'])
def edittask():
    task = [-1, -1, "", "", ""]
    if request.method == 'GET':
        taskid = int(request.args['id'])
        #the following code should be changed to database fetch code
        #==========
        for entry in testdata:
            if entry[0] == taskid:
                task = entry
        #==========
        return '<input type="hidden" id="id" value="{}"><input type="text" id="status" value="{}"><br><textarea id="content">{}</textarea><br><input type="date" id="deadline" value="{}"><br><button class="btn btn-primary" id="push">Push Edits</button>'.format(task[0], task[2], task[3], task[4])
    else:
        taskid = int(request.form['id'])
        #the following code should be changed to database update code
        #==========
        for entry in testdata:
            if entry[0] == taskid:
                entry[2] = request.form['stat']
                entry[3] = request.form['content']
                entry[4] = request.form['deadline']
        #==========
                return "{}-<b>{}</b>: <i>{}</i>".format(request.form['deadline'], request.form['content'], request.form['stat'])

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def profile():
    return render_template('home.html')

@app.route('/account')
def managed():
    return render_template('account.html')

@app.route('/invites')
def joined():
    return render_template('invites.html')

@app.route('/projects')
def create():
    return render_template('projects.html')

@app.route('/projects/<id>')
def create():
    return render_template('id.html')


app.run(debug=True)
