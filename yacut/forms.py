from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

from settings import ORIGINAL_LINK_MIN_MAX, CUSTOM_ID_MAX_LEN


class LinkForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(*ORIGINAL_LINK_MIN_MAX)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(max=CUSTOM_ID_MAX_LEN)]
    )
    submit = SubmitField('Создать')
