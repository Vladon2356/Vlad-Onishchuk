def test_register(client, app):
    response = client.post(
        '/auth/registration',
        json={
            "is_writer": True,
            "is_admin": True,
            "name": "Test",
            "username": "Testuser1",
            "age": 33,
            "email": "test@gmail.gom",
            "password": "1"
        }
    )
    assert response.json['message'] == "User Testuser1 was created"

def test_register_without_data(client, app):
    response = client.post(
        '/auth/registration',
        json={
            "is_writer": True,
            "is_admin": True,
            "name": "Test",
            "age": 33,
            "password": "1"
        }
    )
    assert response.json['message'] == 'Please, provide "age", "name", username", "email" and "password" in body.'


def test_user_already_exists(client, app, authentication_headers):
    response = client.post(
        '/auth/registration',
        json={
            "is_writer": True,
            "is_admin": True,
            "name": "Test",
            "username": "Testuser",
            "age": 33,
            "email": "test@gmail.gom",
            "password": "1"
        }
    )
    assert response.json['message'] == "User with username - Testuser already exists"


def test_login_with_right_username_and_wrong_password(client, app):
    response = client.post(
        '/auth/login',
        json={
            "username": 'Testuser',
            "password": '000'
        }
    )
    assert response.json['message'] == "Wrong password"


def test_login_with_wrong_username(client, app):
    response = client.post(
        '/auth/login',
        json={
            "username": 'Test12345',
            "password": '123'
        }
    )
    assert response.json['message'] == "User Test12345 doesn't exist"


def test_refresh(client, app, authentication_headers):
    response = client.post(
        '/auth/refresh',
        headers={'Authorization':f'Bearer {authentication_headers(is_admin=True)["refresh_token"]}'}
    )
    assert response.json['access_token'] is not None


def test_auth_logout_access(client, app, authentication_headers):
    response = client.post(
        '/auth/logout-access',
        headers=authentication_headers(is_admin=True)
    )
    assert response.json['message'] == 'Access token has been revoked'


def test_auth_logout_refresh(client, app, authentication_headers):
    response = client.post(
        '/auth/logout-refresh',
        headers={'Authorization':f'Bearer {authentication_headers(is_admin=True)["refresh_token"]}'}
    )
    assert response.json['message'] == 'Refresh token has been revoked'
