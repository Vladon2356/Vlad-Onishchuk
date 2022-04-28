from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from ..dicorators import admin_group_required, admin_or_writer_group_required
from ..models import PostModel, UserModel

posts_bp = Blueprint('posts', __name__)


@posts_bp.route("/posts", methods=["GET"])
def get_all_posts():
    posts = PostModel.return_all()
    return jsonify(posts)

@posts_bp.route("/posts/<int:id>", methods=["GET"])
def get_post(id):
    post = PostModel.find_by_id(id)
    if not post:
        return jsonify({"message": f"Post with id - {id} not found."}), 404
    return jsonify(post)

@posts_bp.route("/posts", methods=["POST"])
@jwt_required()
@admin_or_writer_group_required
def create_post():
    title = request.json.get("title")
    text = request.json.get("text")
    author_id = is_writer = request.json.get("author_id")
    if not title or not text or not author_id:
        return jsonify({'message': 'Please, specify "title", "text" and "author_id"'})
    post = PostModel(title=title, text=text, author_id=author_id)
    post.save_to_db()
    return jsonify({"id": post.id}), 201


@posts_bp.route("/posts/<int:id>", methods=["PATCH"])
@jwt_required()
@admin_or_writer_group_required
def update_post(id):
    title = request.json.get("title")
    text = request.json.get("text")
    post, code = PostModel.find_by_id(id, to_dict=False)
    if code == 404:
        return jsonify({"message": 'post not found'}), 404
    else:
        if title:
            post.title = title
        if text:
            post.text = text
        post.save_to_db()
        return jsonify({"message":"Updated"})

@posts_bp.route("/posts/<int:id>", methods=["DELETE"])
@jwt_required()
@admin_or_writer_group_required
def delete_post(id):
    code = PostModel.delete_by_id(id)
    if code == 404:
        return jsonify({"message": "Post not found."}), 404

    return jsonify({"message": "Deleted"})
