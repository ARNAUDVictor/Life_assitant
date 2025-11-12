from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(7), default="#667eea")

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

    def __repr__(self):
        return f'<Task {self.title}>'
    

    #calculates if the task is overdue
    def is_overdue(self):
        if not self.due_date or self.completed:
            return False
        return datetime.now() > self.due_date
    

    @staticmethod
    def validate_input(title, due_date_str):
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
        