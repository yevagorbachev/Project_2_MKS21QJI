#Yevgeniy Gorbachev
#SoftDev1 pd1
#K<n> -- <K<n>.__name__>
#ISO 8601 Date

from flask import *
from os import urandom


app = Flask(__name__)
app.secret_key = urandom(32)

# @app.route('/')
# def index():
#     return render_template('_base.html')

## run template tests
@app.route("/")
def root():
    if ("userid" in session): #if signed in, go to profile
        return redirect(url_for('profile'))
    return redirect(url_for('sign')) #else go to sign-in options

#welcome page with sign-in options
@app.route("/welcome")
def sign():
    return render_template('base_prof.html')

app.run(debug=True)
