from flask.testing import FlaskClient

def test_view_all_notes(test_app: FlaskClient):
    response = test_app.get('/notes/list')
    response_data = response.data

    assert b'<p>No notes found</p>' in response_data