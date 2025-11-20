from flask import Flask, redirect, url_for
from flask_login import LoginManager
from models import User, db
from config import Config
from blueprints.tasks import tasks_bp
from blueprints.auth import auth_bp
from flask_migrate import Migrate

# App creation
app = Flask(__name__)

# Load configuration from Config class
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Register blueprints
app.register_blueprint(tasks_bp)
app.register_blueprint(auth_bp)


# Initialize Flask-Login
login_manager = LoginManager(app)
# Set the login view for unauthorized users
login_manager.login_view = "auth.login"

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Route d'accueil (redirige vers /tasks/)
@app.route('/')
def index():
    return redirect(url_for('tasks.home'))

########################Run the app########################
if __name__ == '__main__':
    app.run(debug=True)