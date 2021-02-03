from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from PIL import Image
from flaskapp.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'  # to tell where to look for login view in account logged in check
login_manager.login_message_category = 'info'
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)  # everything except the flask extensions
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskapp.main.routes import main
    from flaskapp.users.routes import users
    from flaskapp.jobs.routes import jobs
    from flaskapp.profiles.routes import profiles
    from flaskapp.errors.handlers import errors


    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(jobs)
    app.register_blueprint(profiles)
    app.register_blueprint(errors)
    

    return app


from flaskapp.main.utils import DefaultImgToThumb
# DefaultImgToThumb((125, 125))


