from flask import render_template, Blueprint

errors = Blueprint('errors', __name__)


@errors.errorhandler(404)
def page_not_found(_error):
    return render_template('errors/404.html'), 404


@errors.errorhandler(500)
def internal_server_error(_error):
    return render_template('errors/500.html'), 500