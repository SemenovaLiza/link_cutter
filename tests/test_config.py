import os


def test_env_vars():
    assert 'sqlite:///db.sqlite3' in list(os.environ.values()), (
        'Check for an environment variable with connection settings'
        'databases with the sqlite value:///db.sqlite3'
    )


def test_config(default_app):
    assert (
        default_app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///db.sqlite3'
    ), (
        'Check that the SQLALCHEMY_DATABASE_URL configuration key '
        'a value has been assigned with settings for connecting the database'
    )
    assert default_app.config['SECRET_KEY'] == os.getenv('SECRET_KEY'), (
        'Check that the SECRET_KEY configuration key '
        'assigned value')
