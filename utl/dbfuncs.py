from flask import *
from models import db, User, Invites, Project, Task, Assignment, Employment

def get_user(**kwargs):
    return User.query.filter_by(username=kwargs['uname']).first()

def get_project(**kwargs):
    return Project.query.filter_by(name=kwargs['uname']).first()

def get_user_project(**kwargs):
    return Employment.query.filter_by(userid=kwargs['uid']).all()

def verify_user(**kwargs):
    print(kwargs)
    check_user = User.query.filter_by(username=kwargs['uname']).first()

    if (check_user == None):
        flash("Username does not exist",'danger')
        return False

    if (check_user.password == kwargs['password']):
        print("LOG IN")
        return True
    else:
        flash("Username and password combination not found",'danger')
        return False

def edit_token(**kwargs):
    kwargs['user'].token = kwargs['new_token']
    db.session.commit()
    return

def fetch_token(user):
    return user.tokentype

def add_user(**kwargs):
    new_user = User(kwargs['uname'], kwargs['password'], None)
    db.session.add(new_user)
    db.session.commit()
    return

def change_password(**kwargs):
    if (kwargs['user'].password == kwargs['old_password']):
        kwargs['user'].password = kwargs['new_password']
        print(kwargs['user'].password)
        flash("Successfully changed password",'success')
        db.session.commit()
        return True
    else:
        flash("Incorrect password",'danger')
        return False

def get_invites(**kwargs):
    return Invites.query.filter_by(user=kwargs['user'].id).all()

def add_invite(**kwargs):
    new_invite = Invite(kwargs['project'].id, kwargs['user'].id, None)
    db.session.add(new_invite)
    db.session.commit()
    return

def accept_invite(**kwargs):
    i = Invites.query.filter_by(user=kwargs['user'].id,project=kwargs['project'].id).first()
    i.status = 0;
    join_project(user=uname, project=p)
    db.session.commit()
    return

def decline_invite(**kwargs):
    i = Invites.query.filter_by(user=kwargs['user'].id,project=kwargs['project'].id).first()
    i.status = -1;
    db.session.commit()
    return

def join_project(**kwargs):
    employ = Employment(kwargs['user'].id, kwargs['project'].id)
    db.seesion.add(employ)
    db.session.commit()
    return

def add_project(**kwargs):
    check_pname = Project.query.filter_by(name=kwargs['pname']).first()
    if(check_pname == None):
        new_project = Project(kwargs['pname'], 0, kwargs['manager'], kwargs['teams'], kwargs['blurb'], kwargs['description'], kwargs['log'])
        db.session.add(new_project)
        db.session.commit(project=new_project.id,user=kwargs['manager'])
        # join_project()
        return 1
    return 0

def change_manager(**kwargs):
    proj = Project.query.filter_by(name=kwargs['pname']).first()
    new_manager = User.query.filter_by(name=kwargs['mname']).first()
    proj.manager = new_manager.id
    db.session.commit()
    return

def complete_project(**kwargs):
    proj = Project.query.filter_by(name=kwargs['pname']).first()
    proj.status = 1
    db.session.commit()
    return

def abandon_project(**kwargs):
    proj = Project.query.filter_by(name=kwargs['pname']).first()
    proj.status = -1
    db.session.commit()
    return

def get_tasks(**kwargs):
    return Assignment.query.filter_by(project=kwargs['pid'])

def add_task(**kwargs):
    proj = Project.query.filter_by(name=kwargs['pname']).first()
    new_task = Task(proj.id, kwargs['status'], kwargs['content'], kwargs['deadline'])
    db.session.add(new_task)

    user = User.query.filter_by(name=kwargs['uname']).first()
    new_assignment = Assignment(user.id, proj.id, new_task.id)
    db.session.add(new_assignment)

    db.session.commit()
    return new_task.id

def edit_task(**kwargs):
    t = Task.query.filter_by(id=kwargs['tid'])
    if (kwargs['content'] != ''):
        t.content = kwargs['content']
    if (kwargs['deadline'] != ''):
        t.deadline = kwargs['deadline']
    db.session.commit()
    return

def complete_task(**kwargs):
    proj = Project.query.filter_by(name=kwargs['pname']).first()
    task = Task.query.filter_by(projid=proj.id).first()
    task.status = 1
    db.session.commit()
    return

def delete_task(**kwargs):
    proj = Project.query.filter_by(name=kwargs['pname']).first()
    task = Task.query.filter_by(projid=proj.id).first()
    db.session.delete(task)
    db.session.commit()
    return
