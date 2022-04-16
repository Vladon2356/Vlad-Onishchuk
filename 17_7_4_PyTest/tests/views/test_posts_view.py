
def test_get_post_detail(client, app, authentication_headers):
    response = client.get(
        '/posts/3',
        headers=authentication_headers(is_admin=True)
    )
    assert response.json['id'] == 3

def test_get_not_exist_post(client, app, authentication_headers):
    response = client.get(
        '/posts/999',
        headers=authentication_headers(is_admin=True)
    )
    assert response.json['message'] == 'Post with id - 999 not found.'


def test_get_all_posts(client, app, authentication_headers):
    response = client.get(
        '/posts',
    )

    assert response.json[0]['id'] == 2


def test_create_post(client, app, authentication_headers):
    response = client.post(
        '/posts',
        json={
            "title": "TestTitle",
            "text": "TestText",
            "author_id": 9
        },
        headers=authentication_headers(is_admin=True)
    )
    assert isinstance(response.json['id'], int)

def test_create_post_without_title(client, app, authentication_headers):
    response = client.post(
        '/posts',
        json={
            "text": "TestText",
            "author_id": 9
        },
        headers=authentication_headers(is_admin=True)
    )
    assert response.json['message'] == 'Please, specify "title", "text" and "author_id"'


def test_create_post_without_text(client, app, authentication_headers):
    response = client.post(
        '/posts',
        json={
            "text": "TestText",
            "author_id": 9
        },
        headers=authentication_headers(is_admin=True)
    )
    assert response.json['message'] == 'Please, specify "title", "text" and "author_id"'

def test_create_post_without_author_id(client, app, authentication_headers):
    response = client.post(
        '/posts',
        json={
            "title": "TestTitle",
            "text": "TestText"
        },
        headers=authentication_headers(is_admin=True)
    )
    assert response.json['message'] == 'Please, specify "title", "text" and "author_id"'

def test_update_post(client, app, authentication_headers):
    response = client.patch(
        '/posts/3',
        json={
            "title": "Test title",
            "text": "Test text",
        },
        headers=authentication_headers(is_admin=True)
    )

    assert response.json['message'] == 'Updated'


def test_update_not_exist_post(client, app, authentication_headers):
    response = client.patch(
        '/posts/999',
        json={
            "title": "Test title",
            "text": "Test text",
        },
        headers=authentication_headers(is_admin=True)
    )

    assert response.json['message'] == 'post not found'


def test_delete_post(client, app, authentication_headers):
    response = client.delete(
        '/posts/48',
        headers=authentication_headers(is_admin=True)
    )
    assert response.json['message'] == 'Deleted'

def test_delete_not_exist_post(client, app, authentication_headers):
    response = client.delete(
        '/posts/999',
        headers=authentication_headers(is_admin=True)
    )
    assert response.json['message'] == 'Post not found.'
