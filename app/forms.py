import os
import pathlib
import secrets
from turtle import title
from PIL import Image
import time
import cv2
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, StringField,ValidationError, TextAreaField
from wtforms.validators import Regexp, DataRequired, Email, EqualTo, Length
from app.extensions import db
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask import current_app as app
from .models import Post

class PostForm(FlaskForm):
    title = StringField(r'Title',validators=[DataRequired(),Length(max=100,min=5)])
   
    content = TextAreaField(r'Content', validators=[DataRequired(), Length(max=10000, min=10)])
    img_data = FileField(
        r'Image', validators=[FileAllowed(['jpg', 'png', 'gif','jpeg'])])
    submit=SubmitField('Submit')
    # FileAllowed(photos, 'Image only!')

    # def save_file(self, uploaded_file, path, file_name_alias=None):
   
    #     if not pathlib.Path(path).exists():
    #         pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    #     new_file_name = file_name_alias if file_name_alias else uploaded_file.filename
    #  
    #     uploaded_file.save(os.path.join(path, new_file_name))
    #     return self

    def save_image(self, photo):
        hash_photo = secrets.token_urlsafe(10)
        path = app.config['FILES_STORAGE']
        if not pathlib.Path(path).exists():
                 pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        _,file_extension = os.path.splitext(photo.filename)
        photo_name= hash_photo + file_extension
        file_path=os.path.join(path, photo_name)
        Image.open(photo).save(file_path)
        return photo_name

    def save(self, user_id):
        
        # file_name_lst = self.img_data.data.filename.rsplit('.', 1)
      
        # file_name_lst.insert(1, '_%s.' % str(time.strftime(r'%Y%m%d-%H%M%S')))
        # filename_on_server = ''.join(file_name_lst)
        # self.save_file(self.img_data.data, os.path.join(app.config['FILES_STORAGE'], filename_on_server))
        # url=os.path.join(os.path.join(app.config['FILES_STORAGE'], filename_on_server),self.img_data.data.filename)
        # self.img_data(os.path.join(app.config['FILES_STORAGE'], filename_on_server))
        image_id = None
        file_path = None
        if self.img_data.data:
            image_id = self.save_image(self.img_data.data)
            file_path = os.path.join(app.config['FILES_STORAGE'], image_id)
            
       
            # _image_resize(url,photo_name,600,'lg')
            _image_resize(app.config['FILES_STORAGE'], image_id,300,'sm')

 
        data = {
            # "file_name":self.img_data.data.filename,
        "user_id":user_id,
        "title":self.title.data,
        "content":self.content.data,
      
        # "img_data":self.img_data.data.read(),
        "file_alias_name":image_id,
        "url":file_path,
       
       
        }
       
                                    
        Post.create_upload_file(**data)
        

        return self


# def _image_resize(original_file_path,image_id, image_base, extension):
#     name, ext= image_id.rsplit('.', 1)
#     file_path = os.path.join(
#                 original_file_path, image_id)
#     image = Image.open(file_path)
#     wpercent = (image_base/float(image.size[0]))
#     hsize = int((float( image.size[1] )* float( wpercent )))
#     image = image.resize((image_base,hsize), Image.ANTIALIAS)
#     modified_image_path= os.path.join(
#                 original_file_path, name +'.'+ extension +'.jpg')
#     image.save(modified_image_path)
#     return 

def _image_resize(original_file_path, image_id, image_base, extension):
    name, ext = os.path.splitext(image_id)
    file_path = os.path.join(original_file_path, image_id)

    # Reading the image using OpenCV
    image = cv2.imread(file_path)

    # Calculating the new dimensions to maintain aspect ratio
    aspect_ratio = image_base / float(image.shape[1])
    new_height = int(image.shape[0] * aspect_ratio)

    # Resizing the image using OpenCV
    resized_image = cv2.resize(image, (image_base, new_height))

    # Constructing the modified image path
    modified_image_path = os.path.join(original_file_path, f"{name}.{extension}.jpg")

    # Saving the modified image
    cv2.imwrite(modified_image_path, resized_image)


class EditPostForm(FlaskForm):
    title = StringField(r'Title',validators=[DataRequired(),Length(max=100,min=5)])
   
    content = TextAreaField(r'Content', validators=[DataRequired(), Length(max=10000, min=10)])
    img_data = FileField(
        r'Image', validators=[FileAllowed(['jpg', 'png', 'gif','jpeg'])])
    submit=SubmitField('Submit')

    def update_image(self, photo):
        hash_photo = secrets.token_urlsafe(10)
        path = app.config['FILES_STORAGE']
        if not pathlib.Path(path).exists():
                    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        _,file_extension = os.path.splitext(photo.filename)
        photo_name= hash_photo + ".jpg"
        file_path=os.path.join(path, photo_name)
        Image.open(photo).save(file_path)
        return photo_name

    def update(self, user_id, post_id):
      
        query = Post.query.filter(Post.id == post_id).first()
   
        image_id = None
        file_path = None
        if self.img_data.data:
            path = app.config['FILES_STORAGE']
            if os.path.exists(path):
                filename = path + "\\" + query.img_filename
            
                os.remove(filename+".jpg")
                os.remove(filename+".sm.jpg")
           
            image_id = self.update_image(self.img_data.data)
            
            file_path = os.path.join(app.config['FILES_STORAGE'], image_id)
            
     
            # _image_resize(url,photo_name,600,'lg')
            _image_resize(app.config['FILES_STORAGE'], image_id,300,'sm')

     
       
        query.id = post_id
        query.title  = self.title.data
        query.content = self.content.data
        if self.img_data.data:
            name, ext= image_id.rsplit('.', 1)
            query.img_filename = name
        query.date = db.func.now()
        query.user_id = current_user.id
        db.session.commit()

        return self