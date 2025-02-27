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

    from app.chief import chief_bp
    app.register_blueprint(chief_bp, url_prefix='/chief')

    from app.views import UserModelView, CustomPageView, DashBoardView, EmployeeModelView, LocalManagerView
    from mpl_view import PlotView

    admin = Admin(app, name='Working Statistics', template_mode='bootstrap4', index_view=DashBoardView())
    admin.add_view(UserModelView(User, db.session, endpoint='user'))
    admin.add_view(EmployeeModelView(Employee, db.session, endpoint='employee'))
    admin.add_view(CustomPageView(name='Import Data', endpoint='custom_page'))
    admin.add_view(PlotView(name='Stat Plots', endpoint='plot_view'))
    admin.add_view(LocalManagerView(Employee, db.session, name='My Team', endpoint='local_manager'))

    return app




