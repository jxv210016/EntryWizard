from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .routes import main as main_blueprint  # Ensure this import is correct

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Tell Flask to use the /instance folder for configuration
    app.config.from_object('instance.config.Config')  # if config class is named Config
    # OR use the below line to load the instance config.py without class
    # app.config.from_pyfile('config.py', silent=True) 

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
