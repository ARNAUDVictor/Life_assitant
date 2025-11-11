from flask import Flask
from models import db
from config import Config
from blueprints.tasks import tasks_bp

#app creation
app = Flask(__name__)

# Load configuration from Config class
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Register blueprints
app.register_blueprint(tasks_bp)


########################Run the app########################
if __name__ == '__main__':
    app.run(debug=True)