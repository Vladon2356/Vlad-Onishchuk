import pytest
from app.models import PostModel
from random import choice

def test_find_by_id(app):
    post = PostModel.find_by_id(id=2, to_dict=False)
    assert post.title == 'Post2'
    assert post.text == 'Test post2'
    assert post.author_id == 2

def test_find_by_not_exist_id(app):
    post, code = PostModel.find_by_id(id=9999, to_dict=False)
    assert post['message'] == 'Post with id 9999 not found'
    assert code == 404

def test_find_by_title(app):
    post = PostModel.find_by_titile(title='Post2', to_dict=False)
    assert post.title == 'Post2'
    assert post.text == 'Test post2'
    assert post.author_id == 2

def test_find_by_not_exist_title(app):
    post = PostModel.find_by_titile(title='Something', to_dict=False)
    assert post['message'] == 'Post with title Something not found'


def test_find_by_author_id(app):
    posts = PostModel.find_by_author_id(3, to_dict=False)
    assert choice(posts).author_id == 3
    assert choice(posts).author_id == 3
    assert choice(posts).author_id == 3
    assert choice(posts).author_id == 3


def test_find_by_not_extist_author_id(app):
    post = PostModel.find_by_author_id(9999, to_dict=False)
    assert isinstance(post, dict)


def test_return_all(app):
    posts = PostModel.return_all(to_dict=False)
    assert isinstance(posts, list)



def test_delete_by_id(app):
    deleted_post = PostModel.find_by_id(4, to_dict=False)
    code = PostModel.delete_by_id(4)
    posts = PostModel.return_all(to_dict=False)
    assert code == 200
    assert deleted_post not in posts

def test_delete_by_not_exist_id(app):
    code = PostModel.delete_by_id(9999)
    assert code == 404



def test_to_dict(app):
    post = PostModel.return_all(to_dict=False)
    res = PostModel.to_dict(post[3])
    assert res['id'] == 6
    assert res['title'] == 'Post3'
    assert res['text'] == 'Test post3'
    assert res['author_id'] == 3
