

def test_index_page(client):
    result = client.get('/')
    assert b'appengine_flask_security_auth' in result.data
