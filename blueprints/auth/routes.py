from flask import Blueprint


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Login page
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    pass


# registration page
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    pass


@auth_bp.route("/logout",)
def logout():
    pass