import pytest

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


def test_recognize_by_image(client):
    rv = client.post('/files', data={'image': 'test.jpg'})
    assert b'Be happy' in rv.data


def test_recognize_by_url(client):
    rv = client.post('/files', data={'url':
                                'https://images.freeimages.com/images/large-previews/b69/llibre-de-text-1311023.jpg'})
    assert b'Medios de ottros que' in rv.data


def test_error_extension_error(client):
    rv = client.post('/files', data={'image': 'test.py'})
    assert b'Server does not recognize files with this extension!' in rv.data


def test_error_invalid_request(client):
    rv = client.post('/files', data={'image': ''})
    assert b'Sorry but server could not understand your request. Try again later!' in rv.data
