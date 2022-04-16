from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

from app.models import UserModel
from ..decorators import admin_group_required

users_bp = Blueprint('users', __name__)


@users_bp.route("/users", methods=["GET"])
@jwt_required()
@admin_group_required
def get_users():
    users = UserModel.return_all()
    return jsonify(users)


@users_bp.route("/users/<int:id>", methods=["GET"])
@jwt_required()
@admin_group_required
def get_user(id):
    user = UserModel.find_by_id(id)
    if not user:
        return jsonify({"message": "User not found."}), 404

    return jsonify(user)


@users_bp.route("/users", methods=["POST"])
@jwt_required()
@admin_group_required
def create_user():
    if not request.json:
        return jsonify({"message": 'Please, specify "username", "name", "email", "password" and "age".'}), 400

    age = request.json.get("age")
    name = request.json.get("name")
    email = request.json.get("email")
    username = request.json.get("username")
    password = request.json.get("password")
    is_admin = request.json.get("is_admin", False)
    is_writer = request.json.get("is_writer", False)

    if not (age and name and username and password and email):
        return jsonify({"message": 'Please, specify "username", "name", "email" "password" and "age".'}), 400

    user = UserModel(
        name=name, age=age, username=username, is_admin=is_admin, email=email,is_writer=is_writer,
        hashed_password=UserModel.generate_hash(password))
    user.save_to_db()

    return jsonify({"id": user.id}), 201


@users_bp.route("/users/<int:id>", methods=["PATCH"])
@jwt_required()
@admin_group_required
def update_user(id):
    age = request.json.get("age")
    name = request.json.get("name")
    email = request.json.get("email")
    username = request.json.get("username")
    password = request.json.get("password")
    is_admin = request.json.get("is_admin")
    is_writer = request.json.get("is_writer")

    user = UserModel.find_by_id(id, to_dict=False)
    if not user:
        return jsonify({"message": "User not found."}), 404

    if not is_admin is None:
        user.is_admin = is_admin
    if  notis_writer is None:
        user.is_writer = is_writer
    if age:
        user.age = age
    if name:
        user.name = name
    if username:
        user.username = username
    if password:
        user.hashed_password = UserModel.generate_hash(password)
    if email:
        user.email = email
    user.save_to_db()
    return jsonify({"message": "Updated"})


@users_bp.route("/users/<int:id>", methods=["DELETE"])
@jwt_required()
@admin_group_required
def delete_user(id):
    code = UserModel.delete_by_id(id)
    if code == 404:
        return jsonify({"message": "User not found."}), 404

    return jsonify({"message": "Deleted"})
