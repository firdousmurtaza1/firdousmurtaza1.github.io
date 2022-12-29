from sqlalchemy.schema import UniqueConstraint
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import cached_property
from app.extensions import db, login_manager
# from app.auth import Permission


class User(db.Model, UserMixin):
    # __tablename__ = r'GuiUser'
    USER_TYPE_NORMAL = 1
    USER_TYPE_ADMIN = 2

    USER_TYPES = (
        (USER_TYPE_ADMIN, r'Admin'),
        (USER_TYPE_NORMAL, r'ART-User'),
    )

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255, collation='NOCASE'),
                      nullable=False, unique=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60),  server_default=r'')
    is_active = db.Column(db.Boolean(),
                          nullable=True, server_default='1', default=False)
    password_hash = db.Column(db.String(
        255), nullable=True, server_default='')
    last_login = db.Column(db.DateTime)
    type = db.Column(db.Integer, nullable=True,
                     default=1, server_default='1')
    create_date = db.Column(db.DateTime, default=db.func.now())
    

    post = db.relationship(
        r'Post', backref='user', lazy=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __repr__(self):
        """Object representation menthod"""
        return r"<User : {}>".format(self.email)

    @property
    def user_type(self):
        return [user[1] for user in User.USER_TYPES if user[0] == self.type][0]

    @property
    def display_name(self):
        if self.first_name or self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)
        return self.email.split('@')[0]

    @property
    def is_superuser(self):
        return self.type == User.USER_TYPE_ADMIN

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    #@cached_property
    
   
  

    def activate_user(self):
        self.is_active = True
        db.session.add(self)
        db.session.commit()
        return self

    def deactivate_user(self):
        self.is_active = False
        db.session.add(self)
        db.session.commit()
        return self

    def update_last_login(self):
        self.last_login = db.func.now()
        db.session.add(self)
        db.session.commit()
        return self

    @staticmethod
    def get_system_user():
        return User.query.filter(User.type == User.USER_TYPE_NORMAL).first()

    @property
    def is_editable(self):
        return self.type == User.USER_TYPE_NORMAL


    def get_change_password_hash(self):
        from app.core.security import generate_key, encrypt_string
        enc_key  = generate_key()
        return {
            'email_hash' :encrypt_string(self.email,enc_key),
            'hash_token':enc_key.decode('utf-8')
        } 


