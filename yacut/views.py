import random

from flask import render_template, request, redirect

from . import app, db
from .forms import LinkForm
from .models import URLMap
from settings import (CHARS,
                      SHORT_LINK_LENGTH,
                      MESSAGE_URL_DONE,
                      MESSAGE_URL_FAIL)


def get_unique_short_id(custom_id=None):
    if custom_id:
        return custom_id
    short_id = ''.join(random.choices(CHARS, k=SHORT_LINK_LENGTH))
    while check_unique_short_id(short_id):
        short_id = request.host_url + ''.join(random.choices(CHARS, k=6))
    return short_id


def check_unique_short_id(short_id):
    if URLMap.query.filter_by(short=short_id).first() is not None:
        return True
    return False


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    if form.validate_on_submit():
        if form.custom_id.data and check_unique_short_id(form.custom_id.data):
            return render_template(
                'index.html',
                message=MESSAGE_URL_FAIL,
                form=form
            )
        unique_short_id = get_unique_short_id(form.custom_id.data)
        url = URLMap(
            original=form.original_link.data,
            short=unique_short_id
        )
        db.session.add(url)
        db.session.commit()
        return render_template(
            'index.html',
            url=url,
            message=MESSAGE_URL_DONE,
            form=form
        )
    return render_template('index.html', form=form)


@app.route('/<short>', methods=['GET'])
def redirect_view(short):
    url = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url.original)
