import re
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user
from sqlalchemy import exists
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Login page
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    pass


# registration page
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password =request.form.get("password", "")
        pseudo = request.form.get("pseudo", "")

        errors = User.validate_register(email, password, pseudo)
        if errors:
            for error in errors:
                flash(error, "error")
            return redirect(url_for("auth.register"))
        
        # créer l'user et l'ajouter a la DB
        hashed_password = generate_password_hash(password)
        user = User(email=email, password=hashed_password, pseudo=pseudo)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash("Erreur lors de la création du compte", "error")
            return redirect(url_for("auth.register"))
        
        flash("Compte créé avec succès !", "success")
        login_user(user)
        return redirect(url_for("tasks.home"))
    
    # GET request
    return render_template("auth/register.html")


@auth_bp.route("/logout",)
def logout():
    pass