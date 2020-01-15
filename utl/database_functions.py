from models.py import db, User, Project, Task, Assignment, Employment

def add_user(username, password):
    new_user = User(username, password)
    db.session.add(new_user)
    db.session.commit()
    return

def add_project(name, manager, teams, blurb, description, log):
    new_project = Project(name, 0, manager, teams, blurb, description, log)
    db.session.add(new_project)
    db.session.commit()
    return

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
