from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from ProfilerApp.config import Config
from flask_mail import Mail


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
  
    from ProfilerApp.users.routes import users
    from ProfilerApp.posts.routes import posts
    from ProfilerApp.profiles.routes import profile
    from ProfilerApp.admin.routes import admin
    #from ProfilerApp.main.routes import main
    from ProfilerApp.api.routes import api
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(profile)
    app.register_blueprint(admin)
    #app.register_blueprint(main)
    app.register_blueprint(api)

    return app