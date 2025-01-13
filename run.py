from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_admin import Admin, BaseView, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from wtforms import SelectField

app = Flask(__name__)
app.config['FLASK_ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///work_hours.db'
app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    role = db.Column(db.String, nullable=False)  # Admin, Manager, etc.
    email = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    employees = db.relationship('Employee', backref='added_by', lazy=True)

    def __repr__(self):
        return f'{self.username}'


class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    exclusion = db.Column(db.Boolean, default=False)
    added_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.name} {self.surname}'


ROLES = [
    ('Admin', 'Admin'),
    ('Manager', 'Manager'),
    ('Chief Department', 'Chief Department'),
]

DEPARTMENTS = [
    ('Engineering', 'Engineering'),
    ('Development', 'Development'),
    ('Marketing', 'Marketing')
]


class UserModelView(ModelView):
    form_overrides = {'role': SelectField}
    form_args = {
        'role': {'choices': ROLES, 'label': 'User Role'}
    }


#class ManagerModelView(ModelView):
#    def is_accessible(self):
#        current_user = get_current_user()
#        return current_user.role == 'Manager'


class CustomPageView(BaseView):
    @expose('/')
    def custom_page(self):
        return render_template('some_page.html')


# to display some data on the page with AdminDashboard view:
class DashBoardView(AdminIndexView):
    @expose('/')
    def add_db_data(self):
        all_users = User.query.all()  # feel free to change the function upon your needs
        return self.render('dashboard_index.html', all_users=all_users)


admin = Admin(app, name='Working Statistics', template_mode='bootstrap4', index_view=DashBoardView())
# admin.add_view(ModelView(User, db.session, name='user'))
admin.add_view(UserModelView(User, db.session, endpoint='user'))
admin.add_view(ModelView(Employee, db.session, 'employee'))
admin.add_view(CustomPageView(name='Custom Page', endpoint='custom_page'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)

