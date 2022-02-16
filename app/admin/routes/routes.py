"""
The module for Admin Routes.
Amer Ahmed
Amir Ramic
Supervisor: Joakim Wassberg
Version 0.0
"""

from flask import render_template, request, Blueprint
from app.models.models.models import Post


admin = Blueprint('admin', __name__)


@admin.route('/')
def index():
    # Home page
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.published.desc()).paginate(page=page, per_page=5)
    return render_template('index.html', posts=posts)


@admin.route("/about")
def about():
    # About page
    return render_template('about.html')


@admin.route('/contact')
def contact():
    # Contact page
    return render_template('contact.html')


@admin.route('/projects')
def projects():
    # Projects for applications
    return render_template('profile/projects.html')


@admin.route('/resume')
def resume():
    # User resume
    return render_template('profile/resume.html')
