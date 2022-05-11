from flask.testing import FlaskClient

def test_search_notes(test_app: FlaskClient):
    response = test_app.get('/search')
    response_data = response.data

    assert b'<option value="Title">Search by Title</option>' in response_data
    assert b'<option value="Course">Search by Course</option>' in response_data
    assert b'<option value="Author">Search by Author</option>' in response_data
    assert b'<input type="text" name="q" id="q" class="form-control" autocomplete="off" required>' in response_data