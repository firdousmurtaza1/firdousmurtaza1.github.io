import os
from datetime import datetime
from tkinter import image_names
from app.extensions import db
from hashlib import md5
from flask import current_app as app, send_from_directory


class Post(db.Model):


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    content=db.Column(db.String(200),nullable=False)
    date= db.Column(db.DateTime, default=db.func.now())
    img_filename = db.Column(db.String(50), nullable=True)
    # img_data = db.Column(db.LargeBinary,  nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_path = db.Column(db.String, nullable=True)
    # user = db.relationship(r'User', innerjoin=True)

    
    def __str__(self):
        return "{} {}".format(self.user_id, self.title)

    def __repr__(self):
        """Object representation menthod"""
        return r"<Post : {}>".format(self.id)

    @staticmethod
    def create_upload_file(**data):
        if data.get('file_alias_name') is not None:
            name,ext = data.get('file_alias_name').rsplit('.', 1)
            filename_on_server =name 
        else:
            filename_on_server = data.get('file_alias_name')
       

        post_upload = Post(title=data.get('title'),
                            user_id=data.get('user_id'),
                            content = data.get('content'),
            
                            img_filename = filename_on_server,
                            # img_data = data.get('img_data'),
                                file_path = data.get('file_path'),     
                                     )

        db.session.add(post_upload)
        db.session.commit()
        return post_upload

        