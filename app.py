#Yevgeniy Gorbachev
#SoftDev1 pd1
#K<n> -- <K<n>.__name__>
#ISO 8601 Date

from flask import *
from os import urandom
import json


app = Flask(__name__)
app.secret_key = urandom(32)

@app.route('/')
def index():
    return render_template('_base.html')

@app.route('/newtask', methods=['POST'])
#this function needs to be redone to fit into database stuff
def addtask():
    taskid = len(testdata)
    testdata.append([taskid, request.form['projid'], "incomplete", "", ""])
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

app.run(debug=True)
