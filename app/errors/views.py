from flask import render_template
from . import errors

@errors.error_handler(404)
def page_not_found(e):
    return render_template('errors/404.html')