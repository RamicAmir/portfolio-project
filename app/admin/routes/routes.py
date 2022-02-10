from flask import render_template, request, Blueprint
from app.models.models import Post


admin = Blueprint('admin', __name__)


@admin.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.published.desc()).paginate(page=page, per_page=2)
    return render_template('index.html', posts=posts)


@admin.route("/about")
def about():
    return render_template('about.html')


@admin.route('/contact')
def contact():
    return render_template('contact.html')


@admin.route('/projects')
def projects():
    return render_template('profile/projects.html')


@admin.route('/resume')
def resume():
    return render_template('profile/resume.html')
