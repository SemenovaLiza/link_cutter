from flask import Flask, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired
import random
from string import ascii_letters, digits

from datetime import datetime


app = Flask(__name__)
LINK_CHOICES_ELEMENTS = list(ascii_letters + digits)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'MY SECRET KEY'
BASE_URL = 'http://127.0.0.1:5000/'
db = SQLAlchemy(app)


class URLForm(FlaskForm):
    original = StringField(
        'Введите исходную ссылку',
        validators=[DataRequired(message='Обязательное поле')]
    )
    short = StringField(
        'Введите короткую ссылку'
    )
    submit = SubmitField('Создать')

def get_unique_short_id():
    short_link = random.choices(LINK_CHOICES_ELEMENTS, k=6)
    return ''.join(short_link)


@app.route('/', methods=['GET', 'POST'])
def id_view():
    form = URLForm()
    if form.validate_on_submit():
        custom_short_link = form.short.data
        if custom_short_link is not None:
            if URLMap.query.filter_by(short=custom_short_link).first() is not None:
                flash('Предложенный вариант короткой ссылки уже существует.', 'exception-message')
                return render_template('index.html', form=form)

        if custom_short_link is None:
            custom_short_link = get_unique_short_id()

        link = URLMap(
            original=form.original.data,
            short=form.short.data
        )
        db.session.add(link)
        db.session.commit()

        return render_template(
            'index.html', form=form,
            short_link=BASE_URL + link.short,
            original_link=link.original
        )
    return render_template('index.html', form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_short_link_view(short):
    link = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(link.original)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(250), nullable=False)
    short = db.Column(db.String(16), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, unique=True, default=datetime.utcnow)

if __name__ == '__main__':
    app.run()