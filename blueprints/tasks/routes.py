from flask import Blueprint, render_template, request, redirect, url_for
from models import Task, db


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# Home page - display all tasks
@tasks_bp.route('/')
def home():
    task_list = Task.query.all()
    return render_template('templates/tasks/index.html', tasks=task_list)


# Add a new task
@tasks_bp.route("/add_task", methods=['POST'])
def add_task():
    task = Task(title=request.form.get('title'))
    db.session.add(task)
    db.session.commit()

    return redirect(url_for("tasks.home"))


# Mark a task as complete
@tasks_bp.route("/mark_task_complete/<int:task_id>")
def mark_task_complete(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = not task.completed
        db.session.commit()

    return redirect(url_for("tasks.home"))


# Delete a task
@tasks_bp.route("/delete_task/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()

    return redirect(url_for("tasks.home"))
###
