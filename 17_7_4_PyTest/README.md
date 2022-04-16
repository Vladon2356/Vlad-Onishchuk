# JWT tokens with admin group example
Here only authenticated admins can list, create, update or delete users.
Authenticated non-admins can see secret resource and shared resource.
Unauthenticated users can only see shared resource.

shared resource - post and list of post

secret - others

POST /auth/registration - create user and get tokens


raw - {
        "is_writer": true,
        "is_admin": true,
        "name": "Test",
        "username": "Testuser",
        "age": 33,
        "email": "test@gmail.gom",
        "password": "1"
}  

POST /auth/login {"username": "Testuser", "password": "1"}  - get tokens

POST /auth/refresh Authorization: Bearer refresh-token-here  - get new access token

POST /auth/logout-access Authorization: Bearer access-token-here  - revoke access token

POST /auth/logout-refresh Authorization: Bearer refresh-token-here  - revoke refresh token

GET /users  - list users (only for admin)

POST /users  - create a user

GET /users/{id}  - get user by id (only for admin)

PATCH /users/{id}  - update user by id (only for admin)

DELETE /users/{id}  - delete user by id (only for admin)

GET /posts  - list of posts 

POST /posts  - create a post (only for admin or writer)

GET /posts/{id}  - get post by id

PATCH /posts/{id}  - update post by id (only for admin or writer)

DELETE /posts/{id}  - delete post by id (only for admin or writer)


# How to run it
1. pip install -r requirements.txt
2. From root:
```python run.py```
