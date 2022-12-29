from flask import Flask
from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
from app.extensions import db
from app.core.decorators import user_is_anonymous
from .forms import LoginForm, RegistrationForm, ChangePasswordForm
from .models import User
from .blueprint import account_blueprint
import secrets
HOME_PAGE=r'home.homepage'

@account_blueprint.route(r'/login', methods=[r'POST',])
@account_blueprint.route(r'/login', methods=[r'GET',])
@user_is_anonymous
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = form.validate_user()
        if user and login_user(user):
            
            user.update_last_login()
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('home.post_world' ,next=(request.referrer) + secrets.token_urlsafe()))
            # return redirect(url_for('home.post_world'))
        else:
            flash(r'Invalid email or password.', category=r'danger')
    return render_template(r'auth/login.html', form=form, title=r'Login')



@account_blueprint.route(r'/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    return redirect(url_for(r'account.login'))

@account_blueprint.route(r'/register', methods=[r'POST',])
@account_blueprint.route(r'/register', methods=[r'GET',])
def register():
    """
    Handle requests to the /register route
    Register an employee through the register link
    """
    form = RegistrationForm()
   
    if form.validate_on_submit():
        form.save_form()
        flash('User updated successfully.',category='success')
        return redirect(url_for('account.login'))
    return render_template(r'auth/register.html', form=form, current_link=r'users', title=r'Edit User')


@account_blueprint.route(r'/change-password', methods=[r'GET', r'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        form.save(current_user)
        flash(r'Password has been updated!', r'success')
        return redirect(url_for('home.post_world', next = secrets.token_urlsafe()))
    return render_template(r'auth/change_password.html', title=r'Change Password', form=form)
    