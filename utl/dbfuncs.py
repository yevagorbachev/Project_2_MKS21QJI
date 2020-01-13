from flask import *
from models import db, User, Project, Task, Assignment, Employment


def verify_user(username, password):
    check_user = User.query.filter_by(username=user).first()

    if (check_user == None):
        flash("Username does not exist")
        return False

    if (check_user.password == password):
        return True
    else:
        flash("Username and password combination not found")
        return False

def edit_token(user,token):
    user.tokentype = token
    return

def fetch_token(user):
    return user.tokentype

def add_user(username, password):
    new_user = User(username, password)
    db.session.add(new_user)
    db.session.commit()
    return

def change_password(user, old_password, new_password):
    if (user.password == old_password):
        user.password = new_password
        flash("Successfully changed password")
        return True
    else:
        flash("Incorrect password")
        return False

def join_project(user, project):
    employ = Employment(user, project, 0)
    db.seesion.add(emplo)
    db.session.commit()
    return

def add_project(pname, manager, teams, blurb, description, log):
    check_pname = Project.query.filter_by(name=pname).first()
    if(check_pname != None):
        new_project = Project(pname, 0, manager, teams, blurb, description, log)
        db.session.add(new_project)
        db.session.commit()
        return 1
    return 0

def change_manager(pname, mname):
    proj = Project.query.filter_by(name=pname).first()
    new_manager = User.query.filter_by(name=mname).first()
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

def add_task(pname, uname, status, content, deadline):
    proj = Project.query.filter_by(name=pname).first()
    new_task = Task(proj.id, status, content, deadline)
    db.session.add(new_task)

    user = User.query.filter_by(name=uname).first()
    new_assignment = Assignment(user.id, proj.id, new_task.id)
    db.session.add(new_assignment)

    db.session.commit()
    return

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
