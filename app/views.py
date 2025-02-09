from flask import render_template, redirect, url_for
from app import bcrypt, db
from wtforms import SelectField, PasswordField
from app.models import User, Employee
from flask_admin import AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
import json
from datetime import datetime

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
    column_list = ['username', 'role', 'email', 'employees']

    def on_model_change(self, form, model, is_created):
        if form.password_hash.data:
            model.password_hash = bcrypt.generate_password_hash(form.password_hash.data).decode('utf-8')
        super().on_model_change(form, model, is_created)


class DashBoardView(AdminIndexView):
    @expose('/')
    def add_db_data(self):
        all_users = User.query.all()  # feel free to change the function upon your needs
        return self.render('dashboard_index.html', all_users=all_users)

    def is_accessible(self):
        if not current_user.is_authenticated:
            return False

        return current_user.has_role('Admin') or current_user.has_role('Manager')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))


class ManagerView(ModelView):
    form_columns = ['employee']


# what you see after clicking 'Employee' in the dashboard and rules for Create Employee form:
class EmployeeModelView(ModelView):

    form_overrides = {'department': SelectField}
    form_args = {
        'department': {'choices': DEPARTMENTS, 'label': 'Choose department'}
    }

    column_list = ['id', 'name', 'last_name', 'country', 'office', 'department', 'exception', 'hours_month',
                   'office_visits', 'added_by', 'date_added']

    form_readonly_columns = ['added_by_id']

    form_excluded_columns = ['added_by']

    column_formatters = {
        'added_by': lambda v, c, m, p: m.added_by.username if m.added_by else 'Unknown'
    }

    def on_model_change(self, form, model, is_created):
        if is_created and not model.added_by_id:
            model.added_by_id = current_user.id
        super().on_model_change(form, model, is_created)


#class ImportEmployeesView(BaseView):
   # @expose('/')
   # def import_page(self):
   #     return render_template('some_page.html')
#
   # def is_accessible(self):
   #     if not current_user.is_authenticated:
   #         return False
   #     return current_user.has_role('Admin') or current_user.has_role('Manager')
#
   # json_file = 'MOCK_DATA.json'
#
   # user = User.query(id=current_user.id).first()
#
   # with open(json_file, 'r', encoding='utf-8') as file:
   #     employees_data = json.load(file)
#
   # for entry in employees_data:
   #     new_employee = Employee(
   #         name=entry['first_name'],
   #         last_name=entry['last_name'],
   #         country=entry['country'],
   #         office=['office'],
   #         department=['India'],
   #         exception=False,
   #         hours_month=entry['hours/month'],
   #         office_visits=entry['office visits'],
   #         added_by_id=user.id,
   #         date_added=datetime.utcnow()
   #     )
#
   #     db.session.add(new_employee)
   #     try:
   #         db.session.commit()
   #         print("Employees imported successfully!")
   #     except Exception as e:
   #         db.session.rollback()
   #         print(f'Error importing employees: {e}')
