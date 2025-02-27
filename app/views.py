from flask import render_template, redirect, url_for, flash, Response, request
from app import bcrypt, db
from wtforms import SelectField, PasswordField
from app.models import User, Employee
from flask_admin import AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import io
from markupsafe import Markup

ROLES = [
    ('Admin', 'Admin'),
    ('Manager', 'Manager'),
    ('Chief Department', 'Chief Department'),
    ('Local', 'Local Manager')
]

DEPARTMENTS = [
    ('Beer Sheva Engineering', 'Beer Sheva Engineering'),
    ('Beer Sheva Development', 'Beer Sheva Development'),
    ('Beer Sheva Marketing', 'Beer Sheva Marketing'),
    ('Petah Tikva Engineering', 'Petah Tikva Engineering'),
    ('Petah Tikva Development', 'Petah Tikva Development'),
    ('Petah Tikva Marketing', 'Petah Tikva Marketing'),
    ('Jaipur Development', 'Jaipur Development')
]


class CustomPageView(BaseView):
    @expose('/')
    def custom_page(self):
        return render_template('some_page.html')


# What you see after clicking 'User' in the dashboard and rules for Create user form
class UserModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role("Admin")

    def inaccessible_callback(self, name, **kwargs):
        flash('You should be logged in')
        return redirect(url_for('main.index'))

    form_overrides = {
        'role': SelectField,
        'department': SelectField
    }
    form_extra_fields = {
        'password_hash': PasswordField('Password', render_kw={'autocomplete': 'new-password'})
    }
    form_args = {
        'role': {'choices': ROLES, 'label': 'User Role'},
        'department': {'choices': DEPARTMENTS, 'label': 'User Department'}
    }
    form_create_rules = [
        'username',
        'email',
        'role',
        'department',
        'password_hash',
        'created_at'
    ]
    column_list = ['username', 'role', 'email', 'department']

    def on_model_change(self, form, model, is_created):
        if form.password_hash.data:
            model.password_hash = bcrypt.generate_password_hash(form.password_hash.data).decode('utf-8')
        super().on_model_change(form, model, is_created)


class DashBoardView(AdminIndexView):
    @expose('/')
    def add_db_data(self):
        all_users = User.query.all()  # Feel free to change the function upon your needs
        return self.render('dashboard_index.html', all_users=all_users)

    def is_accessible(self):
        if not current_user.is_authenticated:
            flash('You should be logged in')
            return False

        return current_user.has_role('Admin') or current_user.has_role('Manager')

    def inaccessible_callback(self, name, **kwargs):
        flash('You should be logged in')
        return redirect(url_for('main.login'))


def clickable_formatter(view, context, model, name):
    target_url = url_for(f'.employee_stat', id=model.id)
    value = getattr(model, name)
    return Markup(f'<a href="{target_url}" target="_blank">{value}</a>')


# What you see after clicking 'Employee' in the dashboard and rules for Create Employee form
class EmployeeModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role("Admin")

    form_overrides = {'department': SelectField}
    form_args = {
        'department': {'choices': DEPARTMENTS, 'label': 'Choose department'}
    }

    column_list = ['id', 'name', 'last_name', 'country', 'office', 'department', 'exception', 'hours_month',
                   'office_visits', 'added_by']

    form_excluded_columns = ['added_by']

    column_formatters = {
        'added_by': lambda v, c, m, p: m.added_by.username if m.added_by else 'Unknown',
        'name': clickable_formatter,
        'last_name': clickable_formatter
    }

    def on_model_change(self, form, model, is_created):
        if is_created and not model.added_by_id:
            model.added_by_id = current_user.id
        super().on_model_change(form, model, is_created)

    @expose('/employee_stat')
    def employee_stat(self):
        employee_id = request.args.get('id')
        employee = Employee.query.get(employee_id)
        if not employee:
            return self.render('individual_stat.html', error="Employee not found")
        return self.render('individual_stat.html', employee=employee)


class LocalManagerView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('Manager')

    def inaccessible_callback(self, name, **kwargs):
        flash('You should be logged in')
        return redirect(url_for('main.login'))

    def get_query(self):
        return super().get_query().filter(Employee.department == current_user.department)

    column_list = [
        'name', 'last_name', 'country', 'office', 'department', 'exception', 'hours_month', 'office_visits'
    ]

    form_excluded_columns = ['added_by']

