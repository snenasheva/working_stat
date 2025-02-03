from flask import render_template, flash, redirect, url_for
from . import main_bp
from .forms import LoginForm
from app.models import User
from flask_login import login_user, logout_user, current_user
from app.manager.routes import manager_dashboard
from app.decorators import admin_required

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
            login_user(user)
            flash('You have been logged in', category='success')
            return role_redirect()
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
@admin_required
def dashboard_admin():
    pass
