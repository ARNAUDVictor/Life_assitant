import json
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

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
@app.route("/mark_task_complete/<int:task_index>")
def mark_task_complete(task_index):
    print("Marking task as complete:", task_index)
    task_list = get_tasks()
    if 0 <= task_index < len(task_list):
        task_list[task_index]['completed'] = not task_list[task_index]['completed']
        save_tasks(task_list)
    return redirect(url_for("home"))

# Delete a task
@app.route("/delete_task/<int:task_index>")
def delete_task(task_index):
    task_list = get_tasks()
    if 0 <= task_index < len(task_list):
        task_list.pop(task_index)
        save_tasks(task_list)
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