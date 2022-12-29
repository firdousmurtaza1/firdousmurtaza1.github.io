from functools import wraps
from datetime import datetime
from flask import flash, redirect, url_for, request
from flask_login import current_user


def user_is_anonymous(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
           
            return redirect(url_for('home.post_world'))
        return func(*args, **kwargs)
    return decorated_function