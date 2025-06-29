from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .models import URLMap
from .error_handlers import InvalidAPIUsage
from .utils import get_unique_short_id, check_url_symbols, check_unique_short_id


@app.route('/api/id/', methods=['POST'])
def add_opinion():
    data = request.get_json()

    if not data:
        raise InvalidAPIUsage('Request body is missing!', HTTPStatus.BAD_REQUEST)

    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" is required field!', HTTPStatus.BAD_REQUEST)

    if 'custom_id' not in data or data['custom_id'] is None:
        data['custom_id'] = get_unique_short_id()

    custom_short_id = data['custom_id']

    if check_unique_short_id(custom_short_id):
        raise InvalidAPIUsage('Suggested short link already exist!', HTTPStatus.BAD_REQUEST)

    if not check_url_symbols(custom_short_id):
        raise InvalidAPIUsage('Invalid name is specified for the short link!', HTTPStatus.BAD_REQUEST)

    link = URLMap()
    link.from_dict(data)
    db.session.add(link)
    db.session.commit()
    return jsonify(link.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Specified id was not found!', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK