from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()

class User(db.Model):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    token = db.Column(db.Text)


    def __init__(self, username, password, tokentype):
        self.username = username
        self.password = password

class Invites(db.Model):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Integer, nullable=False)

    def __init__(self, project, user, status):
        self.project = project
        self.user = user
        self.status = 0

class Project(db.Model):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    manager = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    teams = db.Column(db.Text)
    blurb = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    log = db.Column(db.Text)
    calendarid = db.Column(db.Text)

    def __init__(self, name, status, manager, teams, blurb, description, log):
        self.name = name
        self.status = status
        self.manager = manager
        self.teams = teams
        self.blurb = blurb
        self.description = description
        self.log = log

class Task(db.Model):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    status = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    deadline = db.Column(db.Text, nullable=False)

    def __init__(self, project, status, content, deadline):
        self.project = project
        self.status = status
        self.content = content
        self.deadline = deadline

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer,db.ForeignKey('user.id'))
    projid = db.Column(db.Integer,db.ForeignKey('project.id'))
    taskid = db.Column(db.Integer,db.ForeignKey('task.id'))

    UniqueConstraint(userid,projid,taskid)

    user = db.relationship('User', foreign_keys=[userid])
    project = db.relationship('Project', foreign_keys=[projid])
    task = db.relationship('Task', foreign_keys=[taskid])

    def __init__(self, userid, projid, taskid):
        self.userid = userid
        self.projid = projid
        self.taskid = taskid

class Employment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projid = db.Column(db.ForeignKey('project.id'))
    userid = db.Column(db.ForeignKey('user.id'))
    team = db.Column(db.Integer)

    UniqueConstraint(projid,userid)

    project = db.relationship('Project', foreign_keys=[projid])
    user = db.relationship('User', foreign_keys=[userid])

    def __init__(self, projid, userid):
        self.projid = projid
        self.userid = userid
        self.team = None
