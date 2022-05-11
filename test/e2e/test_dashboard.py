from flask.testing import FlaskClient

def test_dashboard(test_app: FlaskClient):
    response = test_app.get('/dashboard', follow_redirects = True)
    response_data = response.data
    assert b'<input type="text" id="username" name="username" class="form-control" autocomplete="off" required>' in response_data
    assert b'<label class="form-label" for="username">Username</label>' in response_data