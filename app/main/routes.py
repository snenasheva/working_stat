from flask import render_template, flash, redirect, url_for, Response
from . import main_bp
from .forms import LoginForm
from app.models import User, Employee
from flask_login import login_user, logout_user, current_user
import json
from datetime import datetime
from app.manager.routes import manager_dashboard
from app import db


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in', category='info')
        return role_redirect()

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_login_psw(form.password.data):
            login_user(user, remember=True)
            flash('You have been logged in', category='success')
            return redirect(url_for('admin.index'))
        else:
            flash('Invalid name or password. Please, try again', category='danger')

    return render_template('login.html', form=form)


ROLES_REDIRECTS = {
    'Admin': 'admin.index',
    'Manager': 'admin.index',
    'Chief Department': 'chief.chief_dashboard'
}


def role_redirect():
    endpoint = ROLES_REDIRECTS.get(current_user.role)
    if endpoint:
        return redirect(url_for(endpoint))
    else:
        flash(f'No dashboard available for the role: {current_user.role}', category='danger')
        return redirect(url_for('main.index'))
    #if current_user.role == "Manager":
    #    return redirect(url_for('manager.manager_dashboard'))
    #if current_user.role == "Chief":
    #    return redirect(url_for('chief.chief_dashboard'))


@main_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', category='info')
    return redirect(url_for('main.index'))


@main_bp.route('/dashboard_admin')
def dashboard_admin():
    return render_template('dashboard_index.html')


@main_bp.route('/bulk_import', methods=["POST"])
def bulk_import():
    json_file = 'MOCK_DATA.json'

    user = User.query.filter_by(id=current_user.id).first()

    with open(json_file, 'r', encoding='utf-8') as file:
        employees_data = json.load(file)

    for entry in employees_data:
        new_employee = Employee(
            name=entry['first_name'],
            last_name=entry['last_name'],
            country=entry['country'],
            office=entry['office'],
            department='Engineering',
            exception=False,
            hours_month=entry['hours/month'],
            office_visits=entry['office visits'],
            added_by_id=user.id,
            date_added=datetime.utcnow()
        )

        db.session.add(new_employee)
        try:
            db.session.commit()
            print("Employees imported successfully!")
        except Exception as e:
            db.session.rollback()
            print(f'Error importing employees: {e}')

    flash('The import finished successfully')
    return redirect(url_for('admin.index'))



