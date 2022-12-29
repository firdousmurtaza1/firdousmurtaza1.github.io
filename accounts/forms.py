from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError,BooleanField
from wtforms.validators import Regexp, DataRequired, Email, EqualTo, Length
from app.extensions import db
from .models import User

class RegistrationForm(FlaskForm):
    email = StringField(r'Email', validators=[DataRequired(
        message=r'Please enter valid email address.'), Email(message=r'Please enter valid email address.')])
    first_name = StringField('First Name', validators=[
                             DataRequired(message=r'First name is required'), Length(min=3)])
    last_name = StringField(r'Last Name', validators=[])
    password = PasswordField(r'Password', description=r'Password must have atleast 6 characters(i.e. only letters numbers or underscore).', validators=[
        DataRequired(message=r'Password is required'), Length(
            min=6, message=r'Password must have atleast 6 characters.'),
        Regexp(
            r'^\w+$', message=r"Password must contain only letters numbers or underscore")
    ])
    confirm_password = PasswordField(r'Confirm Password')
   
    submit = SubmitField('Register')

    def validate_confirm_password(self, field):
        if not self.password.errors and self.password.data != self.confirm_password.data:
            raise ValidationError(
                r'Confirm password didn\'t match with password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(r'Given email address is not available.')

    def save_form(self):
      
        user = User(email=self.email.data,
                    first_name=self.first_name.data,
                    last_name=self.last_name.data,)
        user.set_password(self.password.data)
        user.activate_user()
        db.session.add(user)
        db.session.commit()
       
        return user

class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('Email', validators=[
                        DataRequired(r'Please enter your email address.'), Email(r'Please enter valid email address.')])
    password = PasswordField('Password', validators=[
                             DataRequired(r'Password cannot be blank.')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_user(self):
    
        user = User.query.filter_by(email=self.email.data).first()
        if user and user.check_password(self.password.data):
           
            return user
        return False



class ChangePasswordForm(FlaskForm):
    password = PasswordField(r'New Password', description=r'Password must have atleast 6 characters(i.e. only letters numbers or underscore).', validators=[
        DataRequired(message=r'Password is required'), Length(
            min=6, message=r'Password must have atleast 6 characters.'),
        Regexp(
            r'^\w+$', message=r"Password must contain only letters numbers or underscore")
    ])
    confirm_password = PasswordField(r'Confirm Password')
    submit = SubmitField('Register')

    def validate_confirm_password(self, field):
        if not self.password.errors and self.password.data != self.confirm_password.data:
            raise ValidationError(
                r'Confirm password didn\'t match with password')

    def save(self, user):
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

