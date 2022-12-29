import os 
from flask import Blueprint, send_from_directory
from flask import flash, redirect, render_template, url_for, request
from flask import current_app as app
from app.extensions import db

from flask_login import current_user
from .forms import EditPostForm, PostForm

from . models import Post
home = Blueprint(r'home', __name__)


@home.route("/")
def post_world():
    page = request.args.get('page', 1, type=int)
    post = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=10)
    # files = os.listdir(app.config['FILES_STORAGE'])
    return render_template('post/posthome.html', post=post)

# @home.route('/<filename>')
# def display_image(filename):

#     return redirect(url_for('static', filename='\img'+filename))

@home.route('/<filename>')
def display_image(filename):
  
    path = app.config['FILES_STORAGE']
    return send_from_directory(path, filename+".sm.jpg")


@home.route(r'/posts', methods=['GET','POST'])
def post():
    form = PostForm()

    if current_user.is_authenticated:
        if form.validate_on_submit():
            form.save(current_user.id)
            return redirect(url_for('home.post_world'))
        else:
            flash(r'Invalid field.', category=r'danger')
        return render_template('post/post.html', form=form,)
    
    return redirect(url_for('account.login'))

@home.route(r'/delete/<int:id>/', methods=[r'GET'])
def delete_post(id):
    query = Post.query.filter(Post.id == id).first()
    if query.img_filename:
        path = app.config['FILES_STORAGE']
        if os.path.exists(path):
            filename = path + "\\" + query.img_filename
       
            os.remove(filename+".jpg")
            os.remove(filename+".sm.jpg")
    db.session.query(Post).filter(Post.id==id).\
                            delete(synchronize_session="fetch")
    db.session.commit()
    return redirect(request.referrer)

@home.route(r'/post/edit/<int:id>/', methods=[r'GET',r'POST'])
def edit_post(id):
    query = Post.query.filter(Post.id == id).first()
    path = app.config['FILES_STORAGE']
    form = EditPostForm(title=query.title, content =query.content)
    if current_user.is_authenticated:
        if form.validate_on_submit():
            form.update(current_user.id,id)
            return redirect(url_for('home.post_world'))
        else:
            flash(r'Invalid field.', category=r'danger')
        return render_template('post/editpost.html', form=form,)
    
    return redirect(url_for('account.login'))


