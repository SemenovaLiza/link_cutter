import pytest

from yacut.models import URLMap

py_url = 'https://www.python.org'


def test_create_id(client):
    got = client.post('/api/id/', json={
        'url': py_url,
        'custom_id': 'py',
    })
    assert got.status_code == 201, (
        'When creating a short link, the status code 201 should be returned'
    )
    assert list(got.json.keys()) == ['short_link', 'url'], (
        'When creating a short link, the response must contain the keys `url, '
        'short_link`'
    )
    assert got.json == {
        'url': py_url,
        'short_link': 'http://localhost/py',
    }, 'When creating a short link, the API response body differs from the expected one.'


def test_create_empty_body(client):
    try:
        got = client.post('/api/id/')
    except Exception:
        raise AssertionError(
            'If no information is passed in the request body, raise an exception.'
        )
    assert got.status_code == 400, (
        'In response to an empty POST request to the endpoint `/api/id/`must '
        'return status code 400.'
    )
    assert list(got.json.keys()) == ['message'], (
        'In response to an empty POST request to the endpoint `/api/id/` must be '
        'the `message` key'
    )
    assert got.json == {'message': 'Request body is missing'}, (
        'A message in the response body when creating a short link '
        'without a body in the request does not meet the specification'
    )


@pytest.mark.parametrize('json_data', [
    ({'url': py_url, 'custom_id': '.,/!?'}),
    ({'url': py_url, 'custom_id': 'Hodor-Hodor'}),
    ({'url': py_url, 'custom_id': 'h@k$r'}),
    ({'url': py_url, 'custom_id': '$'}),
    ({'url': py_url, 'custom_id': 'п'}),
    ({'url': py_url, 'custom_id': 'l l'}),
])
def test_invalid_short_url(json_data, client):
    got = client.post('/api/id/', json=json_data)
    assert got.status_code == 400, (
        'If the short link name is invalid, the response status must '
        'be 400'
    )
    assert list(got.json.keys()) == ['message'], (
        'If the short link name is invalid, the response must be '
        'the `message` key'
    )
    assert (
        got.json == {'message': 'Invalid name is specified for a short link'}
    ), (
        'If the short link name is invalid, a message is returned that '
        'does not match the specification.'
    )
    unique_id = URLMap.query.filter_by(original=py_url).first()
    assert not unique_id, (
        'The short link must be allowed to use strictly '
        'a specific set of characters. Refer to the task text.'
    )


def test_no_required_field(client):
    try:
        got = client.post('/api/id/', json={
            'short_link': 'python',
        })
    except Exception:
        raise AssertionError(
            'If the body of the endpoint request `/api/id/` differs from '
            'expected - throw an exception.'
        )
    assert got.status_code == 400, (
        'If the body of the endpoint request `/api/id/` differs from the expected one '
        '- return the status code 400.'
    )
    assert list(got.json.keys()) == ['message'], (
        'If the body of the endpoint request `/api/id/` differs from the expected - '
        'return a response with the `message` key.'
    )
    assert got.json == {'message': '\"url\" является обязательным полем!'}, (
        'A message in the response body with an incorrect request body '
        'does not meet the specification'
    )


def test_url_already_exists(client, short_python_url):
    try:
        got = client.post('/api/id/', json={
            'url': py_url,
            'custom_id': 'py',
        })
    except Exception:
        raise AssertionError(
            'When trying to create a link with a short name that is already '
            'busy - raise an exception.'
        )
    assert got.status_code == 400, (
        'When trying to create a link with a short name that is already occupied - '
        'return the status code 400'
    )
    assert list(got.json.keys()) == ['message'], (
        'When trying to create a link with a short name that is already occupied - '
        'return a response with the `message` key.'
    )
    assert (
        got.json == {
            'message': 'The offered short link option already exists.'
        }
    ), (
        'When trying to create a link with a short name that is already occupied '
        'a message is returned with a text that does not match the specification.'
    )


@pytest.mark.parametrize('json_data', [
    ({'url': py_url, 'custom_id': None}),
    ({'url': py_url, 'custom_id': ''}),
])
def test_generated_unique_short_id(json_data, client):
    try:
        got = client.post('/api/id/', json=json_data)
    except Exception:
        raise AssertionError(
            'For a request in which the short_id is missing or contains an empty '
            'string - generate an unique short_id.'
        )
    assert got.status_code == 201, (
        'When creating a short link without an explicitly specified name '
        'the status code 201 should be returned'
    )
    unique_id = URLMap.query.filter_by(original=py_url).first()
    assert unique_id, (
        'When creating a short link without an explicitly specified name '
        'it is necessary to generate the relative part of the link '
        'from numbers and Latin characters - and save the link in the database'
    )
    assert got.json == {
        'url': py_url,
        'short_link': 'http://localhost/' + unique_id.short,
    }, (
        'When creating a short link without an explicitly specified name '
        'it is necessary to generate the relative part of the link '
        'from numbers and Latin characters - and return the link in the API response.'
    )


def test_get_url_endpoint(client, short_python_url):
    got = client.get(f'/api/id/{short_python_url.short}/')
    assert got.status_code == 200, (
        'In response to the endpoint GET request `/api/id/<short_id>/`must'
        'return status code 200'
    )
    assert list(got.json.keys()) == ['url'], (
        'In response to the endpoint GET request, `/api/id/<short_id>/` '
        'the `url` key must be passed'
    )
    assert got.json == {'url': py_url}, (
        'When making a GET request to the endpoint, `/api/id/<short_id>/` is returned '
        'an response that does not meet the specification.'
    )


def test_get_url_not_found(client):
    got = client.get('/api/id/{enexpected}/')
    assert got.status_code == 404, (
        'In response to a GET request to get a non-existent link '
        'the 404 status code should be returned.'
    )
    assert list(got.json.keys()) == ['message'], (
        'In response to a GET request to get a non-existent link, you must '
        'pass the `message`'
    )
    assert got.json == {'message': 'The specified id was not found'}, (
        'The response to a GET request to get a non-existent link is not '
        'conforms to the specification.'
    )


def test_len_short_id_api(client):
    long_string = (
        'CuriosityisnotasinHarryHoweverfromtimetotimeyoushouldexercisecaution'
    )
    got = client.post('/api/id/', json={
        'url': py_url,
        'custom_id': long_string,
    })
    assert got.status_code == 400, (
        'If the `short_id` field contains a string longer than 16 characters '
        'during the POST request to the endpoint `/api/id/` '
        ', status code 400 should be returned.'
    )
    assert list(got.json.keys()) == ['message'], (
        'If, during a POST request to the endpoint `/api/id/` '
        ', the `short_id` field contains a string longer than 16 characters, '
        'there must be a `message` key in the response.'
    )
    assert (
        got.json == {'message': 'Invalid name is specified for a short link'}
    ), (
        'During a POST request to the endpoint `/api/id/`, in the `short_id` field '
        'string longer than 16 characters was passed, the response is returned, not '
        'corresponding to the specification.'
    )


def test_len_short_id_autogenerated_api(client):
    client.post('/api/id/', json={
        'url': py_url,
    })
    unique_id = URLMap.query.filter_by(original=py_url).first()
    assert len(unique_id.short) == 6, (
        'For a POST request that does not contain a short link, '
        'a short link with a length of 6 characters must be generated.'
    )
