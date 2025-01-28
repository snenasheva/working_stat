from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from . import chief_bp


@chief_bp.route('/dashboard')
@login_required
def chief_dashboard():
    if current_user.role != "Chief":
        flash('You need to log in')
        redirect(url_for('main.login'))
    return render_template('dashboard_chief.html')

