import os
from flask import Flask, render_template, request, flash, Blueprint

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.config['TREX_files'] = 'extension_app/static/trex/'
    from . import db
    db.init_app(app)

    from . import auth
    from . import ext
    from . import site
    app.register_blueprint(auth.bp)
    app.register_blueprint(ext.bp)
    app.register_blueprint(site.bp)

    # load the instance config, if it exists, when not testing
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.errorhandler(404)
    def not_found(error):
        error_message = 'This page cannot be found. Did you specify a proper url?'
        return render_template('site/error.html', error_message=error_message), 404
    return app