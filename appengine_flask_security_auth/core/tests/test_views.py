

def test_index_page(client):
    result = client.get('/')
    assert b'classiplex' in result.data
