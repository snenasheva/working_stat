from flask import Flask, render_template
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    from app.models import User, Employee

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # ===BLUEPRINTS HERE===

    from app.main import main_bp
    app.register_blueprint(main_bp)

    #from app.manager import manager_bp
    #app.register_blueprint(manager_bp, url_prefix='/manager')

    from app.chief import chief_bp
    app.register_blueprint(chief_bp, url_prefix='/chief')

    from app.views import UserModelView, CustomPageView, DashBoardView, ManagerView, EmployeeModelView

    admin = Admin(app, name='Working Statistics', template_mode='bootstrap4', index_view=DashBoardView())
    admin.add_view(UserModelView(User, db.session, endpoint='user'))
    admin.add_view(EmployeeModelView(Employee, db.session, 'employee'))
    admin.add_view(CustomPageView(name='Custom Page', endpoint='custom_page'))

    return app




