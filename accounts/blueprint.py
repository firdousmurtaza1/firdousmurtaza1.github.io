import os
from flask import Blueprint

TEMPLATE_DIR = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), 'templates')
account_blueprint = Blueprint(
    'account', 'account', template_folder=TEMPLATE_DIR)
