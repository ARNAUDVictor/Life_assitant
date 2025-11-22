import re
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from sqlalchemy import exists
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Login page
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or "@" not in email:
            flash("L'email n'est pas valide", "error")
            return redirect(url_for("auth.login"))
        if not password:
            flash("Veuillez entrez votre mot de passe.", "error")
            return redirect(url_for("auth.login"))
        
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Email ou mot de passe incorrect", "error")
            return redirect(url_for("auth.login"))
        if not check_password_hash(user.password, password):
            flash("Email ou mot de passe incorrect", "error")
            return redirect(url_for("auth.login"))
 
        login_user(user)
        flash(f"Connexion réussie, bienvenue {user.pseudo} !", "success")
        return redirect(url_for("tasks.home"))

    # request method GET    
    return render_template("auth/login.html")

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


# logout method
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Vous avez été déconnecté.", "success")
    return redirect(url_for("auth.login"))