from app import app


def test_index():
    client = app.test_client()
    # JSON API preserved at /api (root now serves HTML)
    rv = client.get('/api')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['message'] == "Hello from Sparki Flask app"


def test_echo():
    client = app.test_client()
    rv = client.post('/echo', json={'hello': 'world'})
    assert rv.status_code == 200
    assert rv.get_json()['received'] == {'hello': 'world'}
