from flask.testing import FlaskClient

def test_view_all_notes(test_app: FlaskClient):
    response = test_app.get('/notes/list')
    response_data = response.data

    assert b'<h1 class="mb-5">All Notes</h1>' in response_data