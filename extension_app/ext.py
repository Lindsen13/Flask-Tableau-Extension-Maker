import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, send_from_directory, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from extension_app.auth import login_required
from extension_app.db import get_db
from . import extension_maker
bp = Blueprint('ext', __name__, url_prefix='/extension')

@bp.route('/')
@login_required
def extensions():
    all_extensions = get_extensions()
    return render_template('ext/extensions.html', all_extensions=all_extensions)
"""
@bp.route('/<int:id>/info', methods=('GET',))
@login_required
def extension_by_id(id):
    extension = get_extension(id)
    if extension:
        extension_log = get_extension_log(id)
    return render_template('ext/extension_by_id.html', extension=extension, extension_log=extension_log)
"""

@bp.route('/<int:id>/info', methods=('GET', 'POST'))
@login_required
def extension_by_id(id):
    extension = get_extension(id)
    extension_log = get_extension_log(id)
    return render_template('ext/extension_by_id.html', extension=extension, extension_log=extension_log)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        url = request.form['url']
        headers = request.form['headers']
        payload = request.form['payload']
        background_colour = request.form['background_colour']
        image = request.form['image']
        error = None

        if not title:
            error = 'Title is required.'
        if not description:
            error = 'Description is required.'
        if not url:
            error = 'Url is required.'

        if error is not None:
            flash(error, 'error')
        else:
            db = get_db()
            db.execute(
                'INSERT INTO extensions (ext_title, ext_description, ext_url, ext_headers, ext_payload, ext_background_colour, ext_image, author_id)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (title, description, url, headers, payload, background_colour, image, g.user['id'])
            )
            last_input = get_db().execute(
                'SELECT id from extensions WHERE ext_title = ? and author_id = ? ORDER BY created DESC',
                (title, g.user['id'],)
            ).fetchone()
            db.execute(
                'INSERT INTO executed_extensions (author_id, extension_id, comment)'
                ' VALUES (?, ?, ?)',
                (g.user['id'], last_input['id'], 'Extension added to database')
            )
            db.commit()
            return redirect(url_for('ext.extensions'))

    return render_template('ext/create.html')

def get_extension(id, check_author=True):
    extension = get_db().execute(
        'SELECT e.id, ext_title, ext_description, ext_url, ext_headers, ext_payload, ext_background_colour, ext_image, created, author_id, username'
        ' FROM extensions e JOIN user u ON e.author_id = u.id'
        ' WHERE e.id = ?',
        (id,)
    ).fetchone()

    if extension is None:
        abort(404, "Extension id {0} doesn't exist.".format(id))

    if check_author and extension['author_id'] != g.user['id']:
        abort(403)

    return extension

def get_extension_log(id, check_author=True):
    extension_log = get_db().execute(
        'SELECT * FROM executed_extensions WHERE extension_id = ?',
        (id,)
    ).fetchall()

    if extension_log is None:
        abort(404, "Extension id {0} doesn't exist.".format(id))

    for log in extension_log:
        if check_author and log['author_id'] != g.user['id']:
            abort(403)

    return extension_log

def get_extensions(check_author=True):
    all_extensions = get_db().execute(
        'SELECT e.id, ext_title, ext_description, ext_url, ext_headers, ext_payload, ext_background_colour, ext_image, created, author_id, username'
        ' FROM extensions e JOIN user u ON e.author_id = u.id'
        ' WHERE e.author_id = ?',
        (g.user['id'],)
    ).fetchall()
    return all_extensions

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    extension = get_extension(id)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        url = request.form['url']
        headers = request.form['headers']
        payload = request.form['payload']
        background_colour = request.form['background_colour']
        image = request.form['image']
        error = None

        if not title:
            error = 'Title is required.'
        if not description:
            error = 'Description is required.'
        if not url:
            error = 'Url is required.'

        if error is not None:
            flash(error, 'error')
        else:
            db = get_db()
            db.execute(
                'UPDATE extensions SET ext_title = ?, ext_description = ?, ext_url = ?, ext_headers = ?, ext_payload = ?, '
                'ext_background_colour = ?, ext_image = ? WHERE id = ?',
                (title, description, url, headers, payload, background_colour, image, id)
            )
            db.commit()
            db.execute(
                'INSERT INTO executed_extensions (author_id, extension_id, comment)'
                ' VALUES (?, ?, ?)',
                (g.user['id'], id, 'Extension updated')
            )
            db.commit()
            return redirect(url_for('ext.extensions'))

    return render_template('ext/update.html', extension=extension)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_extension(id)
    db = get_db()
    db.execute('DELETE FROM extensions WHERE id = ?', (id,))
    db.commit()
    db.execute(
        'INSERT INTO executed_extensions (author_id, extension_id, comment)'
        ' VALUES (?, ?, ?)',
        (g.user['id'], id, 'Extension deleted')
    )
    db.commit()
    return redirect(url_for('ext.extensions'))

@bp.route('/<int:id>/tableau_extension', methods=('GET', 'POST'))
@login_required
def tableau_extension(id):
    extension = get_extension(id)
    if request.method == 'POST':
        response = extension_maker.execute(extension)
        db = get_db()
        db.execute(
            'INSERT INTO executed_extensions (author_id, extension_id, extension_status_code, extension_headers) VALUES (?,?,?,?)',
            (g.user['id'], id, response['status_code'], response['headers'])
        )
        db.commit()
        return redirect(url_for('ext.tableau_extension', id=id, reload=True))
    return render_template('ext/tableau_extension.html', extension=extension)

@bp.route('/<int:id>/download_file', methods=['GET'])
@login_required
def send_file(id):
    extension = get_extension(id)
    with open(f'{current_app.config["TREX_files"]}/base_extension.trex','r') as f:
        text = f.read()
    f.close()
    url = url_for('ext.tableau_extension', id=extension['id'],_external=True)
    text = text.replace('{{CHANGE_URL}}',url)
    filename = f"extension_{str(extension['id'])}.trex"
    with open(f'{current_app.config["TREX_files"]}/{filename}', 'w') as f:
        f.write(text)
    f.close()
    return send_from_directory(current_app.static_folder, filename=f'trex/{filename}', as_attachment=True)