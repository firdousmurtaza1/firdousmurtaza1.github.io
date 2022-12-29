from app.extensions import login_manager
from flask import redirect, flash, url_for, request


def load_user(user_id):
    if user_id:
        from accounts.models import User
        return User.query.filter(User.is_active==True, User.id == user_id).first()
    return None


def get_system_user():
    from accounts.models import User
    return User.get_system_user()


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash(r'You must be logged in to view that page.', category='danger')
    return redirect(url_for(r'account.login', next=request.referrer))
