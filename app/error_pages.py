from flask import current_app as app
from flask import request, render_template


def page_not_found(e):
    app.logger.info(f"Page not found: {request.url}")
    app.logger.error(e)
    return render_template("error_handlers/404.html"), 404


def access_forbidden(e):
    app.logger.error(f"Forbidden error: {request.url}")
    app.logger.error(e)
    return render_template("error_handlers/403.html"), 403


def server_error(e):
    app.logger.error(f"Server error: {request.url}")
    app.logger.error(e)
    return render_template("error_handlers/500.html"), 500
