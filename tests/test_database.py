from sqlalchemy import inspect

from yacut.models import URLMap


def test_fields(_app):
    inspector = inspect(URLMap)
    fields = [column.name for column in inspector.columns]
    print(fields)
    assert (
        all(field in fields for field 
            in ['id', 'original', 'short', 'timestamp'])
    ), (
        'All necessary fields were not found in the model. '
        'Check the model: it should contain the fields id, original, short and timestamp.'
    )