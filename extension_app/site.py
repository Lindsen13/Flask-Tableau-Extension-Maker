import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from extension_app.db import get_db

bp = Blueprint('site', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    return render_template('site/index.html')

@bp.route('/contact', methods=['GET'])
def contact():
    return render_template('site/contact.html')

@bp.route('/about', methods=['GET'])
def about():
    return render_template('site/about.html')

#Temp route to track if the button is working.
@bp.route('traffic', methods=['GET'])
def traffic():
    traffic_all = get_db().execute('SELECT * FROM executed_extensions').fetchall()
    return render_template('temp.html', traffic_all=traffic_all)