def test_get_user_detail(client, app, authentication_headers):
    response = client.get(
        '/users/3',
        headers=authentication_headers(is_admin=True)
    )
    assert response.json['id'] == 3

def test_get_not_exist_user(client, app, authentication_headers):
    response = client.get(
        '/users/999',
        headers=authentication_headers(is_admin=True)
    )
    assert response.json['message'] == 'User not found.'


def test_get_all_users(client, app, authentication_headers):
    response = client.get(
        '/users',
        headers=authentication_headers
    )
    assert response.json[0]['id'] == 1


def test_delete_user(client, app, authentication_headers):
    response = client.delete(
        '/users/1',
        headers=authentication_headers(is_admin=True)
    )
    assert response.json['message'] == 'Deleted'

def test_delete_not_exist_user(client, app, authentication_headers):
    response = client.delete(
        '/users/999',
        headers=authentication_headers(is_admin=True)
    )
    assert response.json['message'] == 'User not found.'


def test_update_user(client, app, authentication_headers):
    response = client.patch(
        '/users/3',
        json={
            "name": "Tony",
            "age": 33,
            "username": " ToN33"
        },
        headers=authentication_headers(is_admin=True)
    )
    assert response.json['message'] == 'Updated'

def test_update_not_extist_user(client, app, authentication_headers):
    response = client.patch(
        '/users/999',
        json={
            "name": "Tony",
            "age": 33,
            "username": " ToN33"
        },
        headers=authentication_headers(is_admin=True)
    )
    assert response.json['message'] == 'User not found.'
