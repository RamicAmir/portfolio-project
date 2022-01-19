from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

posts = [
    {
        'author': 'Amer Ahmed',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': '2021-01-19'
    },
    {
        'author': 'Amir Ramic',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': '2021-01-19'
    }
]


@app.route("/")
def index():
    return render_template('index.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html')


@app.errorhandler(404)
def page_not_found(_error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(_error):
    return render_template('500.html'), 500
