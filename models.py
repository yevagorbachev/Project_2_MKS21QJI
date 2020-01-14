from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()

class User(db.Model):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    token = db.Column(db.String(80))


    def __init__(self, username, password, tokentype):
        self.username = username
        self.password = password

class Project(db.Model):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    manager = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    teams = db.Column(db.String(80))
    blurb = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    log = db.Column(db.String(80))
    calendarid = db.Column(db.Integer)

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
    status = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(80), nullable=False)
    deadline = db.Column(db.String(80), nullable=False)

    def __init__(self, status, content, deadline):
        self.projid = projid
        self.status = status
        self.content = content
        self.deadline = deadline

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.ForeignKey('user.id'))
    projid = db.Column(db.ForeignKey('project.id'))
    taskid = db.Column(db.ForeignKey('task.id'))

    UniqueConstraint(userid,projid,taskid)

    user = db.relationship('User', foreign_keys=[userid])
    project = db.relationship('Project', foreign_keys=[projid])
    task = db.relationship('Task', foreign_keys=[taskid])

    def __init__(self, user, project, task):
        self.user = user
        self.project = project
        self.task = task

class Employment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projid = db.Column(db.ForeignKey('project.id'))
    userid = db.Column(db.ForeignKey('user.id'))
    team = db.Column(db.Integer)

    UniqueConstraint(projid,userid)

    project = db.relationship('Project', foreign_keys=[projid])
    user = db.relationship('User', foreign_keys=[userid])

    def __init__(self, project, user, team):
        self.project = project
        self.user = user
        self.team = team
