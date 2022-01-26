from flask import Flask, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from app.forms.forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'afd1849122d53a3cb9aea6af5b0b7a1625961faa1dd73f1c156d9573363ab268'
bootstrap = Bootstrap(app)

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Your Account have been Created!{form.username.data} Now you are able to signin', 'success')
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have logged in', 'success')
            return redirect(url_for('index'))
        else:
            flash('login Unsuccessful or failed. Please check email and password ', 'danger')
    return render_template('signin.html', form=form)


@app.errorhandler(404)
def page_not_found(_error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(_error):
    return render_template('500.html'), 500
