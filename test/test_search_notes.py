from flask.testing import FlaskClient

def test_search_notes(test_app: FlaskClient):
    response = test_app.get('/search')
    response_data = response.data

    assert b'<select name="filter" id="filter" class="form-select" required>' in response_data
    assert b'<option value="Title">Search by Title</option>' in response_data
    assert b'<option value="Course">Search by Course</option>' in response_data
    assert b'<option value="Author">Search by Author</option>' in response_data