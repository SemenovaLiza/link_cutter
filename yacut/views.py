from flask import flash, redirect, render_template

from . import app, db, BASE_URL
from .forms import URLForm
from .models import URLMap
from .utils import check_unique_short_id, check_url_symbols, get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if check_unique_short_id(custom_id):
            flash("Предложенный вариант короткой ссылки уже существует.")
            return render_template('index.html', form=form)

        if custom_id and not check_url_symbols(custom_id):
            flash('Указано недопустимое имя для короткой ссылки')
            return render_template('index.html', form=form)

        if not custom_id:
            custom_id = get_unique_short_id()

        custom_link = URLMap(
            original=form.original_link.data,
            short=custom_id
        )
        db.session.add(custom_link)
        db.session.commit()
        return render_template(
            'index.html', form=form,
            custom_id=BASE_URL + custom_link.short,
        )
    return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def link_work_view(short):
    link = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(link.original)