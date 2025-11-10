from flask import Flask, redirect, render_template, request, url_for
from models import db, Task
from config import Config

app = Flask(__name__)

###############Database Configuration####################

# Initialize the database
db.init_app(app)


##################Routes#######################

# Home page - display tasks
@app.route('/')
def home():
    task_list = Task.query.all()

    return render_template('index.html', tasks=task_list)


# Add a new task
@app.route("/add_task", methods=['POST'])
def add_task():
    task = Task(title=request.form.get('title'))
    db.session.add(task)
    db.session.commit()

    return redirect(url_for("home"))


# Mark a task as complete
@app.route("/mark_task_complete/<int:task_id>")
def mark_task_complete(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = not task.completed
        db.session.commit()

    return redirect(url_for("home"))


# Delete a task
@app.route("/delete_task/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()

    return redirect(url_for("home"))

################Helper Functions####################



########################Run the app########################
if __name__ == '__main__':
    app.run(debug=True)