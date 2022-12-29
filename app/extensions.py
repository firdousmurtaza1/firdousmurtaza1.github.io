from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect 
# from app.core.file_storage import FileStorage
 

login_manager = LoginManager()
db = SQLAlchemy()
# file_storage = FileStorage()
csrf = CSRFProtect()
# db.create_all()


__all__ = ['db','csrf','login_manager','file_storage' ]