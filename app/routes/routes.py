from flask import render_template, flash, redirect, url_for, request
from app.forms.forms import RegistrationForm, LoginForm
from app import app, db, bcrypt
from app.models.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


posts = [
    {
        'author': 'Amer Ahmed',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'published': '2021-01-19'
    },
    {
        'author': 'Amir Ramic',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'published': '2021-01-19'
    }
]


@app.route("/")
def index():
    return render_template('index.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hash_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now  able to sign in', 'success')
        return redirect(url_for('signin'))
    return render_template('signup.html', form=form)


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Your authentication is failed. Please check email or password and try again!', 'danger')
    return render_template('signin.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/account')
@login_required
def account():
    profiles = url_for('static', filename='profile_pics/' + current_user.profile)
    return render_template('account.html', profile=profiles)


@app.errorhandler(404)
def page_not_found(_error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(_error):
    return render_template('500.html'), 500
