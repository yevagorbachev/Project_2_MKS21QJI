from flask import *
from models import db, User, Project, Task, Assignment, Employment

def get_user(uname):
    return User.query.filter_by(username=uname).first()

def get_project(pname):
    return Project.query.filter_by(name=pname).first()

def verify_user(**kwargs):
    print(kwargs)
    check_user = User.query.filter_by(username=kwargs['user']).first()

    if (check_user == None):
        flash("Username does not exist")
        return False

    if (check_user.password == kwargs['password']):
        print("LOG IN")
        return True
    else:
        flash("Username and password combination not found")
        return False

def edit_token(**kwargs):
    kwargs['user'].token = kwargs['new_token']
    return

def fetch_token(user):
    return user.tokentype

def add_user(**kwargs):
    new_user = User(kwargs['user'], kwargs['password'], None)
    db.session.add(new_user)
    db.session.commit()
    return

def change_password(**kwargs):
    if (kwargs['user'].password == kwargs['old_password']):
        kwargs['user'].password = kwargs['new_password']
        flash("Successfully changed password")
        return True
    else:
        flash("Incorrect password")
        return False

def get_invites(**kwargs):
    return Invites.query.filter_by(user=kwargs['user'].id).all()

def add_invite(**kwargs):
    new_invite = User(kwargs['project'], kwargs['user'], None)
    db.session.add(new_invite)
    db.session.commit()
    return

def accept_invite(uname, project):
    p = get_project(project)
    i = Invites.query.filter_by(user=uname.id,project=project.id).first()
    i.status = 0;
    join_project(user=uname, project=p)
    return

def decline_invite(user, project):
    p = get_project(project)
    i = Invites.query.filter_by(user=user.id,project=project.id).first()
    i.status = -1;
    return

def join_project(**kwargs):
    employ = Employment(kwargs['user'].id, kwargs['project'].id)
    db.seesion.add(employ)
    db.session.commit()
    return

def add_project(**kwargs):
    check_pname = Project.query.filter_by(name=pname).first()
    if(check_pname != None):
        new_project = Project(kwargs['pname'], 0, kwargs['manager'], kwargs['teams'], kwargs['blurb'], kwargs['description'], kwargs['log'])
        db.session.add(new_project)
        db.session.commit()
        return 1
    return 0

def change_manager(**kwargs):
    proj = Project.query.filter_by(name=kwargs['pname']).first()
    new_manager = User.query.filter_by(name=kwargs['mname']).first()
    proj.manager = new_manager.id
    return

def complete_project(pname):
    proj = Project.query.filter_by(name=pname).first()
    proj.status = 1
    return

def abandon_project(pname):
    proj = Project.query.filter_by(name=pname).first()
    proj.status = -1
    return

def get_tasks(pid):
    return Assignment.query.filter_by(project=pid)

def add_task(**kwargs):
    proj = Project.query.filter_by(name=kwargs['pname']).first()
    new_task = Task(proj.id, kwargs['status'], kwargs['content'], kwargs['deadline'])
    db.session.add(new_task)

    user = User.query.filter_by(name=kwargs['uname']).first()
    new_assignment = Assignment(user.id, proj.id, new_task.id)
    db.session.add(new_assignment)

    db.session.commit()
    return

def edit_task(**kwargs):
    t = Task.query.filter_by(id=kwargs['task'])
    if (kwargs['content'] != ''):
        t.content = kwargs['content']
    if (kwargs['deadline'] != ''):
        t.deadline = kwargs['deadline']

def complete_task(pname):
    proj = Project.query.filter_by(name=pname).first()
    task = Task.query.filter_by(projid=proj.id).first()
    task.status = 1
    return

def delete_task(pname):
    proj = Project.query.filter_by(name=pname).first()
    task = Task.query.filter_by(projid=proj.id).first()
    db.session.delete(task)
    return
