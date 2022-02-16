"""
The module for User Routes.
Amer Ahmed
Amir Ramic
Supervisor: Joakim Wassberg
Version 0.0.1
"""

from flask import render_template, url_for, Blueprint
from flask import request, flash, redirect
from flask_login import login_user, logout_user
from flask_login import current_user, login_required
from app.users.forms.forms import RegistrationForm, LoginForm, UpdateAccountForm
from app.users.forms.forms import RequestResetForm, ResetPasswordForm, SearchForm
from app.users.utils.utils import save_picture, send_reset_email
from app.models.models.models import User, Post
from app import db, bcrypt

users = Blueprint('users', __name__)


@users.route("/signup", methods=['GET', 'POST'])
def signup():
    # User can sign up
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hash_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now  able to sign in', 'success')
        return redirect(url_for('users.signin'))
    return render_template('auth/signup.html', form=form)


@users.route("/signin", methods=['GET', 'POST'])
def signin():
    # User can sign in
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin.index'))
        else:
            flash('Your authentication is failed. Please check email or password and try again!', 'danger')
    return render_template('auth/signin.html', form=form)


@users.route('/logout')
def logout():
    # User can log out
    logout_user()
    return redirect(url_for('admin.index'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    # User account with auth
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account has been Updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profiles = url_for('static', filename='profile_pics/' + current_user.profile)
    return render_template('auth/account.html', profile=profiles, form=form)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    # User reset_request
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instruction to reset your password.', 'info')
        return redirect(url_for('users.signin'))
    return render_template('auth/reset_request.html', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    # User verify token reset
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token.', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hash_pw
        db.session.commit()
        flash('Your password has been updated.', 'success')
        return redirect(url_for('users.signin'))
    return render_template('auth/reset_token.html', form=form)


@users.route('/user/<string:username>')
def user_posts(username):
    # User_posts
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username). first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.published.desc())\
        .paginate(page=page, per_page=5)
    return render_template('posts/user_posts.html', posts=posts, user=user)


@users.route('/search', methods=['GET', 'POST'])
@login_required
def search_posts():
    # User can search posts
    form = SearchForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        flash('Your search has been found', 'success')
        return redirect(url_for('admin.index'))
    return render_template('posts/search_posts.html', form=form, legend='Search Posts')
