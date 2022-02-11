"""
The module for Posts Routes.
Amer Ahmed
Amir Ramic
Supervisor: Joakim Wassberg
Version 0.0
"""

from flask import render_template, abort, Blueprint
from flask import flash, redirect, url_for, request
from flask_login import current_user, login_required
from app.posts.forms.forms import PostForm
from app.models.models.models import Post
from app import db


posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def create_posts():
    # User can create posts
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('admin.index'))
    return render_template('posts/create_posts.html', form=form, legend='New Post')


@posts.route('/post/<int:post_id>')
def post(post_id):
    # User id
    post = Post.query.get_or_404(post_id)
    return render_template('posts/post.html', post=post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_posts(post_id):
    # User can update posts
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('posts/create_posts.html', form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_posts(post_id):
    # User can delete posts
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('admin.index'))
