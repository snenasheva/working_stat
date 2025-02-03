from . import manager_bp
from flask_login import login_required, current_user
from flask import redirect, url_for, render_template, flash


@manager_bp.route('/dashboard')
@login_required
def manager_dashboard():
    if current_user.role != 'Manager':
        flash('You need to log in')
        redirect(url_for('main.login'))
    return render_template('dashboard_manager.html')



