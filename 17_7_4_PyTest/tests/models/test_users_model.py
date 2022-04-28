import pytest
from app.models import UserModel

# Methods
def test_find_by_id(app):
    user = UserModel.find_by_id(id=5,to_dict=False)
    assert user.name == 'Test writer'
    assert user.age == 22
    assert user.email == 'test@gmail.gom'
    assert user.username == 'Twriter4'
    assert user.is_admin== False
    assert user.is_writer == True
def test_find_by_not_exist_id(app):
    user = UserModel.find_by_id(id=999)
    assert user == {}

def test_find_by_username(app):
    user = UserModel.find_by_username(username='Twriter4',to_dict=False)
    assert user.name == 'Test writer'
    assert user.age == 22
    assert user.email == 'test@gmail.gom'
    assert user.username == 'Twriter4'


def test_find_by_not_exist_username(app):
    user = UserModel.find_by_username(username='something',to_dict=False)
    assert user == {}


def test_find_by_email(app):
    user = UserModel.find_by_email(email='test@gmail.gom',to_dict=False)
    assert user.name == 'Test writer'
    assert user.age == 22
    assert user.email == 'test@gmail.gom'
    assert user.username == 'Twriter4'



def test_find_by_not_exist_email(app):
    user = UserModel.find_by_email(email='XXX@xxx.com',to_dict=False)
    assert user == {}

def test_return_all(app):
    users = UserModel.return_all(to_dict=False)
    assert len(users) >= 1


def test_delete_by_id(app):
    deleted_user = UserModel.find_by_id(10, to_dict=False)
    code = UserModel.delete_by_id(10)
    users = UserModel.return_all(to_dict=False)
    assert code == 200
    assert deleted_user not in users

def test_delete_by_not_exist_id(app):
    code = UserModel.delete_by_id(999)
    assert code == 404


def test_to_dict(app):
    user = UserModel.find_by_id(5, to_dict=False)

    res = UserModel.to_dict(user)
    assert res['id'] == 5
    assert res['name'] == 'Test writer'
    assert res['age'] == 22
    assert res['username'] == 'Twriter4'
    assert res['email'] == 'test@gmail.gom'
    assert res['is_admin'] == False
    assert res['is_writer'] == True
