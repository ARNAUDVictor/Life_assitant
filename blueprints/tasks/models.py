from datetime import datetime
from models import db

class Category(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(7), default="#667eea")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", backref="categories")

    def __repr__(self):
        return f"<Category {self.name}>"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    due_date = db.Column(db.DateTime, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=True)
    category = db.relationship("Category", backref="tasks")
    priority = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", backref="tasks")
    parent_id = db.Column(db.Integer, db.ForeignKey("task.id", ondelete="CASCADE", name="fk_task_parent"), nullable=True)
    subtasks = db.relationship('Task',
                                backref=db.backref('parent', remote_side='Task.id'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Task {self.title}>'
    

    #calculates if the task is overdue
    def is_overdue(self):
        if not self.due_date or self.completed:
            return False
        return datetime.now() > self.due_date
    

    # validates task input
    @staticmethod
    def validate_input(title, due_date_str,):
        errors = []
        if not title or len(title) > 200:
            errors.append("Le titre d'une tache ne peut etre vide ou plus long que 200 caractères")

        if due_date_str:
            try:
                due_date = datetime.fromisoformat(due_date_str)
                if due_date < datetime.now():
                    errors.append("La date d'échéance ne peut pas être dans le passé.")
            except ValueError:
                errors.append("Format de date invalide.")

        return errors

    # processes task input
    @staticmethod
    def parse_form_data(due_date_str, category_id_str):
        data = {}
        due_date = None
        if due_date_str:
             due_date = datetime.fromisoformat(due_date_str)
        data["due_date"] = due_date

        category_id = None
        if category_id_str:
            try:
                category_id = int(category_id_str)
            except ValueError:
                category_id = None
        data["category_id"] = category_id

        return data
    

    # returns the level of the task in the hierarchy
    def get_level(self):

        level = 0
        current = self
        while current.parent:
            level += 1
            current = current.parent
        return level


    # checks if the task can have subtasks (max 2 levels)
    def can_have_subtasks(self):
        return self.get_level() < 2