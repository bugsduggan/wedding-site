from functools import wraps

from flask import current_app, flash, redirect, url_for
from flask.ext.login import current_user


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif not current_user.is_admin():
            flash('You don\'t have permission to do that', 'danger')
            return redirect(url_for('frontend.index'))
        return func(*args, **kwargs)
    return decorated_view
