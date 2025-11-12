from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Category, Task, db


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# Home page - display all tasks
@tasks_bp.route('/')
def home():
    task_list = Task.query.all()
    categories = Category.query.all()
    return render_template('tasks/index.html', tasks=task_list, categories=categories)


# Add a new task
@tasks_bp.route("/add_task", methods=['POST'])
def add_task():
    task_title = request.form.get('title', "").strip()
    due_date_str = request.form.get('due_date', "")
    category_id = request.form.get("category_id", "")

    if not task_title or len(task_title) > 200:
        flash("Le titre d'une tache ne peut etre vide ou plus long que 200 caractères", "error")
        return redirect(url_for("tasks.home"))
    
    due_date = None
    if due_date_str:
        due_date = datetime.fromisoformat(due_date_str)

    if category_id:
        category_id = int(category_id)

    task = Task(title=task_title, due_date=due_date, category_id=category_id)
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


# Categories home page
@tasks_bp.route("/categories")
def categories():
    categories = Category.query.all()

    return render_template("tasks/categories.html", categories=categories)


# Add a category
@tasks_bp.route("/add_category", methods=['POST'])
def add_category():
    name = request.form.get("name", "").strip()
    color = request.form.get("color", "")

    if not name or len(name) > 20:
        flash("Le nom ne peut etre vide ou supérieure à 20 caractères.", "error")
        return(url_for("tasks.categories"))
    
    category = Category(name=name, color=color)
    db.session.add(category)
    db.session.commit()
    flash("Catégorie ajoutée avec succès !", "success")

    return redirect(url_for("tasks.categories"))


# Delete a category
@tasks_bp.route("/delete_category/<int:category_id>")
def delete_category(category_id):
    category = Category.query.get(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
        flash("Category supprimée avec succès !", "success")

    return redirect(url_for("tasks.categories"))