from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from settings import SHORT_LINK_MAX_LENGHT, REGEX_FORM_VALIDATION


class URLForm(FlaskForm):
    original_link = URLField(
        'Long link',
        validators=[DataRequired(message='Required field'),
                    Length(1, 256)]
    )
    custom_id = URLField(
        'Your short link option',
        validators=[Length(max=SHORT_LINK_MAX_LENGHT, message=f'The maximum length of link should be {SHORT_LINK_MAX_LENGHT} symbols'),
                    Regexp(REGEX_FORM_VALIDATION, message='The link must consist of numbers and latin letters.'),
                    Optional()]
    )
    submit = SubmitField('Add')