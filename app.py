import json
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update

app = Flask(__name__)

###############Database Configuration####################

# SQLite configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db = SQLAlchemy(app)

###############Database Model#######################

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.title}>'
##################Routes#######################

# Home page - display tasks
@app.route('/')
def home():
    task_list = get_tasks()
    return render_template('index.html', tasks=task_list)


# Add a new task
@app.route("/add_task", methods=['POST'])
def add_task():
    task = Task(title = request.form.get('title'))
    save_tasks(task)

    return redirect(url_for("home"))


# Mark a task as complete
@app.route("/mark_task_complete/<int:task_id>")
def mark_task_complete(task_id):
    print("task_index :", task_id)
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
#get tasks from json file
def get_tasks():
    return Task.query.all()

#save tasks to json file
def save_tasks(task):
    db.session.add(task)
    db.session.commit()

########################Run the app########################
if __name__ == '__main__':
    app.run(debug=True)