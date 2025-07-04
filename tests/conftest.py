import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv
from mixer.backend.flask import mixer as _mixer

load_dotenv()

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR))


try:
    from yacut import app, db
    from yacut.models import URLMap
except NameError:
    raise AssertionError(
        'The application object was not detected. Create an instance of the Flask class and '
        'name it app',
    )
except ImportError as exc:
    if any(obj in exc.name for obj in ['models', 'URLMap']):
        raise AssertionError('The URLMap model was not found in the models file')
    raise AssertionError(
        'An object of the SQLAlchemy class was not detected. Create it and name it db.'
    )


@pytest.fixture
def default_app():
    with app.app_context():
        yield app


@pytest.fixture
def _app(tmp_path):
    db_path = tmp_path / 'test_db.sqlite3'
    db_uri = 'sqlite:///' + str(db_path)
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': db_uri,
        'WTF_CSRF_ENABLED': False,
    })
    with app.app_context():
        db.create_all()
    yield app
    db.drop_all()
    db.session.close()
    db_path.unlink()


@pytest.fixture
def client(_app):
    return _app.test_client()


@pytest.fixture
def cli_runner():
    return app.test_cli_runner()


@pytest.fixture
def mixer():
    _mixer.init_app(app)
    return _mixer


@pytest.fixture
def short_python_url(mixer):
    return mixer.blend(URLMap, original='https://www.python.org', short='py')
