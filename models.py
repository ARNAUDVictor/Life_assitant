from datetime import datetime
import re
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<User {self.pseudo}>"
    
    @staticmethod
    def validate_register(email, password, pseudo):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        errors = []
        
        if not re.match(pattern, email):
            errors.append("Email non valide")

        if User.query.filter_by(email=email).first():
            errors.append("Un compte existe déja avec cet email.")

        if len(password) < 4:
            errors.append("Le mot de passe doit faire au moins 4 caractères.")

        if not pseudo:
            errors.append("Veuillez choisir un pseudo")
            
        if User.query.filter_by(pseudo=pseudo).first():
            errors.append("Ce pseudo est déja utilisé.")

        return errors    
            