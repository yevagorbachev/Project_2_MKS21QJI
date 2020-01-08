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

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/profile/managed')
def managed():
    return render_template('managed.html')

@app.route('/profile/joined')
def joined():
    return render_template('joined.html')

@app.route('/create')
def create():
    return render_template('create.html')


app.run(debug=True)
