from flask import render_template, redirect, url_for, flash
from app import bcrypt
from wtforms import SelectField, PasswordField
from app.models import User, Employee
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

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


class CustomPageView(BaseView):
    @expose('/')
    def custom_page(self):
        return render_template('some_page.html')


class UserModelView(ModelView):  # what you see after clicking 'User' in the dashboard and rules for Create user form
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role("Admin")

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index'))

    form_overrides = {'role': SelectField}
    form_extra_fields = {
        'password_hash': PasswordField('Password', render_kw={'autocomplete': 'new-password'})
    }
    form_args = {
        'role': {'choices': ROLES, 'label': 'User Role'}
    }
    form_create_rules = [
        'username',
        'role',
        'email',
        'password_hash',
        'created_at'
    ]
    column_list = ['username', 'role', 'email']

    def on_model_change(self, form, model, is_created):
        if form.password_hash.data:
            model.password_hash = bcrypt.generate_password_hash(form.password_hash.data).decode('utf-8')
        super().on_model_change(form, model, is_created)


# to display some data on the page with AdminDashboard view:
class DashBoardView(AdminIndexView):
    @expose('/')
    def add_db_data(self):
        all_users = User.query.all()  # feel free to change the function upon your needs
        return self.render('dashboard_index.html', all_users=all_users)


class ManagerView(ModelView):
    form_columns = ['employee']


# what you see after clicking 'Employee' in the dashboard and rules for Create Employee form:
class EmployeeModelView(ModelView):
    form_overrides = {'department': SelectField}
    form_args = {
        'department': {'choices': DEPARTMENTS, 'label': 'Choose department'}
    }
