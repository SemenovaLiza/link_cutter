from flask import render_template, flash, redirect

from . import BASE_URL, app, db
from .forms import URLForm
from .models import URLMap
from .utils import custom_link_view, validate_custom_link


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        short_link = form.short_link.data
        if URLMap.query.filter_by(short=short_link).first():
            flash(f'Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        
        if not validate_custom_link(short_link):
            flash('Допустимые символы: A-z, 0-9. Длина не должна превышать 16 символов.')
            return render_template('index.html', form=form)

        if not short_link:
            short_link = custom_link_view()
        
        custom_link = URLMap(
            original=form.original_link.data,
            short=short_link
        )
        db.session.add(custom_link)
        db.session.commit()
        return render_template(
            'index.html', form=form,
            short_link=BASE_URL+custom_link.short,
            )
    return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def link_work_view(short):
    link = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(link.original)
