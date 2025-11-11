from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Task, db


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# Home page - display all tasks
@tasks_bp.route('/')
def home():
    task_list = Task.query.all()
    return render_template('tasks/index.html', tasks=task_list)


# Add a new task
@tasks_bp.route("/add_task", methods=['POST'])
def add_task():
    task_title = request.form.get('title', "").strip()
    if not task_title or len(task_title) > 200:
        flash("Le titre d'une tache ne peut etre vide ou plus long que 200 caractères", "error")
        return redirect(url_for("tasks.home"))
    
    task = Task(title=task_title)
    db.session.add(task)
    db.session.commit()
    flash("Tache ajouté avec succès !", "success")

    return redirect(url_for("tasks.home"))


# Mark a task as complete
@tasks_bp.route("/mark_task_complete/<int:task_id>")
def mark_task_complete(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = not task.completed
        db.session.commit()
        flash("Tache mise à jour !", "success")

    return redirect(url_for("tasks.home"))


# Delete a task
@tasks_bp.route("/delete_task/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        flash("Tache supprimée avec succès !", "success")

    return redirect(url_for("tasks.home"))
###
