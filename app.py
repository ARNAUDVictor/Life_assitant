from flask import Flask, redirect, url_for
from models import db
from config import Config
from blueprints.tasks import tasks_bp
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

# Route d'accueil (redirige vers /tasks/)
@app.route('/')
def index():
    return redirect(url_for('tasks.home'))

########################Run the app########################
if __name__ == '__main__':
    app.run(debug=True)