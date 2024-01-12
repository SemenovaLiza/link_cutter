from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .models import URLMap
from .error_handlers import InvalidAPIUsage
from .utils import custom_link_view, validate_custom_link, check_unique_short_id


@app.route('/api/id/', methods=['POST'])
def add_opinion():
    data = request.get_json()

    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса', HTTPStatus.BAD_REQUEST)

    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!', HTTPStatus.BAD_REQUEST)
    
    if 'custom_id' not in data or data['custom_id'] is None:
        data['custom_id'] = custom_link_view()

    custom_short_id = data['custom_id']

    if check_unique_short_id(custom_short_id):
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.', HTTPStatus.BAD_REQUEST)
    
    if not validate_custom_link(custom_short_id):
        raise InvalidAPIUsage('Допустимые символы: A-z, 0-9. Длина не должна превышать 16 символов.', HTTPStatus.BAD_REQUEST)
    

    link = URLMap()
    link.from_dict(data)
    db.session.add(link)
    db.session.commit()
    return jsonify(link.to_dict()), HTTPStatus.CREATED

@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if not link:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': link.to_dict()}), HTTPStatus.OK