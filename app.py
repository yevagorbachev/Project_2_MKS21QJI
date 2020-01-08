#Team super-duper-umbrella
#SoftDev1 pd1
#P02 -- The End
#2020-01-16

from flask import *
from os import urandom


app = Flask(__name__)
app.secret_key = urandom(32)

@app.route('/')
def index():
    return render_template('_base.html')

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
