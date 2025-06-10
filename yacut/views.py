from flask import flash, redirect, render_template, jsonify, request

from . import app, db, BASE_URL
from .forms import URLForm
from .models import URLMap
from .utils import check_unique_short_id, check_url_symbols, get_unique_short_id


# @app.route('/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            custom_id = form.custom_id.data
            if check_unique_short_id(custom_id):
                flash("Suggested short link already exist!")
                return render_template('index.html', form=form)

            if custom_id and not check_url_symbols(custom_id):
                flash('Invalid name is specified for the short link!')
                return render_template('index.html', form=form)

            if not custom_id:
                custom_id = get_unique_short_id()

            custom_link = URLMap(
                original=form.original_link.data,
                short=custom_id
            )
            db.session.add(custom_link)
            db.session.commit()
            return jsonify({'success': True, 'custom_id': custom_id})
        else:
            jsonify({'status': 'error', 'errors': form.errors})

    return render_template('index.html', form=form)

# db.session.add(custom_link)
 #       db.session.commit()

@app.route('/<string:short>', methods=['GET'])
def link_work_view(short):
    link = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(link.original)