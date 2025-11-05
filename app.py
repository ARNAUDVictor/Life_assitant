import json
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


##################Routes#######################

# Home page - display tasks
@app.route('/')
def home():
    task_list = get_tasks()
    return render_template('index.html', tasks=task_list)

# Add a new task
@app.route("/add_task", methods=['POST'])
def add_task():
    task = {"title" : request.form.get('title'),
            "completed": False}
    tasks_list = get_tasks() 
    tasks_list.append(task) 
    save_tasks(tasks_list)

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
    try:
        with open('data/tasks.json', 'r') as f:
            tasks_list = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks_list = []
    return tasks_list

#save tasks to json file
def save_tasks(tasks_list):
    with open('data/tasks.json', 'w') as f:
        json.dump(tasks_list, f)

########################Run the app########################
if __name__ == '__main__':
    app.run(debug=True)