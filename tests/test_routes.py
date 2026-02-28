def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Cloud Inventory" in response.data

def test_api_products(client):
    response = client.get('/api/products')
    assert response.status_code == 200
    assert isinstance(response.json['products'], list)
