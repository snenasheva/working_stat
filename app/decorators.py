from flask import session, redirect, url_for, abort
from functools import wraps
from flask_login import current_user
from app.models import User


def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        user = User.query.get(user_id)

        if not user or not user.is_admin:
            abort(403)

        return func(*args, **kwargs)

    return decorated_function


