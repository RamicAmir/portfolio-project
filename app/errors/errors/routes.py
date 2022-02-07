from flask import render_template, Blueprint

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def errors_404(e):
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def errors_403(e):
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def errors_500(e):
    return render_template('errors/500.html'), 500

