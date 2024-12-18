from flask import flash, redirect, render_template

from . import app
from .forms import LinkForm
from .models import URLMap
from .error_handlers import InvalidAPIUsage
from settings import MESSAGE_URL_DONE


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    if form.validate_on_submit():
        try:
            url = URLMap.create_short_link(
                original=form.original_link.data,
                custom_id=form.custom_id.data
            )
            flash(MESSAGE_URL_DONE)
            return render_template(
                'index.html',
                url=url,
                form=form
            )
        except InvalidAPIUsage as error:
            flash(error.message, 'error')
    return render_template('index.html', form=form)


@app.route('/<short>', methods=['GET'])
def redirect_view(short):
    url = URLMap.get_url_by_short_id(short).first_or_404()
    return redirect(url.original)
