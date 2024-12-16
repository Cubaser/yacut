from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from settings import (API_MESSAGE_BAD_CUSTOM_ID,
                      CUSTOM_ID_MAX_LEN,
                      CUSTOM_ID_PATTERN)


class LinkForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(max=CUSTOM_ID_MAX_LEN),
            Regexp(
                CUSTOM_ID_PATTERN,
                message=API_MESSAGE_BAD_CUSTOM_ID
            )
        ]
    )
    submit = SubmitField('Создать')
