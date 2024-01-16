from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from settings import SHORT_LINK_MAX_LENGHT, REGEX_FORM_VALIDATION


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 256)]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Length(max=SHORT_LINK_MAX_LENGHT, message=f'Максимальная длина ссылки должна быть {SHORT_LINK_MAX_LENGHT} символов'),
                    Regexp(REGEX_FORM_VALIDATION, message='Ссылка должна состоять из цифр и латинские букв.'),
                    Optional()]
    )
    submit = SubmitField('Добавить')