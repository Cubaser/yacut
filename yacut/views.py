from flask import redirect, render_template

from . import app
from .forms import LinkForm
from .models import URLMap
from settings import MESSAGE_URL_DONE, MESSAGE_URL_FAIL


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    if form.validate_on_submit():
        if (form.custom_id.data and
                URLMap.check_unique_short_id(form.custom_id.data)):
            return render_template(
                'index.html',
                message=MESSAGE_URL_FAIL,
                form=form
            )
        url = URLMap(
            original=form.original_link.data,
            short=form.custom_id.data
        )
        url.save_data()
        return render_template(
            'index.html',
            url=url,
            message=MESSAGE_URL_DONE,
            form=form
        )
    return render_template('index.html', form=form)


@app.route('/<short>', methods=['GET'])
def redirect_view(short):
    url = URLMap.get_url_by_short_id(short).first_or_404()
    return redirect(url.original)
