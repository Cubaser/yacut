import re

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id, check_unique_short_id
from settings import (API_MESSAGE_URL_FAIL,
                      API_MESSAGE_BODY_FAIL,
                      API_MESSAGE_DOUBLE_CUSTOM_ID,
                      API_MESSAGE_BAD_CUSTOM_ID,
                      API_MESSAGE_CUSTOM_ID_FAIL,
                      CUSTOM_ID_PATTERN,
                      CUSTOM_ID_MAX_LEN)


def check_request(request):
    try:
        return request.get_json()
    except:
        raise InvalidAPIUsage(API_MESSAGE_BODY_FAIL)


@app.route('/api/id/', methods=['POST'])
def create_short_id():
    data = check_request(request)
    if 'url' not in data:
        raise InvalidAPIUsage(API_MESSAGE_URL_FAIL)
    if 'custom_id' in data:
        if check_unique_short_id(data['custom_id']):
            raise InvalidAPIUsage(API_MESSAGE_DOUBLE_CUSTOM_ID)
        elif (not re.fullmatch(CUSTOM_ID_PATTERN, data['custom_id'])
              or len(data['custom_id']) > CUSTOM_ID_MAX_LEN):
            raise InvalidAPIUsage(API_MESSAGE_BAD_CUSTOM_ID)
        else:
            unique_short_id = get_unique_short_id(data['custom_id'])
    else:
        unique_short_id = get_unique_short_id()
    url = URLMap(
        original=data['url'],
        short=unique_short_id
    )
    db.session.add(url)
    db.session.commit()
    url.short = url.short
    return jsonify(url.to_dict()), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def gets_short_id(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsage(API_MESSAGE_CUSTOM_ID_FAIL, 404)
    return jsonify({'url': url.original}), 200
