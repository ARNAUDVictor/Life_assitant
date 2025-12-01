from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from models import Category, Task, db


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# Home page - display all tasks
@tasks_bp.route('/')
@login_required
def home():
    sort_by = request.args.get('sort_by', 'due_date')
    categories_filter = request.args.get('category', None)

    if categories_filter:
        categories_filter = int(categories_filter)
        
        task_list = Task.query.filter_by(category_id=categories_filter, user_id=current_user.id).order_by(getattr(Task, sort_by).desc()).all()
    else:
        task_list = Task.query.filter_by(user_id=current_user.id).order_by(getattr(Task, sort_by).desc()).all()

    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('tasks/index.html', tasks=task_list, categories=categories, datetime=datetime)


################################### TASKS

# Add a new task
@tasks_bp.route("/add_task", methods=['POST'])
@login_required
def add_task():
    task_title = request.form.get('title', "").strip()
    due_date_str = request.form.get('due_date', "")
    category_id_str = request.form.get("category_id", "")

    errors = Task.validate_input(task_title, due_date_str)
    if errors:
        for error in errors:
            flash(error, "error")
        return redirect(url_for("tasks.home"))
    
    processed_data = Task.parse_form_data(due_date_str, category_id_str)
    print("processed_data : ", processed_data)
    task = Task(title=task_title, 
                due_date=processed_data["due_date"], 
                category_id=processed_data["category_id"], 
                user_id=current_user.id)
    
    db.session.add(task)
    db.session.commit()
    flash("Tache ajouté avec succès !", "success")

    return redirect(url_for("tasks.home"))


# Mark a task as complete
@tasks_bp.route("/mark_task_complete/<int:task_id>")
@login_required
def mark_task_complete(task_id):
    task = Task.query.get(task_id)
    if task and task.user_id == current_user.id:
        task.completed = not task.completed
        db.session.commit()
        flash("Tache mise à jour !", "success")

    return redirect(url_for("tasks.home"))


# Delete a task
@tasks_bp.route("/delete_task/<int:task_id>")
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task and task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
        flash("Tache supprimée avec succès !", "success")

    return redirect(url_for("tasks.home"))


# Edit a task
@tasks_bp.route("/edit_task/<int:task_id>", methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return redirect(url_for("tasks.home"))
    
    if request.method == 'POST':
        task_title = request.form.get('title', "").strip()
        due_date_str = request.form.get('due_date', "")
        category_id_str = request.form.get("category_id", "")
        errors = Task.validate_input(task_title, due_date_str)

        if errors:
            for error in errors:
                flash(error, "error")
            return redirect(url_for("tasks.edit_task", task_id=task.id))
            
        processed_data = Task.parse_form_data(due_date_str, category_id_str)

        task.title = task_title
        task.due_date = processed_data["due_date"]
        task.category_id = processed_data["category_id"]
        db.session.commit()
        flash("Tache mise à jour avec succès !", "success")
        return redirect(url_for("tasks.home"))
    
    # GET : afficher le formulaire
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('tasks/edit.html', task=task, categories=categories, datetime=datetime)


#####################################   Sub-task

# Add a sub-task
@tasks_bp.route("/add_subtask/<int:task_id>", methods=["POST"])
@login_required
def add_subtask(task_id):
    parent_task = Task.query.get_or_404(task_id)
    if parent_task.user_id != current_user.id:
        return redirect(url_for("tasks.home"))
    
    if not parent_task.can_have_subtasks():
        flash("Cette tache ne peut pas avoir du sous-taches", "error")
        return redirect(url_for("tasks.home"))
    
    task_title = request.form.get('title', "").strip()
    due_date_str = request.form.get('due_date', "")
    category_id_str = request.form.get("category_id", "")
    errors = Task.validate_input(task_title, due_date_str)

    if errors:
        for error in errors:
            flash(error, "error")
        return redirect(url_for("tasks.home"))
            
    processed_input = Task.parse_form_data(due_date_str, category_id_str)

    subtask = Task(title = task_title,
                    due_date = processed_input["due_date"],
                    category_id = processed_input["category_id"],
                    parent_id = parent_task.id,
                    user_id = current_user.id,
                    )
    
    db.session.add(subtask)
    db.session.commit()
    flash("Sous-tâche ajoutée avec succès !", "success")
    return redirect(url_for("tasks.home"))


#####################################   Category

# Categories home page
@tasks_bp.route("/categories")
@login_required
def categories():
    categories = Category.query.filter_by(user_id=current_user.id).all()

    return render_template("tasks/categories.html", categories=categories)


# Add a category
@tasks_bp.route("/add_category", methods=['POST'])
@login_required
def add_category():
    name = request.form.get("name", "").strip()
    color = request.form.get("color", "")

    if not name or len(name) > 20:
        flash("Le nom ne peut etre vide ou supérieure à 20 caractères.", "error")
        return(url_for("tasks.categories"))
    
    category = Category(name=name, color=color, user_id=current_user.id)
    db.session.add(category)
    db.session.commit()
    flash("Catégorie ajoutée avec succès !", "success")

    return redirect(url_for("tasks.categories"))


# Delete a category
@tasks_bp.route("/delete_category/<int:category_id>")
@login_required
def delete_category(category_id):
    category = Category.query.get(category_id)
    if category and category.user_id == current_user.id:
        db.session.delete(category)
        db.session.commit()
        flash("Category supprimée avec succès !", "success")

    return redirect(url_for("tasks.categories"))