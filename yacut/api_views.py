from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from settings import (API_MESSAGE_BODY_FAIL,
                      API_MESSAGE_CUSTOM_ID_FAIL,
                      API_MESSAGE_URL_FAIL)


def check_request(request):
    try:
        return request.get_json()
    except Exception:
        raise InvalidAPIUsage(API_MESSAGE_BODY_FAIL)


@app.route('/api/id/', methods=['POST'])
def create_short_id():
    data = check_request(request)
    if 'url' not in data:
        raise InvalidAPIUsage(API_MESSAGE_URL_FAIL)
    if 'custom_id' in data:
        url = URLMap(
            original=data['url'],
            short=data['custom_id']
        )
        url.save_api_data()
        return jsonify(url.to_dict()), HTTPStatus.CREATED
    url = URLMap(
        original=data['url']
    )
    url.save_api_data()
    return jsonify(url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_short_id(short_id):
    url = URLMap.get_url_by_short_id(short_id).first()
    if not url:
        raise InvalidAPIUsage(API_MESSAGE_CUSTOM_ID_FAIL, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK
